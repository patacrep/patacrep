"""Command line tool to compile songbooks using the songbook library."""

import argparse
import locale
import logging
import sys
import textwrap

from patacrep.build import SongbookBuilder, DEFAULT_STEPS
from patacrep.utils import yesno
from patacrep import __version__
from patacrep import errors
from patacrep.songbook import open_songbook

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

def yesno_type(string):
    """Interpret argument as a "yes" or a "no".

    Raise `argparse.ArgumentTypeError` if string cannot be analysed.
    """
    try:
        return yesno(string)
    except ValueError as error:
        raise argparse.ArgumentTypeError(str(error))

def argument_parser(args):
    """Parse arguments"""
    parser = argparse.ArgumentParser(
        prog="songbook",
        description="A song book compiler",
        formatter_class=argparse.RawTextHelpFormatter,
        )

    parser.add_argument(
        '--version', help='Show version', action='version',
        version='%(prog)s ' + __version__,
        )

    parser.add_argument(
        'book', nargs=1, help=textwrap.dedent("Book to compile.")
        )

    parser.add_argument(
        '--datadir', '-d', nargs='+', type=str, action='append',
        help=textwrap.dedent("""\
                Data location. Expected (not necessarily required) subdirectories are 'songs', 'img', 'latex', 'templates'.
        """),
        )

    parser.add_argument(
        '--verbose', '-v', nargs=0, action=VerboseAction,
        help=textwrap.dedent("""\
                Show details about the compilation process.
        """)
        )

    parser.add_argument(
        '--cache', '-c', nargs=1,
        help=textwrap.dedent("""\
                Enable song cache.
        """),
        type=yesno_type,
        default=[True],
        )

    parser.add_argument(
        '--error', '-e', nargs=1,
        help=textwrap.dedent("""\
                By default, this program tries hard to fix or ignore song and book errors. This option changes this behaviour:
                - failonsong: stop as soon as a song contains (at least) one error;
                - failonbook: stop when all the songs have been parsed and rendered, if any error was met;
                - fix: tries to fix (or ignore) errors.

                Note that compilation *may* fail even with `--error=fix`.
        """),
        type=str,
        choices=[
            "failonsong",
            "failonbook",
            "fix",
        ],
        default=["fix"],
        )

    parser.add_argument(
        '--steps', '-s', nargs=1, type=str,
        action=ParseStepsAction,
        help=textwrap.dedent("""\
                Steps to run. Default is "{steps}".  Available steps are:
                - "tex" produce .tex file from templates;
                - "pdf" compile .tex file;
                - "sbx" compile index files;
                - "clean" remove temporary files;
                - any string beginning with '#' (in this case, it will be run in a shell).
                Several steps (excepted the custom shell command) can be combinend in one --steps argument, as a comma separated string.

                Substring {{basename}} is replaced by the basename of the song book, and substrings {{aux}}, {{log}}, {{out}}, {{pdf}}, {{sxc}}, {{tex}} are replaced by "<BASENAME>.aux", "<BASENAME>.log", and so on.
        """.format(steps=','.join(DEFAULT_STEPS))),
        default=None,
        )

    options = parser.parse_args(args)

    return options


def main(args=None):
    """Main function:"""
    if args is None:
        args = sys.argv

    # set script locale to match user's
    try:
        locale.setlocale(locale.LC_ALL, '')
    except locale.Error as error:
        # Locale is not installed on user's system, or wrongly configured.
        LOGGER.error("Locale error: {}\n".format(str(error)))

    options = argument_parser(args[1:])

    songbook_path = options.book[-1]

    # Load the user songbook config
    try:
        songbook = open_songbook(songbook_path)

        # Command line options
        if options.datadir:
            for datadir in reversed(options.datadir):
                songbook['datadir'].insert(0, datadir)
        songbook['_cache'] = options.cache[0]
        songbook['_error'] = options.error[0]

        sb_builder = SongbookBuilder(songbook)
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
