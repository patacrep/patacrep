#!/usr/bin/python
# -*- coding: utf-8 -*-
#

"""Command line tool to compile songbooks using the songbook library."""

import argparse
import json
import locale
import logging
import os.path
import textwrap
import sys

from songbook.build import buildsongbook
from songbook import __VERSION__
from songbook import errors


def argument_parser(args):
    """Parse argumnts"""
    parser = argparse.ArgumentParser(description="A song book compiler")

    parser.add_argument('--version', help='Show version', action='version',
            version='%(prog)s ' + __VERSION__)

    parser.add_argument('book', nargs=1, help=textwrap.dedent("""\
                    Book to compile.
            """))

    parser.add_argument('--datadir', '-d', nargs=1, type=str, action='store',
            help=textwrap.dedent("""\
                    Data location. Expected (not necessarily required)
                    subdirectories are 'songs', 'img', 'latex', 'templates'.
            """))

    options = parser.parse_args(args)

    return options


def main():
    """Main function:"""

    # Logging configuration
    logging.basicConfig(name = 'songbook')
    logger = logging.getLogger('songbook')

    # set script locale to match user's
    try:
        locale.setlocale(locale.LC_ALL, '')
    except locale.Error as error:
        # Locale is not installed on user's system, or wrongly configured.
        sys.stderr.write("Locale error: {}\n".format(error.message))

    options = argument_parser(sys.argv[1:])

    songbook_path = options.book[0]

    basename = os.path.basename(songbook_path)[:-3]

    with open(songbook_path) as songbook_file:
        songbook = json.load(songbook_file)

    if options.datadir is not None:
        songbook['datadir'] = options.datadir[0]
    elif 'datadir' in songbook.keys():
        if not os.path.isabs(songbook['datadir']):
            songbook['datadir'] = os.path.join(os.path.dirname(songbook_path),
                                               songbook['datadir']
                                               )
    else:
        songbook['datadir'] = os.path.dirname(songbook_path)
    try:
        buildsongbook(songbook, basename, interactive = True, logger = logger)
    except errors.SongbookError as error:
        logger.error(error)
        sys.exit(1)

    sys.exit(0)

if __name__ == '__main__':
    main()
