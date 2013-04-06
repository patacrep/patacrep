#!/usr/bin/python
# -*- coding: utf-8 -*-
#

import getopt, sys
import os.path
import locale
import platform
import shutil
import json
import re
from subprocess import call
from tools import recursiveFind
from index import *
from unidecode import unidecode
from utils.plastex import parsetex

class Song:
    #: Ordre de tri
    sort = []
    #: Préfixes à ignorer pour le tri
    prefixes = []

    def __init__(self, path, languages, titles, args):
        self.titles  = titles
        self.normalized_titles = [locale.strxfrm(unprefixed(unidecode(unicode(title, "utf-8")), self.prefixes)) for title in titles]
        self.args   = args
        self.path   = path
        self.languages = languages

    def __repr__(self):
        return repr((self.titles, self.args, self.path))

    def __cmp__(self, other):
        if not isinstance(other, Song):
            return NotImplemented
        for key in self.sort:
            if key == "@title":
                self_key = self.normalized_titles
                other_key = other.normalized_titles
            elif key == "@path":
                self.key = locale.strxfrm(self.path)
                other_key = locale.strxfrm(other.path)
            else:
                self_key = locale.strxfrm(self.args.get(key, ""))
                other_key = locale.strxfrm(other.args.get(key, ""))

            if self_key < other_key:
                return -1
            elif self_key > other_key:
                return 1
        return 0

def matchRegexp(reg, iterable):
    return [ m.group(1) for m in (reg.match(l) for l in iterable) if m ]

def unprefixed(title, prefixes):
    """Remove the first prefix of the list in the beginning of title (if any).
    """
    for prefix in prefixes:
        match = re.compile(r"^(%s)\b\s*(.*)$" % prefix).match(title)
        if match:
            return match.group(2)
    return title

class SongsList:
    """Manipulation et traitement de liste de chansons"""

    def __init__(self, library, language):
        self._library = library
        self._language = language

        # Liste triée des chansons
        self.songs = []


    def append(self, filename):
        """Ajout d'une chanson à la liste

        Effets de bord : analyse syntaxique plus ou moins sommaire du fichier
        pour en extraire et traiter certaines information (titre, langue,
        album, etc.).
        """
        path = os.path.join(self._library, 'songs', filename)
        # Exécution de PlasTeX
        data = parsetex(path)

        song = Song(path, data['languages'], data['titles'], data['args'])
        low, high = 0, len(self.songs)
        while low != high:
            middle = (low + high) / 2
            if song < self.songs[middle]:
                high = middle
            else:
                low = middle + 1
        self.songs.insert(low, song)

    def append_list(self, filelist):
        """Ajoute une liste de chansons à la liste

        L'argument est une liste de chaînes, représentant des noms de fichiers.
        """
        for filename in filelist:
            self.append(filename)

    def latex(self):
        """Renvoie le code LaTeX nécessaire pour intégrer la liste de chansons.
        """
        result = [ '\\input{{{0}}}'.format(song.path.replace("\\","/").strip()) for song in self.songs]
        result.append('\\selectlanguage{%s}' % self._language)
        return '\n'.join(result)

    def languages(self):
        """Renvoie la liste des langues utilisées par les chansons"""
        return set().union(*[set(song.languages) for song in self.songs])

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

def makeTexFile(sb, library, output):
    name = output[:-4]

    # default value
    template = "patacrep.tmpl"
    songs = []
    titleprefixwords = ""
    prefixes = []

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
            titleprefixwords += "\\titleprefixword{%s}\n" % prefix
        sb["titleprefixwords"] = titleprefixwords
    if "lang" not in sb:
        sb["lang"] = "french"
    if "sort" in sb:
        sort = sb["sort"]
        del sb["sort"]
    else:
        sort = [u"by", u"album", u"@title"]
    Song.sort = sort
    Song.prefixes = prefixes

    parameters = parseTemplate("templates/"+template)

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
    f = open("templates/"+template)
    content = [ line for line in f if not commentPattern.match(line) ]

    for index, line in enumerate(content):
        if re.compile("getLibraryImgDirectory").search(line):
            line = line.replace("\\getLibraryImgDirectory", library + "img/")
            content[index] = line
        if re.compile("getLibraryLilypondDirectory").search(line):
            line = line.replace("\\getLibraryLilypondDirectory", library + "lilypond/")
            content[index] = line

    f.close()
    out.write(''.join(content))

    out.close()

def makeDepend(sb, library, output):
    name = output[:-2]

    indexPattern = re.compile(r"^[^%]*\\(?:newauthor|new)index\{.*\}\{(.*?)\}")
    lilypondPattern = re.compile(r"^[^%]*\\(?:lilypond)\{(.*?)\}")

    # check for deps (in sb data)
    deps = [];
    if sb["songs"] == "all":
        deps += recursiveFind(os.path.join(library, 'songs'), '*.sg')
    else:
        deps += map(lambda x: library + "songs/" + x, sb["songs"])

    # check for lilypond deps (in songs data) if necessary
    lilypond = []
    if "bookoptions" in sb and "lilypond" in sb["bookoptions"]:
        for filename in deps:
            tmpl = open(filename)
            lilypond += matchRegexp(lilypondPattern, tmpl)
            tmpl.close()

    # check for index (in template file)
    if "template" in sb:
        filename = sb["template"]
    else:
        filename = "patacrep.tmpl"
    tmpl = open("templates/"+filename)
    idx = map(lambda x: x.replace("\getname", name), matchRegexp(indexPattern, tmpl))
    tmpl.close()

    # write .d file
    out = open(output, 'w')
    out.write('{0} {1} : {2}\n'.format(output, name+".tex", ' '.join(deps)))
    out.write('{0} : {1}\n'.format(name+".pdf", ' '.join(map(lambda x: x+".sbx",idx)+map(lambda x: library+"lilypond/"+x+".pdf", lilypond))))
    out.write('\t$(LATEX) {0}\n'.format(name+".tex"))
    out.write('{0} : {1}\n'.format(' '.join(map(lambda x: x+".sxd",idx)), name+".aux"))
    out.close()

def usage():
    print "No usage information yet."

def main():
    locale.setlocale(locale.LC_ALL, '') # set script locale to match user's
    try:
        opts, args = getopt.getopt(sys.argv[1:], 
                                   "hs:l:",
                                   ["help","songbook=","library="])
    except getopt.GetoptError, err:
        # print help and exit
        print str(err)
        usage()
        sys.exit(2)

    sbFile = None
    library = './'

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-s", "--songbook"):
            sbFile = a
        elif o in ("-l", "--library"):
            if not a.endswith('/'):
                a += '/'
            library = a
        else:
            assert False, "unhandled option"

    basename = os.path.basename(sbFile)[:-3]
    texFile  = basename + ".tex"
    pdfFile  = basename + ".pdf"
    
    f = open(sbFile)
    sb = json.load(f)
    f.close()

    # Make TeX file
    makeTexFile(sb, library, texFile)

    # First pdflatex pass
    call(["pdflatex", texFile])

    # Make index
    sxdFiles = recursiveFind(".", basename + "*.sxd")
    print sxdFiles
    for sxdFile in sxdFiles:
        print "processing " + sxdFile
        idx = processSXD(sxdFile)
        indexFile = open(sxdFile[:-3]+"sbx", "w")
        indexFile.write(idx.entriesToStr())
        indexFile.close()

    # Second pdflatex pass
    call(["pdflatex", texFile])

if __name__ == '__main__':
    main()
