#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import call
import glob
import json
import os.path
import re

from songbook.files import recursiveFind
from songbook.index import processSXD
from songbook.songs import Song, SongsList

def parseTemplate(template):
    embeddedJsonPattern = re.compile(r"^%%:")
    f = open(template)
    code = [ line[3:-1] for line in f if embeddedJsonPattern.match(line) ]
    f.close()
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
        return data+'pt'
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
    return '\\def\\set@{name}#1{{\\def\\get{name}{{#1}}}}\n'.format(name=name) + formatDefinition(name, toValue(parameter, value))

def formatDefinition(name, value):
    return '\\set@{name}{{{value}}}\n'.format(name=name, value=value)

def makeTexFile(sb, library, output, core_dir):
    name = output[:-4]
    template_dir = core_dir+'templates/'
    # default value
    template = "patacrep.tmpl"
    songs = []

    prefixes_tex = ""
    prefixes = []

    authwords_tex = ""
    authwords = {"after": ["by"], "ignore": ["unknown"], "sep": ["and"]}
    
    # parse the songbook data
    if "template" in sb:
        template = sb["template"]
        del sb["template"]
    if "songs" in sb:
        songs = sb["songs"]
        del sb["songs"]
    if "titleprefixwords" in sb:
        prefixes = sb["titleprefixwords"]
        for prefix in sb["titleprefixwords"]:
            prefixes_tex += "\\titleprefixword{%s}\n" % prefix
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
                    authwords_tex += "\\auth%sword{%s}\n" % ("by", word)
                else:
                    authwords_tex += "\\auth%sword{%s}\n" % (key, word)
        sb["authwords"] = authwords_tex
    if "after" in authwords:
        authwords["after"] = [re.compile(r"^.*%s\b(.*)" % after) for after in authwords["after"]]
    if "sep" in authwords:
        authwords["sep"] = [" %s" % sep for sep in authwords["sep"]] + [","]
        authwords["sep"] = [re.compile(r"^(.*)%s (.*)$" % sep) for sep in authwords["sep"] ]

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

    parameters = parseTemplate(template_dir+template)

    # compute songslist
    if songs == "all":
        songs = map(lambda x: x[len(library) + 6:], recursiveFind(os.path.join(library, 'songs'), '*.sg'))
    songslist = SongsList(library, sb["lang"])
    songslist.append_list(songs)

    sb["languages"] = ",".join(songslist.languages())

    # output relevant fields
    out = open(output, 'w')
    out.write('%% This file has been automatically generated, do not edit!\n')
    out.write('\\makeatletter\n')
    # output automatic parameters
    out.write(formatDeclaration("name", {"default":name}))
    out.write(formatDeclaration("songslist", {"type":"stringlist"}))
    # output template parameter command
    for name, parameter in parameters.iteritems():
        out.write(formatDeclaration(name, parameter))
    # output template parameter values
    for name, value in sb.iteritems():
        if name in parameters:
            out.write(formatDefinition(name, toValue(parameters[name],value)))

    if len(songs) > 0:
        out.write(formatDefinition('songslist', songslist.latex()))
    out.write('\\makeatother\n')

    # output template
    commentPattern = re.compile(r"^\s*%")
    with open(template_dir+template) as f:
        content = [ line for line in f if not commentPattern.match(line) ]

        for index, line in enumerate(content):
            if re.compile("getLibraryImgDirectory").search(line):
                line = line.replace("\\getLibraryImgDirectory", core_dir + "img/")
                content[index] = line

    out.write(''.join(content))
    out.close()

def buildsongbook(sb, basename, library):
    """Build a songbook

    Arguments:
    - sb: Python representation of the .sb songbook configuration file.
    - library: directory containing the "songs" directory, itself containing
      songs.
    - basename: basename of the songbook to be built.
    """

    MOD_DIR = os.path.dirname(os.path.abspath(__file__))
    CORE_DIR = MOD_DIR + '/../'

    texFile  = basename + ".tex"

    # Make TeX file
    makeTexFile(sb, library, texFile, CORE_DIR)
    
    os.environ['TEXMFHOME'] = MOD_DIR + '/../'
    # First pdflatex pass
    if call(["pdflatex", "--shell-escape", texFile]):
        sys.exit(1)

    # Make index
    sxdFiles = glob.glob("%s_*.sxd" % basename)
    for sxdFile in sxdFiles:
        print "processing " + sxdFile
        idx = processSXD(sxdFile)
        indexFile = open(sxdFile[:-3]+"sbx", "w")
        indexFile.write(idx.entriesToStr().encode('utf8'))
        indexFile.close()

    # Second pdflatex pass
    if call(["pdflatex", "--shell-escape", texFile]):
        sys.exit(1)
