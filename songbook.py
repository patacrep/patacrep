#!/usr/bin/python
# -*- coding: utf-8 -*-
#

import argparse
import json
import locale
import os.path
import textwrap
import sys

from songbook.build import buildsongbook
from songbook import __VERSION__

def argument_parser(args):
    parser = argparse.ArgumentParser(description="A song book compiler")

    parser.add_argument('--version', help='Show version', action='version',
            version='%(prog)s ' + __VERSION__)

    parser.add_argument('book', nargs=1, help=textwrap.dedent("""\
                    Book to compile.
            """))

    parser.add_argument('--datadir', '-d', nargs=1, type=str, action='store', default=".",
            help=textwrap.dedent("""\
                    Data location. Expected (not necessarily required) subdirectories are 'songs', 'img', 'latex', 'templates'.
            """))

    options = parser.parse_args(args)

    return options

def main():
    locale.setlocale(locale.LC_ALL, '') # set script locale to match user's

    options = argument_parser(sys.argv[1:])

    sbFile = options.book[0]

    basename = os.path.basename(sbFile)[:-3]

    f = open(sbFile)
    sb = json.load(f)
    f.close()

    if 'datadir' in sb.keys():
        if not os.path.isabs(sb['datadir']):
            sb['datadir'] = os.path.join(os.path.dirname(sbFile), sb['datadir'])
    else:
        sb['datadir'] = options.datadir
    buildsongbook(sb, basename)

if __name__ == '__main__':
    main()
