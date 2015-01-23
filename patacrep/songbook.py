"""Command line tool to compile songbooks using the songbook library."""

import argparse
import json
import locale
import logging
import os.path
import textwrap
import sys

from patacrep.build import SongbookBuilder, DEFAULT_STEPS
from patacrep import __version__
from patacrep import errors
import patacrep.encoding

# Logging configuration
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()

# pylint: disable=too-few-public-methods
class ParseStepsAction(argparse.Action):
    """Argparse action to split a string into a list."""
    def __call__(self, __parser, namespace, values, __option_string=None):
        if not getattr(namespace, self.dest):
            setattr(namespace, self.dest, [])
        setattr(
                namespace,
                self.dest,
                (
                    getattr(namespace, self.dest)
                    + [value.strip() for value in values[0].split(',')]
                    ),
                )

class VerboseAction(argparse.Action):
    """Set verbosity level with option --verbose."""
    def __call__(self, *_args, **_kwargs):
        LOGGER.setLevel(logging.DEBUG)

def argument_parser(args):
    """Parse arguments"""
    parser = argparse.ArgumentParser(description="A song book compiler")

    parser.add_argument('--version', help='Show version', action='version',
            version='%(prog)s ' + __version__)

    parser.add_argument('book', nargs=1, help=textwrap.dedent("""\
                    Book to compile.
            """))

    parser.add_argument('--datadir', '-d', nargs='+', type=str, action='append',
            help=textwrap.dedent("""\
                    Data location. Expected (not necessarily required)
                    subdirectories are 'songs', 'img', 'latex', 'templates'.
            """))

    parser.add_argument('--verbose', '-v', nargs=0, action=VerboseAction,
            help=textwrap.dedent("""\
                    Show details about the compilation process.
            """))

    parser.add_argument('--steps', '-s', nargs=1, type=str,
            action=ParseStepsAction,
            help=textwrap.dedent("""\
                    Steps to run. Default is "{steps}".
                    Available steps are:
                    "tex" produce .tex file from templates;
                    "pdf" compile .tex file;
                    "sbx" compile index files;
                    "clean" remove temporary files;
                    any string beginning with '%%' (in this case, it will be run
                    in a shell). Several steps (excepted the custom shell
                    command) can be combinend in one --steps argument, as a
                    comma separated string.
            """.format(steps=','.join(DEFAULT_STEPS))),
            default=None,
            )

    options = parser.parse_args(args)

    return options


def main():
    """Main function:"""

    # set script locale to match user's
    try:
        locale.setlocale(locale.LC_ALL, '')
    except locale.Error as error:
        # Locale is not installed on user's system, or wrongly configured.
        LOGGER.error("Locale error: {}\n".format(str(error)))

    options = argument_parser(sys.argv[1:])

    songbook_path = options.book[0]

    basename = os.path.basename(songbook_path)[:-3]

    try:
        with patacrep.encoding.open_read(songbook_path) as songbook_file:
            songbook = json.load(songbook_file)
        if 'encoding' in songbook:
            with patacrep.encoding.open_read(
                    songbook_path,
                    encoding=songbook['encoding']
                    ) as songbook_file:
                songbook = json.load(songbook_file)
    except Exception as error: # pylint: disable=broad-except
        LOGGER.error(error)
        LOGGER.error("Error while loading file '{}'.".format(songbook_path))
        sys.exit(1)

    # Gathering datadirs
    datadirs = []
    if options.datadir:
        # Command line options
        datadirs += [item[0] for item in options.datadir]
    if 'datadir' in songbook:
        # .sg file
        if isinstance(songbook['datadir'], str):
            songbook['datadir'] = [songbook['datadir']]
        datadirs += [
                os.path.join(
                    os.path.dirname(os.path.abspath(songbook_path)),
                    path
                    )
                for path in songbook['datadir']
                ]
    # Default value
    datadirs.append(os.path.dirname(os.path.abspath(songbook_path)))

    songbook['datadir'] = datadirs

    try:
        sb_builder = SongbookBuilder(songbook, basename)
        sb_builder.unsafe = True

        sb_builder.build_steps(options.steps)
    except errors.SongbookError as error:
        LOGGER.error(error)
        if LOGGER.level >= logging.INFO:
            LOGGER.error(
                    "Running again with option '-v' may give more information."
                    )
        sys.exit(1)
    except KeyboardInterrupt:
        LOGGER.warning("Aborted by user.")
        sys.exit(1)

    sys.exit(0)

if __name__ == '__main__':
    main()
