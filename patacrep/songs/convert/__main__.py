"""Conversion between formats

See the :meth:`__usage` method for more information.
"""

import os
import logging
import sys

from patacrep.build import DEFAULT_CONFIG
from patacrep import files

LOGGER = logging.getLogger(__name__)

def __usage():
    return "python3 -m patacrep.songs.convert INPUTFORMAT OUTPUTFORMAT FILES"

def yesno(prompt):
    while True:
        answer = input("{} [yn] ".format(prompt))
        if answer.strip().lower() == "y":
            return True
        if answer.strip().lower() == "n":
            return False

def confirm(destname):
    return yesno("File '{}' already exist. Overwrite?".format(destname))

if __name__ == "__main__":
    if len(sys.argv) < 4:
        LOGGER.error("Invalid number of arguments.")
        LOGGER.error("Usage: %s", __usage())
        sys.exit(1)

    source = sys.argv[1]
    dest = sys.argv[2]
    song_files = sys.argv[3:]

    song_parsers = files.load_plugins(
        datadirs=DEFAULT_CONFIG.get('datadir', []),
        root_modules=['songs'],
        keyword='SONG_PARSERS',
        )

    if source not in song_parsers:
        LOGGER.error(
            "Unknown file format '%s'. Available ones are %s.",
            source,
            ", ".join(["'{}'".format(key) for key in song_parsers.keys()])
            )
        sys.exit(1)

    for file in song_files:
        song = song_parsers[source](".", file, DEFAULT_CONFIG)
        try:
            converted = song.render(dest)
            destname = "{}.{}".format(".".join(file.split(".")[:-1]), dest)
            if os.path.exists(destname):
                if not confirm(destname):
                    continue
            with open(destname, "w") as destfile:
                destfile.write(converted)

        except NotImplementedError:
            LOGGER.error("Cannot convert to format '%s'.", dest)
            sys.exit(1)
        except KeyboardInterrupt:
            print()
            LOGGER.info("Aborted by user.")
            sys.exit(0)

    sys.exit(0)
