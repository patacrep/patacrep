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
import sys

from songbook import __SHAREDIR__
from songbook import errors
from songbook.files import recursiveFind
from songbook.index import processSXD
from songbook.songs import Song, SongsList

EOL = "\n"


def parseTemplate(template):
    """Return the list of parameters defined in the template."""
    embeddedJsonPattern = re.compile(r"^%%:")
    with open(template) as template_file:
        code = [
                line[3:-1]
                for line
                in template_file
                if embeddedJsonPattern.match(line)
                ]

    data = json.loads(''.join(code))
    parameters = dict()
    for param in data:
        parameters[param["name"]] = param
    return parameters


def toValue(parameter, data):
    if "type" not in parameter:
        return data
    elif parameter["type"] == "stringlist":
        if "join" in parameter:
            joinText = parameter["join"]
        else:
            joinText = ''
        return joinText.join(data)
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
            joinText = parameter["join"]
        else:
            joinText = ''
        return joinText.join(data)


def formatDeclaration(name, parameter):
    value = ""
    if "default" in parameter:
        value = parameter["default"]
    return (
            r'\def\set@{name}#1{{\def\get{name}{{#1}}}}'.format(name=name)
            + EOL
            + formatDefinition(name, toValue(parameter, value))
            )


def formatDefinition(name, value):
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


def makeTexFile(sb, output):
    """Create the LaTeX file corresponding to the .sb file given in argument."""
    datadir = sb['datadir']
    name = output[:-4]
    template_dir = os.path.join(datadir, 'templates')
    songs = []

    prefixes_tex = ""
    prefixes = []

    authwords_tex = ""
    authwords = {"after": ["by"], "ignore": ["unknown"], "sep": ["and"]}

    # parse the songbook data
    if "template" in sb:
        template = sb["template"]
        del sb["template"]
    else:
        template = os.path.join(__SHAREDIR__, "templates", "default.tmpl")
    if "songs" in sb:
        songs = sb["songs"]
        del sb["songs"]
    if "titleprefixwords" in sb:
        prefixes = sb["titleprefixwords"]
        for prefix in sb["titleprefixwords"]:
            prefixes_tex += r"\titleprefixword{%s}" % prefix + EOL
        sb["titleprefixwords"] = prefixes_tex
    if "authwords" in sb:
        # Populating default value
        for key in ["after", "sep", "ignore"]:
            if key not in sb["authwords"]:
                sb["authwords"][key] = authwords[key]
        # Processing authwords values
        authwords = sb["authwords"]
        for key in ["after", "sep", "ignore"]:
            for word in authwords[key]:
                if key == "after":
                    authwords_tex += r"\auth%sword{%s}" % ("by", word) + EOL
                else:
                    authwords_tex += r"\auth%sword{%s}" % (key, word) + EOL
        sb["authwords"] = authwords_tex
    if "after" in authwords:
        authwords["after"] = [re.compile(r"^.*%s\b(.*)" % after)
                              for after in authwords["after"]]
    if "sep" in authwords:
        authwords["sep"] = [" %s" % sep for sep in authwords["sep"]] + [","]
        authwords["sep"] = [re.compile(r"^(.*)%s (.*)$" % sep)
                            for sep in authwords["sep"]]

    if "lang" not in sb:
        sb["lang"] = "french"
    if "sort" in sb:
        sort = sb["sort"]
        del sb["sort"]
    else:
        sort = [u"by", u"album", u"@title"]
    Song.sort = sort
    Song.prefixes = prefixes
    Song.authwords = authwords

    parameters = parseTemplate(os.path.join(template_dir, template))

    # compute songslist
    if songs == "all":
        songs = [
                os.path.relpath(filename, os.path.join(datadir, 'songs'))
                for filename
                in recursiveFind(os.path.join(datadir, 'songs'), '*.sg')
                ]
    songslist = SongsList(datadir, sb["lang"])
    songslist.append_list(songs)

    sb["languages"] = ",".join(songslist.languages())

    # output relevant fields
    out = codecs.open(output, 'w', 'utf-8')
    out.write('%% This file has been automatically generated, do not edit!\n')
    out.write(r'\makeatletter' + EOL)
    # output automatic parameters
    out.write(formatDeclaration("name", {"default": name}))
    out.write(formatDeclaration("songslist", {"type": "stringlist"}))
    # output template parameter command
    for name, parameter in parameters.iteritems():
        out.write(formatDeclaration(name, parameter))
    # output template parameter values
    for name, value in sb.iteritems():
        if name in parameters:
            out.write(formatDefinition(name, toValue(parameters[name], value)))

    if len(songs) > 0:
        out.write(formatDefinition('songslist', songslist.latex()))
    out.write(r'\makeatother' + EOL)

    # output template
    commentPattern = re.compile(r"^\s*%")
    with codecs.open(
            os.path.join(template_dir, template), 'r', 'utf-8'
            ) as template_file:
        content = [
                line
                for line
                in template_file
                if not commentPattern.match(line)
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

def buildsongbook(sb, basename, interactive = False, logger = logging.getLogger()):
    """Build a songbook

    Arguments:
    - sb: Python representation of the .sb songbook configuration file.
    - basename: basename of the songbook to be built.
    - interactive: in False, do not expect anything from stdin.
    """

    texFile = basename + ".tex"

    # Make TeX file
    makeTexFile(sb, texFile)

    if not 'TEXINPUTS' in os.environ.keys():
        os.environ['TEXINPUTS'] = ''
    os.environ['TEXINPUTS'] += os.pathsep + os.path.join(__SHAREDIR__, 'latex')
    os.environ['TEXINPUTS'] += os.pathsep + os.path.join(sb['datadir'], 'latex')

    # pdflatex options
    pdflatex_options = []
    pdflatex_options.append("--shell-escape") # Lilypond compilation
    if not interactive:
        pdflatex_options.append("-halt-on-error")

    # First pdflatex pass
    if subprocess.call(["pdflatex"] + pdflatex_options + [texFile]):
        raise errors.LatexCompilationError(basename)

    # Make index
    sxdFiles = glob.glob("%s_*.sxd" % basename)
    for sxdFile in sxdFiles:
        logger.info("processing " + sxdFile)
        idx = processSXD(sxdFile)
        indexFile = open(sxdFile[:-3] + "sbx", "w")
        indexFile.write(idx.entriesToStr().encode('utf8'))
        indexFile.close()

    # Second pdflatex pass
    if subprocess.call(["pdflatex"] + pdflatex_options + [texFile]):
        raise errors.LatexCompilationError(basename)

    # Cleaning
    clean(basename)
