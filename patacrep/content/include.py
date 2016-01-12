"""Include an external list of songs

This plugin provides keyword 'include', used to include an external list of
songs in JSON format.
"""

import json
import os
import logging

from patacrep.content import process_content, ContentError, ContentList
from patacrep import encoding, errors, files

LOGGER = logging.getLogger(__name__)

def load_from_datadirs(path, datadirs):
    """Load 'path' from one of the datadirs.

    Raise an exception if it was found if none of the datadirs of 'config'.
    """
    for filepath in files.iter_datadirs(datadirs, "songs", path):
        if os.path.exists(filepath):
            return filepath
    # File not found
    raise ContentError(
        "include",
        errors.notfound(path, list(files.iter_datadirs(datadirs)))
        )

#pylint: disable=unused-argument
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

    for path in argument:
        try:
            filepath = load_from_datadirs(path, config['_datadir'])
        except ContentError as error:
            new_contentlist.append_error(error)
            continue
        content_file = None
        try:
            with encoding.open_read(
                filepath,
                encoding=config['book']['encoding']
                ) as content_file:
                new_content = json.load(content_file)
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
