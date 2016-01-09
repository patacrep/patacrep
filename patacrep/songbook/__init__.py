"""Raw songbook utilities"""

import logging
import os
import sys
import yaml

from patacrep import encoding
import patacrep

LOGGER = logging.getLogger()

def open_songbook(filename):
    """Open songbook, and return a raw songbook object.

    :param str filename: Filename of the yaml songbook.
    :rvalue: dict
    :return: Songbook, as a dictionary.
    """
    if os.path.exists(filename + ".sb") and not os.path.exists(filename):
        filename += ".sb"

    try:
        with patacrep.encoding.open_read(filename) as songbook_file:
            songbook = yaml.load(songbook_file)
        if 'encoding' in songbook:
            with encoding.open_read(
                filename,
                encoding=songbook['encoding']
                ) as songbook_file:
                songbook = yaml.load(songbook_file)
    except Exception as error: # pylint: disable=broad-except
        raise patacrep.errors.YAMLError(str(error))

    songbook['_basename'] = os.path.basename(filename)[:-3]

    # Gathering datadirs
    datadirs = []
    if 'datadir' in songbook:
        if isinstance(songbook['datadir'], str):
            songbook['datadir'] = [songbook['datadir']]
        datadirs += [
            os.path.join(
                os.path.dirname(os.path.abspath(filename)),
                path
                )
            for path in songbook['datadir']
            ]
    # Default value
    datadirs.append(os.path.dirname(os.path.abspath(filename)))

    songbook['datadir'] = datadirs

    return songbook
