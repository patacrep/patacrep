"""Include an external list of songs

This plugin provides keyword 'include', used to include an external list of
songs in JSON or YAML format.
"""

import os
import logging

import yaml

from patacrep.content import process_content, ContentError, ContentList, validate_parser_argument
from patacrep import encoding, errors

LOGGER = logging.getLogger(__name__)

def load_from_datadirs(filename, songdirs, songbookfile_dir=None):
    """Load 'filename', relative to:
        - or one of the songdirs
        - the dir of the songbook file dir

    Raise an exception if it was not found in any directory.
    """
    for path in songdirs:
        fullpath = os.path.join(path.fullpath, filename)
        if os.path.exists(fullpath):
            return fullpath
    if songbookfile_dir:
        fullpath = os.path.join(songbookfile_dir, filename)
        if os.path.exists(fullpath):
            return fullpath
    # File not found
    raise ContentError(
        "include",
        errors.notfound(filename, list(songdirs))
        )

#pylint: disable=unused-argument
@validate_parser_argument("""
type: //any
of:
  - type: //str
  - type: //arr
    contents: //str
""")
def parse(keyword, config, argument):
    """Include an external file content.

    Arguments:
        - keyword: the string 'include';
        - config: the current songbook configuration dictionary;
        - argument:
            a list of file paths to be included
            or a string of the file to include

    """
    new_contentlist = ContentList()
    if isinstance(argument, str):
        argument = [argument]

    for filename in argument:
        try:
            filepath = load_from_datadirs(
                filename,
                config['_songdir'],
                config.get('_songbookfile_dir')
            )
        except ContentError as error:
            new_contentlist.append_error(error)
            continue
        content_file = None
        try:
            with encoding.open_read(
                filepath,
                encoding=config['book']['encoding']
                ) as content_file:
                new_content = yaml.safe_load(content_file)
        except Exception as error: # pylint: disable=broad-except
            new_contentlist.append_error(ContentError(
                keyword="include",
                message="Error while loading file '{}': {}".format(filepath, error),
                ))
            continue

        config['_datadir'].append(os.path.abspath(os.path.dirname(filepath)))
        new_contentlist.extend(process_content(new_content, config))
        config['_datadir'].pop()

    return new_contentlist

CONTENT_PLUGINS = {'include': parse}
