"""Raw songbook utilities"""

import logging
import os
import sys
import yaml

from patacrep import encoding
from patacrep.build import config_model
from patacrep.utils import DictOfDict
from patacrep.songs import DataSubpath
import patacrep

LOGGER = logging.getLogger()

def open_songbook(filename):
    """Open a songbook file, and prepare it to
    return a raw songbook object.

    :param str filename: Filename of the yaml songbook.
    :rvalue: dict
    :return: Songbook, as a dictionary.
    """
    if os.path.exists(filename + ".yaml") and not os.path.exists(filename):
        filename += ".yaml"

    try:
        with patacrep.encoding.open_read(filename) as songbook_file:
            user_songbook = yaml.load(songbook_file)
        if 'encoding' in user_songbook.get('book', []):
            with encoding.open_read(
                filename,
                encoding=user_songbook['book']['encoding']
                ) as songbook_file:
                user_songbook = yaml.load(songbook_file)
    except Exception as error: # pylint: disable=broad-except
        raise patacrep.errors.SongbookError(str(error))

    user_songbook['_filepath'] = filename
    user_songbook['_basename'] = os.path.splitext(os.path.basename(filename))[0]

    return prepare_songbook(user_songbook)

def prepare_songbook(songbook):
    """Prepare a songbook by adding default values and datadirs
    Returns a raw songbook object.

    :param dict songbook: Initial yaml songbook.
    :rvalue: dict
    :return: Songbook, as a dictionary.
    """
    songbook = _add_songbook_defaults(songbook)


    # Gathering datadirs
    songbook['_datadir'] = list(_iter_absolute_datadirs(songbook))
    if 'datadir' in songbook['book']:
        del songbook['book']['datadir']

    songbook['_songdir'] = [
        DataSubpath(path, 'songs')
        for path in songbook['_datadir']
    ]

    return songbook

def _add_songbook_defaults(user_songbook):
    """ Adds the defaults values to the songbook if missing from
    the user songbook

    Priority:
        - User values
        - Default values of the user lang (if set)
        - Default english values
    """

    # Merge the default and user configs
    locale_default = config_model('default')
    # Initialize with default in english
    default_songbook = locale_default.get('en', {})
    default_songbook = DictOfDict(default_songbook)

    if 'lang' in user_songbook.get('book', []):
        # Update default with current lang
        lang = user_songbook['book']['lang']
        default_songbook.update(locale_default.get(lang, {}))
    # Update default with user_songbook
    default_songbook.update(user_songbook)

    return dict(default_songbook)

def _iter_absolute_datadirs(raw_songbook):
    """Iterate on the absolute datadirs of the raw songbook

    Appends the songfile dir at the end
    """
    datadir = raw_songbook.get('book', {}).get('datadir')
    filepath = raw_songbook['_filepath']

    if datadir is None:
        datadir = []
    elif isinstance(datadir, str):
        datadir = [datadir]
    basedir = os.path.dirname(os.path.abspath(filepath))

    for path in datadir:
        abspath = os.path.join(basedir, path)
        if os.path.exists(abspath) and os.path.isdir(abspath):
            yield abspath
        else:
            LOGGER.warning(
                "Ignoring non-existent datadir '{}'.".format(path)
                )
    yield basedir
