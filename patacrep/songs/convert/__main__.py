"""Conversion between formats

See the :meth:`__usage` method for more information.
"""

import logging
import sys

from patacrep.build import DEFAULT_CONFIG
from patacrep import files

LOGGER = logging.getLogger(__name__)

def __usage():
    return "python3 -m patacrep.songs.convert chordpro latex FILE"

if __name__ == "__main__":
    if len(sys.argv) != 4:
        LOGGER.error("Invalid number of arguments.")
        LOGGER.error("Usage: %s", __usage())
        sys.exit(1)

    source = sys.argv[1]
    dest = sys.argv[2]
    file = sys.argv[3]

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

    song = song_parsers[source](".", file, DEFAULT_CONFIG)
    try:
        print(song.render(dest))
    except NotImplementedError:
        LOGGER.error("Cannot convert to format '%s'.", dest)
        sys.exit(1)

    sys.exit(0)
