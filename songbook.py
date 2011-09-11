#!/usr/bin/python
# -*- coding: utf-8 -*-
#

import getopt, sys
import os.path
import glob
import re
import json

def matchRegexp(reg, iterable):
    return [ m.group(1) for m in (reg.match(l) for l in iterable) if m ]

def songslist(songs):
    directories = set(["img/"] + map(lambda x: "songs/" + os.path.dirname(x), songs))
    result = ['\\graphicspath{'] + [ '  {{{0}/}},'.format(d) for d in directories ] + ['}'] + [ '\\input{{songs/{0}}}'.format(s.strip()) for s in songs ]
    return '\n'.join(result)

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

def makeTexFile(sb, output):
    name = output[:-4]

    # default value
    template = "patacrep.tmpl"
    songs = []

    # parse the songbook data
    if "template" in sb:
        template = sb["template"]
        del sb["template"]
    if "songs" in sb:
        songs = sb["songs"]
        del sb["songs"]

    parameters = parseTemplate("templates/"+template)

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
    # output songslist
    if songs == "all":
        songs = map(lambda x: x[6:], glob.glob('songs/*/*.sg'))
        songs.sort()
    if len(songs) > 0:
        out.write(formatDefinition('songslist', songslist(songs)))
    out.write('\\makeatother\n')

    # output template
    commentPattern = re.compile(r"^\s*%")
    f = open("templates/"+template)
    content = [ line for line in f if not commentPattern.match(line) ]
    f.close()
    out.write(''.join(content))
    out.close()

def makeDepend(sb, output):
    name = output[:-2]

    dependsPattern = re.compile(r"^[^%]*(?:include|input)\{(.*?)\}")
    indexPattern = re.compile(r"^[^%]*\\(?:newauthor|new)index\{.*\}\{(.*?)\}")
    lilypondPattern = re.compile(r"^[^%]*\\(?:lilypond)\{(.*?)\}")

    # check for deps (in sb data)
    deps = matchRegexp(dependsPattern, [ v for v in sb.itervalues() if type(v) is not list ])
    if sb["songs"] == "all":
        deps += glob.glob('songs/*/*.sg')
    else:
        deps += map(lambda x: "songs/" + x, sb["songs"])

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
