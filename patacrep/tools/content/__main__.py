"""Perform operations on songbook content."""

import argparse
import logging
import os
import shutil
import sys
import textwrap
import yaml

from patacrep import errors
from patacrep.songbook import open_songbook
from patacrep.build import Songbook

LOGGER = logging.getLogger("patatools.content")

def filename(name):
    """Check that argument is an existing, readable file name.

    Return the argument for convenience.
    """
    if os.path.isfile(name) and os.access(name, os.R_OK):
        return name
    raise argparse.ArgumentTypeError("Cannot read file '{}'.".format(name))

def commandline_parser():
    """Return a command line parser."""

    parser = argparse.ArgumentParser(
        prog="patatools content",
        description="Operations related to the content of a songbook.",
        formatter_class=argparse.RawTextHelpFormatter,
        )

    subparsers = parser.add_subparsers(
        description="",
        dest="command",
        )
    subparsers.required = True

    content_items = subparsers.add_parser(
        "items",
        description="Display the content items of a songbook.",
        help="Return the content items.",
        )
    content_items.add_argument(
        'songbook',
        metavar="SONGBOOK",
        help=textwrap.dedent("""Songbook file to be used to look for content items."""),
        type=filename,
        )
    content_items.set_defaults(command=do_content_items)

    return parser

def do_content_items(namespace):
    """Execute the `patatools content items` command."""
    config = open_songbook(namespace.songbook)
    config['_cache'] = True
    config['_error'] = "fix"
    songbook = Songbook(config, config['_outputname'])
    _, content_items = songbook.get_content_items()
    content_items = [item.file_entry() for item in content_items]
    print(yaml.safe_dump(content_items, allow_unicode=True, default_flow_style=False))

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
