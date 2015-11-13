"""Conversion between formats

See the :meth:`__usage` method for more information.
"""

import os
import logging
import sys

from patacrep import files
from patacrep.build import DEFAULT_CONFIG
from patacrep.utils import yesno

LOGGER = logging.getLogger(__name__)

def __usage():
    return "python3 -m patacrep.songs.convert INPUTFORMAT OUTPUTFORMAT FILES"

def confirm(destname):
    while True:
        try:
            return yesno(input("File '{}' already exist. Overwrite? [yn] ".format(destname)))
        except ValueError:
            continue

if __name__ == "__main__":
    if len(sys.argv) < 4:
        LOGGER.error("Invalid number of arguments.")
        LOGGER.error("Usage: %s", __usage())
        sys.exit(1)

    source = sys.argv[1]
    dest = sys.argv[2]
    song_files = sys.argv[3:]

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
