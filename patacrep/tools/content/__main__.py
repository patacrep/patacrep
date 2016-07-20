"""Perform operations on songbook content."""

import argparse
import logging
import os
import sys
import textwrap
import yaml

from patacrep.songbook import open_songbook
from patacrep.build import Songbook
from .. import existing_file

LOGGER = logging.getLogger("patatools.content")

def commandline_parser():
    """Return a command line parser."""

    parser = argparse.ArgumentParser(
        prog="patatools content",
        description="Operations related to the content of a songbook.",
        formatter_class=argparse.RawTextHelpFormatter,
        )

    subparsers = parser.add_subparsers()
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
        type=existing_file,
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
    yaml_dir = os.path.dirname(os.path.abspath(namespace.songbook))
    ref_dir = os.path.join(yaml_dir, 'songs')
    content_items = [
        normalize_song_path(item.to_dict(), ref_dir)
        for item in content_items
    ]
    sys.stdout.write(yaml.safe_dump(content_items, allow_unicode=True, default_flow_style=False))

def normalize_song_path(file_entry, ref_dir):
    """Normalize the 'song' value, relative to ref_dir"""
    if 'song' in file_entry:
        file_entry['song'] = os.path.relpath(file_entry['song'], ref_dir)
    return file_entry

def main(args):
    """Main function: run from command line."""
    options = commandline_parser().parse_args(args[1:])
    options.command(options)

if __name__ == "__main__":
    main(sys.argv)
