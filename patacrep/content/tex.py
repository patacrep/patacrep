#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Include LaTeX raw code in the songbook."""

import logging
import os

from patacrep import files
from patacrep.content import Content

LOGGER = logging.getLogger(__name__)

class LaTeX(Content):
    """Inclusion of LaTeX code"""

    def __init__(self, filename):
        self.filename = filename

    def render(self, context):
        return r'\input{{{}}}'.format(files.relpath(
            self.filename,
            os.path.dirname(context['filename']),
            ))

#pylint: disable=unused-argument
def parse(keyword, argument, contentlist, config):
    """Parse the contentlist.

    Arguments:
    - keyword: unused;
    - argument: unused;
    - contentlist: a list of name of tex files;
    - config: configuration dictionary of the current songbook.
    """
    if not contentlist:
        LOGGER.warning(
                "Useless 'tex' content: list of files to include is empty."
                )
    filelist = []
    for filename in contentlist:
        checked_file = None
        for path in config['_songdir']:
            if os.path.exists(os.path.join(path, filename)):
                checked_file = os.path.relpath(os.path.join(path, filename))
                break
        if not checked_file:
            LOGGER.warning(
                    ("Cannot find file '{}' in '{}'. Compilation may fail "
                    "later.").format(filename, str(config['_songdir']))
                    )
            continue
        filelist.append(LaTeX(checked_file))

    return filelist


CONTENT_PLUGINS = {'tex': parse}
