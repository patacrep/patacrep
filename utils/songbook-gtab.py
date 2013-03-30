#!/usr/bin/python
# 

import sys
import re
from optparse import OptionParser
from utils.utils import recursiveFind

from utils.utils import recursiveFind

# Pattern set to ignore latex command in title prefix
gtabPattern = re.compile(r"\\gtab\{(.*)\}\{(.*)\}");

def main():
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("-o", "--output", dest="filename",
                      help="write result into FILE", metavar="FILE")
    (options, args) = parser.parse_args()

    # Options processing
    if options.filename:
        output = open(options.filename,"w")
    else:
        output = sys.stdout

    # Actual processing
    chords = dict()
    positions = dict()

    songfiles = recursiveFind(os.path.join(library, 'songs'), '*.sg')
    
    for file in songfiles:
        for line in open(file):
            result = gtabPattern.match(line)
            if result:
                (chord,position) = result.groups()
                if not chords.has_key(chord):
                    chords[chord] = set()
                chords[chord].add(position)
                if not positions.has_key(position):
                    positions[position] = set()
                positions[position].add(chord)

    document = [
        '\\documentclass{article}',        
        '\\usepackage[chorded]{songs}',
        '\\usepackage[utf8]{inputenc}',
        '\\title{Accords}',
        '\\author{Romain Goffe \\and Alexandre Dupas}',
        '\\date{}',
        '\\begin{document}',
        '\\maketitle',
        '\\begin{songs}{}', 
        ]

    document.append('\\section{Chords names}')

    chordskeys = chords.keys()
    chordskeys.sort()

    for k in chordskeys:
        document.append('\\subsection{'+k.replace('#','\\#').replace('&','\\&')+'}')
        for p in chords[k]:
            document.append('\\gtab{'+k+'}{'+p+'}')

    document.append('\\section{Chords names}')

    positionskeys = positions.keys()
    positionskeys.sort()

    for k in positionskeys:
        document.append('\\subsection{'+k+'}')
        for p in positions[k]:
            document.append('\\gtab{'+p+'}{'+k+'}')

    document.extend([
            '\\end{songs}',
            '\\end{document}',
            ])

    output.write('\n'.join(document))

if __name__ == '__main__':
    main()
