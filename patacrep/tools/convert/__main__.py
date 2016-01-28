"""`patatools.convert` command: convert between song formats"""

import os
import logging
import sys

from patacrep import files
from patacrep.songs import DEFAULT_CONFIG
from patacrep.utils import yesno

LOGGER = logging.getLogger("patatools.convert")
SUBCOMMAND_DESCRIPTION = "Convert between song formats"

def _usage():
    return "patatools convert INPUTFORMAT OUTPUTFORMAT FILES"

def confirm(destname):
    """Ask whether destination name should be overwrited."""
    while True:
        try:
            return yesno(input("File '{}' already exist. Overwrite? [yn] ".format(destname)))
        except ValueError:
            continue

def main(args=None):
    """Main function: run from command line."""
    if args is None:
        args = sys.argv
    if len(args) < 4:
        LOGGER.error("Invalid number of arguments.")
        LOGGER.error("Usage: %s", _usage())
        sys.exit(1)

    source = args[1]
    dest = args[2]
    song_files = args[3:]

    renderers = files.load_plugins(
        datadirs=DEFAULT_CONFIG.get('datadir', []),
        root_modules=['songs'],
        keyword='SONG_RENDERERS',
        )

    if dest not in renderers:
        LOGGER.error(
            "Unknown destination file format '%s'. Available ones are %s.",
            source,
            ", ".join(["'{}'".format(key) for key in renderers.keys()])
            )
        sys.exit(1)
    if source not in renderers[dest]:
        LOGGER.error(
            "Unknown source file format '%s'. Available ones are %s.",
            source,
            ", ".join(["'{}'".format(key) for key in renderers[dest].keys()])
            )
        sys.exit(1)

    for file in song_files:
        song = renderers[dest][source](file, DEFAULT_CONFIG)
        try:
            destname = "{}.{}".format(".".join(file.split(".")[:-1]), dest)
            if os.path.exists(destname):
                if not confirm(destname):
                    continue
            with open(destname, "w") as destfile:
                destfile.write(song.render())

        except NotImplementedError:
            LOGGER.error("Cannot convert to format '%s'.", dest)
            sys.exit(1)
        except KeyboardInterrupt:
            print()
            LOGGER.info("Aborted by user.")
            sys.exit(0)

    sys.exit(0)

if __name__ == "__main__":
    main()
