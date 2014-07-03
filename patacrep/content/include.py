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
        - keyword: the string 'sorted';
        - config: the current songbook configuration dictionary;
        - argument: None;
        - contentlist: a list of file paths to be included.
    """
    new_contentlist = []
    for path in contentlist:
        filepath = os.path.join(config["_songbook_dir"], path)
        try:
            with open(filepath, "r") as content_file:
                old_songbook_dir = config["_songbook_dir"]
                new_content = json.load(content_file)
        except Exception as error: # pylint: disable=broad-except
            LOGGER.error(error)
            LOGGER.error("Error while loading file '{}'.".format(filepath))
            sys.exit(1)

        config["_songbook_dir"] = os.path.abspath(
                                        os.path.dirname(filepath)
                                    )

        new_contentlist += process_content(new_content, config)
        config["_songbook_dir"] = old_songbook_dir

    return new_contentlist

CONTENT_PLUGINS = {'include': parse}
