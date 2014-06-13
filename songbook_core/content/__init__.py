#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import importlib
import logging
import os

from songbook_core.errors import SongbookError

LOGGER = logging.getLogger(__name__)
EOL = '\n'

class Content:
    """Content item of type 'example'."""

    def render(self):
        """Render this content item.

        Returns a string, to be placed verbatim in the generated .tex file.
        """
        return ""

    # Block management

    def begin_new_block(self, previous):
        """Return a boolean stating if a new block is to be created.

        # Arguments

        - previous: the songbook.content.Content object of the previous item.

        # Return

        True if the renderer has to close previous block, and begin a new one,
        False otherwise.

        # Default

        The default behavior of this method (if not defined in this child
        class) is: begin a new block if the previous item is not an instance of
        the same class.
        """
        return False

    def begin_block(self):
        """Return the string to begin a block."""
        return ""

    def end_block(self):
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

def render_content(content):
    rendered = ""
    previous = None
    last = None
    for elem in content:
        if not isinstance(elem, Content):
            LOGGER.error("Ignoring bad content item '{}'.".format(elem))
            continue

        last = elem
        if elem.begin_new_block(previous):
            if previous:
                rendered += previous.end_block() + EOL
            rendered += elem.begin_block() + EOL
        rendered += elem.render() + EOL

    if isinstance(last, Content):
        rendered += last.end_block() + EOL

    return rendered

def process_content(content, config = None):
    contentlist = []
    plugins = load_plugins()
    for elem in content:
        if isinstance(elem, basestring):
            TODO
        if len(content) == 0:
            TODO
        if elem[0] not in plugins:
            raise ContentError(elem[0], "Unknown content type.")
        contentlist.extend(plugins[elem[0]](*elem))
    return contentlist
        ## Compute song list
        #if self.config['content'] is None:
        #    self.config['content'] = [(
        #            "song",
        #            os.path.relpath(
        #                filename,
        #                os.path.join(self.config['datadir'][0], 'songs'),
        #                ))
        #            for filename
        #            in recursive_find(
        #                        os.path.join(self.config['datadir'][0], 'songs'),
        #                        '*.sg',
        #                        )
        #            ]
        #else:
        #    content = self.config["content"]
        #    self.config["content"] = []
        #    for elem in content:
        #        if isinstance(elem, basestring):
        #            self.config["content"].append(("song", elem))
        #        elif isinstance(elem, list):
        #            self.config["content"].append((elem[0], elem[1]))
        #        else:
        #            raise errors.SBFileError(
        #                         "Syntax error: could not decode the content "
        #                         "of {0}".format(self.basename)
        #                         )
