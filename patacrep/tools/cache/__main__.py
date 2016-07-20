"""Perform operations on cache."""

import argparse
import logging
import os
import shutil
import sys
import textwrap

from patacrep import errors
from patacrep.songbook import open_songbook
from .. import existing_file

LOGGER = logging.getLogger("patatools.cache")

def commandline_parser():
    """Return a command line parser."""

    parser = argparse.ArgumentParser(
        prog="patatools cache",
        description="Clean the caches related to a songbook.",
        formatter_class=argparse.RawTextHelpFormatter,
        )

    subparsers = parser.add_subparsers()
    subparsers.required = True

    clean = subparsers.add_parser(
        "clean",
        description="Delete cache.",
        help="Delete cache.",
        )
    clean.add_argument(
        'songbook',
        metavar="SONGBOOK",
        help=textwrap.dedent("""Songbook file to be used to look for cache path."""),
        type=existing_file,
        )
    clean.set_defaults(command=do_clean)

    return parser

def do_clean(namespace):
    """Execute the `patatools cache clean` command."""
    for datadir in open_songbook(namespace.songbook)['_datadir']:
        cachedir = os.path.join(datadir, ".cache")
        LOGGER.info("Deleting cache directory '{}'...".format(cachedir))
        if os.path.isdir(cachedir):
            shutil.rmtree(cachedir)

def main(args):
    """Main function: run from command line."""
    options = commandline_parser().parse_args(args[1:])
    try:
        options.command(options)
    except errors.SongbookError as error:
        LOGGER.error(str(error))
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv)
