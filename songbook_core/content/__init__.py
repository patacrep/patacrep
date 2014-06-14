#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import importlib
import jinja2
import logging
import os

from songbook_core.errors import SongbookError

LOGGER = logging.getLogger(__name__)
EOL = '\n'

class Content:
    """Content item of type 'example'."""

    def render(self, context):
        """Render this content item.

        Returns a string, to be placed verbatim in the generated .tex file.
        """
        return ""

    # Block management

    def begin_new_block(self, previous, context):
        """Return a boolean stating if a new block is to be created.

        # Arguments

        - previous: the songbook.content.Content object of the previous item.
        - context: current jinja2.runtime.Context.

        # Return

        True if the renderer has to close previous block, and begin a new one,
        False otherwise.
        """
        return True

    def begin_block(self, context):
        """Return the string to begin a block."""
        return ""

    def end_block(self, context):
        """Return the string to end a block."""
        return ""

class ContentError(SongbookError):
    def __init__(self, keyword, message):
        self.keyword = keyword
        self.message = message

    def __str__(self):
        return "Content: {}: {}".format(self.keyword, self.message)

def load_plugins():
    """Load all content plugins, and return a dictionary of those plugins.

    Return value: a dictionary where:
    - keys are the keywords ;
    - values are functions triggered when this keyword is met.
    """
    plugins = {}
    for name in glob.glob(os.path.join(os.path.dirname(__file__), "*.py")):
        if name.endswith(".py") and os.path.basename(name) != "__init__.py":
            plugin = importlib.import_module(
                    'songbook_core.content.{}'.format(os.path.basename(name[:-len('.py')]))
                )
            for (key, value) in plugin.CONTENT_PLUGINS.items():
                if key in plugins:
                    LOGGER.warning("File %s: Keyword '%s' is already used. Ignored.", os.path.relpath(name), key)
                    continue
                plugins[key] = value
    return plugins

@jinja2.contextfunction
def render_content(context, content):
    rendered = ""
    previous = None
    last = None
    for elem in content:
        if not isinstance(elem, Content):
            LOGGER.error("Ignoring bad content item '{}'.".format(elem))
            continue

        last = elem
        if elem.begin_new_block(previous, context):
            if previous:
                rendered += previous.end_block(context) + EOL
            rendered += elem.begin_block(context) + EOL
        rendered += elem.render(context) + EOL
        previous = elem

    if isinstance(last, Content):
        rendered += last.end_block(context) + EOL

    return rendered

def process_content(content, config = None):
    contentlist = []
    plugins = load_plugins()
    if not content:
        content = [["song"]]
    for elem in content:
        if isinstance(elem, basestring):
            elem = ["song", elem]
        if len(content) == 0:
            content = ["song"]
        if elem[0] not in plugins:
            raise ContentError(elem[0], "Unknown content type.")
        contentlist.extend(plugins[elem[0]](elem[0], config, *elem[1:]))
    return contentlist
