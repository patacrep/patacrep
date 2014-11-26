"""Include an external list of songs

This plugin provides keyword 'include', used to include an external list of
songs in JSON format.
"""

import json
import os
import sys
import logging

from patacrep.content import process_content, ContentError
from patacrep import encoding
from patacrep import errors

LOGGER = logging.getLogger(__name__)

def load_from_datadirs(path, config=None):
    """Load 'path' from one of the datadirs.

    Raise an exception if it was found if none of the datadirs of 'config'.
    """
    for datadir in config.get("datadir", []):
        filepath = os.path.join(datadir, path)
        if os.path.exists(filepath):
            return filepath
    # File not found
    raise ContentError(
            "include",
            errors.notfound(path, config.get("datadir", [])),
            )

#pylint: disable=unused-argument
def parse(keyword, config, argument, contentlist):
    """Include an external file content.

    Arguments:
        - keyword: the string 'include';
        - config: the current songbook configuration dictionary;
        - argument: None;
        - contentlist: a list of file paths to be included.
    """
    new_contentlist = []

    for path in contentlist:
        filepath = load_from_datadirs(path, config)
        content_file = None
        try:
            with encoding.open_read(
                    filepath,
                    encoding=config['encoding']
                    ) as content_file:
                new_content = json.load(content_file)
        except Exception as error: # pylint: disable=broad-except
            LOGGER.error(error)
            LOGGER.error("Error while loading file '{}'.".format(filepath))
            sys.exit(1)

        config["datadir"].append(os.path.abspath(os.path.dirname(filepath)))
        new_contentlist += process_content(new_content, config)
        config["datadir"].pop()

    return new_contentlist

CONTENT_PLUGINS = {'include': parse}
