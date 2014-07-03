# -*- coding: utf-8 -*-

"""Include an external list of songs

This plugin provides keyword 'include', used to include an external list of
songs in JSON format.
"""

import json
import os
import sys
import logging

from patacrep.content import process_content

LOGGER = logging.getLogger(__name__)

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
    songbook_dir = config.get("_songbook_dir", "")
    if not os.path.isdir(songbook_dir):
        LOGGER.warning("No songbook directory in configuration. 'include' "
                        "keyword may fail.")

    for path in contentlist:
        filepath = os.path.join(songbook_dir, path)
        try:
            with open(filepath, "r") as content_file:
                new_content = json.load(content_file)
        except Exception as error: # pylint: disable=broad-except
            LOGGER.error(error)
            LOGGER.error("Error while loading file '{}'.".format(filepath))
            sys.exit(1)

        config["_songbook_dir"] = os.path.abspath(
                                        os.path.dirname(filepath)
                                    )

        new_contentlist += process_content(new_content, config)
    config["_songbook_dir"] = songbook_dir

    return new_contentlist

CONTENT_PLUGINS = {'include': parse}
