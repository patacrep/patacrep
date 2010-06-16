#!/usr/bin/python
# -*- coding: utf-8 -*-
#

import getopt, sys
import os.path
import glob
import re
import json

def makeTexFile(songbook, output):
    name = output[:-4]

    # default value
    dir = ['img']
    template = "songbook.tmpl"
    songs = []
    booktype = ["chorded"]

    # parse the songbook data
    if "template" in songbook:
        template = songbook["template"]
    if "songs" in songbook:
        songs = songbook["songs"]
    if "booktype" in songbook:
        booktype = songbook["booktype"]

    # output relevant fields
    out = open(output, 'w')

    # output \template
    out.write('\\newcommand{\\template}{\n')
    for key in ["title", "author", "subtitle", "version", "mail", "picture", "picturecopyright", "footer", "licence"]:
        if key in songbook:
            out.write('  \\'+key+'{{{data}}}\n'.format(data=songbook[key]))
    out.write('}\n')
    # output \booktype
    out.write('\\newcommand{{\\booktype}}{{{data}}}'.format(data=','.join(booktype)))
    # output \songlist
    if not type(songs) is list:
        if songs == "all":
            l = glob.glob('songs/*/*.sg')
            l.sort()
            songs = map(lambda x: x[6:], l)
    if len(songs) > 0:
        out.write('\\newcommand{\\songslist}{\n')
        dir += map(os.path.dirname, map(lambda x:"songs/"+x, songs))
        dir = set(dir)
        out.write('  \\graphicspath{\n')
        for dirname in dir:
            out.write('    {{{imagedir}/}},\n'.format(imagedir=dirname))
        out.write('  }\n')
        for song in songs:
            out.write('  \\input{{songs/{songfile}}}\n'.format(songfile=song.strip()))
        out.write('}\n')
        tmpl = open("templates/"+template)
        out.write(tmpl.read().replace("SONGBOOKNAME", name+"_index"))
        tmpl.close()
        out.close()

def makeDepend(sb, output):
    name = output[:-2]

    # pattern that get dependencies
    dependsPattern = re.compile(r"^[^%]*(?:include|input)\{(.*?)\}")
    indexPattern = re.compile(r"^[^%]*\\(?:newauthor|new)index\{.*\}\{(.*?)\}")
    lilypondPattern = re.compile(r"^[^%]*\\(?:lilypond)\{(.*?)\}")

    # check for deps (in sb data)
    deps = []
    if type(sb["songs"]) is list:
        deps += map(lambda x: "songs/"+x, sb["songs"])
    for k in sb.keys():
        if not type(sb[k]) is list:
            match = dependsPattern.match(sb[k])
            if match:
                deps += [match.group(1)]

    # check for lilypond deps (in songs data) if necessary
    lilypond = []
    if "booktype" in sb.keys() and "lilypond" in sb["booktype"]:
        for filename in deps:
            tmpl = open(filename)
            for l in tmpl:
                match = lilypondPattern.match(l)
                if match:
                    lilypond.append(match.group(1))
            tmpl.close()

    # check for index (in template file)
    if "template" in sb:
        filename = "templates/"+sb["template"]
    else:
        filename = "templates/songbook.tmpl"
    idx = []
    tmpl = open(filename)
    for l in tmpl:
        match = indexPattern.match(l)
        if match:
            idx.append(match.group(1).replace("SONGBOOKNAME", name+"_index"))
    tmpl.close()

    # write .d file
    out = open(output, 'w')
    out.write('{0} {1} : {2}\n'.format(output, name+".tex", ' '.join(deps)))
    out.write('{0} : {1}\n'.format(name+".pdf", ' '.join(map(lambda x: x+".sbx",idx)+map(lambda x: "lilypond/"+x+".pdf", lilypond))))
    out.write('\t$(LATEX) {0}\n'.format(name+".tex"))
    out.write('{0} : {1}\n'.format(' '.join(map(lambda x: x+".sxd",idx)), name+".aux"))
    out.close()

def usage():
    print "No usage information yet."

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 
                                   "hs:o:d", 
                                   ["help","songbook=","output=","depend"])
    except getopt.GetoptError, err:
        # print help and exit
        print str(err)
        usage()
        sys.exit(2)

    songbook = None
    depend = False
    output = None

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-s", "--songbook"):
            songbook = a
        elif o in ("-d", "--depend"):
            depend = True
        elif o in ("-o", "--output"):
            output = a
        else:
            assert False, "unhandled option"

    if songbook and output:
        f = open(songbook)
        sb = json.load(f)
        f.close()

        if depend:
            makeDepend(sb, output)
        else:
            makeTexFile(sb, output)

if __name__ == '__main__':
    main()
