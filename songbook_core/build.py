#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Build a songbook, according to parameters found in a .sb file."""

import codecs
import glob
import json
import logging
import os.path
import re
import subprocess

from songbook_core import __SHAREDIR__
from songbook_core import errors
from songbook_core.files import recursive_find
from songbook_core.index import process_sxd
from songbook_core.songs import Song, SongsList

EOL = "\n"


def parse_template(template):
    """Return the list of parameters defined in the template."""
    embedded_json_pattern = re.compile(r"^%%:")
    with open(template) as template_file:
        code = [
                line[3:-1]
                for line
                in template_file
                if embedded_json_pattern.match(line)
                ]

    data = json.loads(''.join(code))
    parameters = dict()
    for param in data:
        parameters[param["name"]] = param
    return parameters


# pylint: disable=too-many-return-statements
def to_value(parameter, data):
    if "type" not in parameter:
        return data
    elif parameter["type"] == "stringlist":
        if "join" in parameter:
            join_text = parameter["join"]
        else:
            join_text = ''
        return join_text.join(data)
    elif parameter["type"] == "color":
        return data[1:]
    elif parameter["type"] == "font":
        return data + 'pt'
    elif parameter["type"] == "enum":
        return data
    elif parameter["type"] == "file":
        return data
    elif parameter["type"] == "flag":
        if "join" in parameter:
            join_text = parameter["join"]
        else:
            join_text = ''
        return join_text.join(data)


def format_declaration(name, parameter):
    """Return LaTeX code to declare variale 'name'.

    'parameter' is the corresponding line of the template (which can provide
    default value).
    """
    value = ""
    if "default" in parameter:
        value = parameter["default"]
    return (
            r'\def\set@{name}#1{{\def\get{name}{{#1}}}}'.format(name=name)
            + EOL
            + format_definition(name, to_value(parameter, value))
            )


def format_definition(name, value):
    """Return LaTeX code to define and set default value of variable 'name'"""
    return r'\set@{name}{{{value}}}'.format(name=name, value=value) + EOL


def clean(basename):
    """Clean (some) temporary files used during compilation.

    Depending of the LaTeX modules used in the template, there may be others
    that are note deleted by this function."""
    generated_extensions = [
            "_auth.sbx",
            "_auth.sxd",
            ".aux",
            ".log",
            ".out",
            ".sxc",
            ".tex",
            "_title.sbx",
            "_title.sxd",
            ]

    for ext in generated_extensions:
        try:
            os.unlink(basename + ext)
        except Exception as exception:
            raise errors.CleaningError(basename + ext, exception)

DEFAULT_AUTHWORDS = {
        "after": ["by"],
        "ignore": ["unknown"],
        "sep": ["and"],
        }

# pylint: disable=too-few-public-methods
class Songbook(object):
    """Reprensent a songbook (.sb) file.

    - Low level: provide a Python representation of the values stored in the
      '.sb' file.
    - High level: provide some utility functions to manipulate these data.
    """

    def __init__(self, raw_songbook, basename):
        super(Songbook, self).__init__()
        self.basename = basename
        # Default values: will be updated while parsing raw_songbook
        self.config = {
                'template': os.path.join(
                    __SHAREDIR__,
                    "templates",
                    "default.tmpl",
                    ),
                'titleprefixwords': [],
                'authwords': {},
                'lang': 'french',
                'sort': [u"by", u"album", u"@title"],
                'songs': None,
                'datadir': os.path.abspath('.'),
                }
        self.songslist = None
        self._parse(raw_songbook)
        self._set_songs_default()

    def _set_songs_default(self):
        """Set the default values for the Song() class."""
        Song.sort = self.config['sort']
        Song.prefixes = self.config['titleprefixwords']
        Song.authwords['after'] = [
                re.compile(r"^.*%s\b(.*)" % after)
                for after
                in self.config['authwords']["after"]
                ]
        Song.authwords['ignore'] = self.config['authwords']['ignore']
        Song.authwords['sep'] = [
                re.compile(r"^(.*)%s (.*)$" % sep)
                for sep
                in ([
                    " %s" % sep
                    for sep
                    in self.config['authwords']["sep"]
                    ] + [','])
                ]


    def _parse(self, raw_songbook):
        """Parse raw_songbook.

        The principle is: some special keys have their value processed; others
        are stored verbatim in self.config.
        """
        self.config.update(raw_songbook)

        ### Some post-processing
        # Compute song list
        if self.config['songs'] is None:
            self.config['songs'] = [
                    os.path.relpath(
                        filename,
                        os.path.join(self.config['datadir'], 'songs'),
                        )
                    for filename
                    in recursive_find(
                        os.path.join(self.config['datadir'], 'songs'),
                        '*.sg',
                        )
                    ]
        self.songslist = SongsList(self.config['datadir'], self.config["lang"])
        self.songslist.append_list(self.config['songs'])

        # Ensure self.config['authwords'] contains all entries
        for (key, value) in DEFAULT_AUTHWORDS.items():
            if key not in self.config['authwords']:
                self.config['authwords'][key] = value

    def write_tex(self, output):
        r"""Build the '.tex' file corresponding to self.

        Arguments:
        - output: a file object, in which the file will be written.


        TODO: Update this.

        Quelques notes concernant le rendu
        - self.config['titleprefixwords']
          > return EOL.join([
          >     r"\titleprefixwords{%s}" % prefix
          >     for prefix
          >     in self.config['titleprefixwords']
          >     ])

        - self.config['authwords']:
          > # Processing authwords values
          > tex = []
          > for key in ["after", "sep", "ignore"]:
          >     for word in self.config['authwords'][key]:
          >         if key == "after":
          >             tex.append(r"\auth%sword{%s}" % ("by", word))
          >         else:
          >             tex.append(r"\auth%sword{%s}" % (key, word))
          > return EOL.join(tex)

        - Liste des langues utilisées (pour chargement par babel):
          self.songlist.languages(). Donc la commande pour Babel peut
          ressembler à :
          > r"\PassOptionsToPackage{%s}{babel}" % ",".join(
          >     self.songslist.languages()
          >     )
        """
        parameters = parse_template(os.path.join(
            self.config['datadir'],
            'templates',
            self.config['template']
            ))
        output.write((
            '%% This file has been automatically '
            'generated, do not edit!\n'
            ))
        output.write(r'\makeatletter' + EOL)
        # output automatic parameters
        output.write(format_declaration("name", {"default": self.basename}))
        output.write(format_declaration("songslist", {"type": "stringlist"}))
        # output template parameter command
        for name, parameter in parameters.iteritems():
            output.write(format_declaration(name, parameter))
        # output template parameter values
        for name, value in self.config.iteritems():
            if name in parameters:
                output.write(format_definition(
                    name,
                    to_value(parameters[name], value),
                    ))

        if len(self.config['songs']) > 0:
            output.write(format_definition('songslist', self.songslist.latex()))
        output.write(r'\makeatother' + EOL)

        # output template
        comment_pattern = re.compile(r"^\s*%")
        with codecs.open(
                os.path.join(
                    self.config['datadir'],
                    'templates',
                    self.config['template']
                    ),
                'r',
                'utf-8',
                ) as template_file:
            content = [
                    line
                    for line
                    in template_file
                    if not comment_pattern.match(line)
                    ]

        output.write(u''.join(content))



def buildsongbook(
        raw_songbook,
        basename,
        interactive=False,
        logger=logging.getLogger()
        ):
    """Build a songbook

    Arguments:
    - raw_songbook: Python representation of the .sb songbook configuration
      file.
    - basename: basename of the songbook to be built.
    - interactive: in False, do not expect anything from stdin.
    """

    songbook = Songbook(raw_songbook, basename)
    with codecs.open("{}.tex".format(basename), 'w', 'utf-8') as output:
        songbook.write_tex(output)

    if not 'TEXINPUTS' in os.environ.keys():
        os.environ['TEXINPUTS'] = ''
    os.environ['TEXINPUTS'] += os.pathsep + os.path.join(
            __SHAREDIR__,
            'latex',
            )
    os.environ['TEXINPUTS'] += os.pathsep + os.path.join(
            songbook.config['datadir'],
            'latex',
            )

    # pdflatex options
    pdflatex_options = []
    pdflatex_options.append("--shell-escape") # Lilypond compilation
    if not interactive:
        pdflatex_options.append("-halt-on-error")

    # First pdflatex pass
    if subprocess.call(["pdflatex"] + pdflatex_options + [basename]):
        raise errors.LatexCompilationError(basename)

    # Make index
    sxd_files = glob.glob("%s_*.sxd" % basename)
    for sxd_file in sxd_files:
        logger.info("processing " + sxd_file)
        idx = process_sxd(sxd_file)
        index_file = open(sxd_file[:-3] + "sbx", "w")
        index_file.write(idx.entries_to_str().encode('utf8'))
        index_file.close()

    # Second pdflatex pass
    if subprocess.call(["pdflatex"] + pdflatex_options + [basename]):
        raise errors.LatexCompilationError(basename)

    # Cleaning
    clean(basename)
