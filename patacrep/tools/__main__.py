#!/bin/env python3

"""Command line client to :mod:`tools`"""

import logging
import sys

import argdispatch

import patacrep

# Logging configuration
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("patatools")

def commandline_parser():
    """Return a command line parser."""

    parser = argdispatch.ArgumentParser(
        prog="patatools",
        description=(
            "Miscellaneous tools for patacrep."
            ),
        formatter_class=argdispatch.RawTextHelpFormatter,
        )

    parser.add_argument(
        '--version',
        help='Show version',
        action='version',
        version='%(prog)s ' + patacrep.__version__
        )

    subparsers = parser.add_subparsers(
        title="Subcommands",
        description="List of available subcommands.",
        )
    subparsers.required = True
    subparsers.dest = "subcommand"
    subparsers.add_submodules("patacrep.tools")

    return parser

def main(args=None):
    """Main function"""
    if args is None:
        args = sys.argv
    commandline_parser().parse_args(args[1:])

if __name__ == "__main__":
    main()
