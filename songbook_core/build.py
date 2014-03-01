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

from songbook_core import __DATADIR__
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
    """Convert 'data' to a LaTeX string.

    Conversion is done according to the template parameter it corresponds to.
    """
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
    """Write LaTeX code to declare a variable"""
    value = ""
    if "default" in parameter:
        value = parameter["default"]
    return (
            r'\def\set@{name}#1{{\def\get{name}{{#1}}}}'.format(name=name)
            + EOL
            + format_definition(name, to_value(parameter, value))
            )


def format_definition(name, value):
    """Write LaTeX code to set a value to a variable"""
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


def make_tex_file(songbook, output):
    """Create the LaTeX file corresponding to the .sb file given in argument."""
    datadir = songbook['datadir']
    name = output[:-4]
    template_dir = os.path.join(datadir, 'templates')
    songs = []

    prefixes_tex = ""
    prefixes = []

    authwords_tex = ""
    authwords = {"after": ["by"], "ignore": ["unknown"], "sep": ["and"]}

    # parse the songbook data
    if "template" in songbook:
        template = songbook["template"]
        del songbook["template"]
    else:
        template = os.path.join(__DATADIR__, "templates", "default.tmpl")
    if "songs" in songbook:
        songs = songbook["songs"]
        del songbook["songs"]
    if "titleprefixwords" in songbook:
        prefixes = songbook["titleprefixwords"]
        for prefix in songbook["titleprefixwords"]:
            prefixes_tex += r"\titleprefixword{%s}" % prefix + EOL
        songbook["titleprefixwords"] = prefixes_tex
    if "authwords" in songbook:
        # Populating default value
        for key in ["after", "sep", "ignore"]:
            if key not in songbook["authwords"]:
                songbook["authwords"][key] = authwords[key]
        # Processing authwords values
        authwords = songbook["authwords"]
        for key in ["after", "sep", "ignore"]:
            for word in authwords[key]:
                if key == "after":
                    authwords_tex += r"\auth%sword{%s}" % ("by", word) + EOL
                else:
                    authwords_tex += r"\auth%sword{%s}" % (key, word) + EOL
        songbook["authwords"] = authwords_tex
    if "after" in authwords:
        authwords["after"] = [re.compile(r"^.*%s\b(.*)" % after)
                              for after in authwords["after"]]
    if "sep" in authwords:
        authwords["sep"] = [" %s" % sep for sep in authwords["sep"]] + [","]
        authwords["sep"] = [re.compile(r"^(.*)%s (.*)$" % sep)
                            for sep in authwords["sep"]]

    if "lang" not in songbook:
        songbook["lang"] = "french"
    if "sort" in songbook:
        sort = songbook["sort"]
        del songbook["sort"]
    else:
        sort = [u"by", u"album", u"@title"]
    Song.sort = sort
    Song.prefixes = prefixes
    Song.authwords = authwords

    parameters = parse_template(os.path.join(template_dir, template))

    # compute songslist
    if songs == "all":
        songs = [
                os.path.relpath(filename, os.path.join(datadir, 'songs'))
                for filename
                in recursive_find(os.path.join(datadir, 'songs'), '*.sg')
                ]
    songslist = SongsList(datadir, songbook["lang"])
    songslist.append_list(songs)

    songbook["languages"] = ",".join(songslist.languages())

    # output relevant fields
    out = codecs.open(output, 'w', 'utf-8')
    out.write('%% This file has been automatically generated, do not edit!\n')
    out.write(r'\makeatletter' + EOL)
    # output automatic parameters
    out.write(format_declaration("name", {"default": name}))
    out.write(format_declaration("songslist", {"type": "stringlist"}))
    # output template parameter command
    for name, parameter in parameters.iteritems():
        out.write(format_declaration(name, parameter))
    # output template parameter values
    for name, value in songbook.iteritems():
        if name in parameters:
            out.write(format_definition(
                name,
                to_value(parameters[name], value),
                ))

    if len(songs) > 0:
        out.write(format_definition('songslist', songslist.latex()))
    out.write(r'\makeatother' + EOL)

    # output template
    comment_pattern = re.compile(r"^\s*%")
    with codecs.open(
            os.path.join(template_dir, template), 'r', 'utf-8'
            ) as template_file:
        content = [
                line
                for line
                in template_file
                if not comment_pattern.match(line)
                ]

        for index, line in enumerate(content):
            if re.compile("getDataImgDirectory").search(line):
                if os.path.abspath(os.path.join(datadir, "img")).startswith(
                        os.path.abspath(os.path.dirname(output))
                        ):
                    imgdir = os.path.relpath(
                            os.path.join(datadir, "img"),
                            os.path.dirname(output)
                            )
                else:
                    imgdir = os.path.abspath(os.path.join(datadir, "img"))
                line = line.replace(r"\getDataImgDirectory", ' {%s/} ' % imgdir)
                content[index] = line

    out.write(u''.join(content))
    out.close()

def buildsongbook(
        songbook,
        basename,
        interactive=False,
        logger=logging.getLogger()
        ):
    """Build a songbook

    Arguments:
    - songbook: Python representation of the .sb songbook configuration file.
    - basename: basename of the songbook to be built.
    - interactive: in False, do not expect anything from stdin.
    """

    tex_file = basename + ".tex"

    # Make TeX file
    make_tex_file(songbook, tex_file)

    if not 'TEXINPUTS' in os.environ.keys():
        os.environ['TEXINPUTS'] = ''
    os.environ['TEXINPUTS'] += os.pathsep + os.path.join(
            __DATADIR__,
            'latex',
            )
    os.environ['TEXINPUTS'] += os.pathsep + os.path.join(
            songbook['datadir'],
            'latex',
            )

    # pdflatex options
    pdflatex_options = []
    pdflatex_options.append("--shell-escape") # Lilypond compilation
    if not interactive:
        pdflatex_options.append("-halt-on-error")

    # First pdflatex pass
    if subprocess.call(["pdflatex"] + pdflatex_options + [tex_file]):
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
    if subprocess.call(["pdflatex"] + pdflatex_options + [tex_file]):
        raise errors.LatexCompilationError(basename)

    # Cleaning
    clean(basename)
