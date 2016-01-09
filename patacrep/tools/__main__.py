#!/bin/env python3

"""Command line client to :mod:`tools`"""

import argparse
import logging
import operator
import os
import pkgutil
import re
import sys

import patacrep

# Logging configuration
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()

def _execlp(program, args):
    """Call :func:`os.execlp`, adding `program` as the first argument to itself."""
    return os.execlp(program, program, *args)

def _iter_subcommands():
    """Iterate over subcommands.

    The objects returned are tuples of:
    - the name of the command;
    - its description;
    - the function to call to execute the subcommand.
    """
    subcommands = []

    # Get python subcommands
    path = [os.path.join(item, "patacrep", "tools") for item in sys.path]
    prefix = "patacrep.tools."
    module_re = re.compile(r'{}(?P<subcommand>[^\.]*)\.__main__'.format(prefix))
    for module_loader, name, _ in pkgutil.walk_packages(path, prefix):
        match = module_re.match(name)
        if match:
            module = module_loader.find_module(match.string).load_module()
            if hasattr(module, "SUBCOMMAND_DESCRIPTION"):
                subcommands.append(match.groupdict()['subcommand'])
                yield (
                    match.groupdict()['subcommand'],
                    getattr(module, "SUBCOMMAND_DESCRIPTION"),
                    module.main,
                    )

class ArgumentParser(argparse.ArgumentParser):
    """Proxy class to circumvent an :mod:`argparse` bug.

    Contrarily to what documented, the `argparse.REMAINDER
    <https://docs.python.org/3/library/argparse.html#nargs>`_ `nargs` setting
    does not include the remainder arguments if the first one begins with `-`.

    This bug is reperted as `17050 <https://bugs.python.org/issue17050>`_. This
    class can be deleted once this bug has been fixed.
    """

    def parse_args(self, args=None, namespace=None):
        if args is None:
            args = sys.argv[1:]
        subcommands = [command[0] for command in set(_iter_subcommands())]
        if len(args) > 0:
            if args[0] in subcommands:
                args = [args[0], "--"] + args[1:]

        value = super().parse_args(args, namespace)

        if hasattr(value, 'remainder'):
            value.remainder = value.remainder[1:]
        return value


def commandline_parser():
    """Return a command line parser."""

    parser = ArgumentParser(
        prog="patatools",
        description=(
            "Miscellaneous tools for patacrep."
            ),
        formatter_class=argparse.RawTextHelpFormatter,
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

    for command, message, function in sorted(_iter_subcommands(), key=operator.itemgetter(0)):
        sub1 = subparsers.add_parser(command, help=message, add_help=False)
        sub1.add_argument('remainder', nargs=argparse.REMAINDER)
        sub1.set_defaults(function=function)

    return parser

def main():
    """Main function"""

    parser = commandline_parser()
    args = parser.parse_args()
    if hasattr(args, "function"):
        args.function(args.remainder)
    else:
        parser.error("Missing command.")

if __name__ == "__main__":
    main()
