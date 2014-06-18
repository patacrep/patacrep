#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Content plugin management.

Content that can be included in a songbook is controlled by plugins. From the
user (or .sb file) point of view, each piece of content is introduced by a
keyword. This keywold is associated with a plugin (a submodule of this very
module), which parses the content, and return a list of instances of the
Content class.

# Plugin definition

A plugin is a submodule of this module, which have a variable
CONTENT_PLUGINS, which is a dictionary where:
    - keys are keywords,
    - values are parsers (see below).

When analysing the content field of the .sb file, when those keywords are
met, the corresponding parser is called.

# Parsers

A parser is a function which takes as arguments:
    - keyword: the keyword triggering this function;
    - argument: the argument of the keyword (see below);
    - contentlist: the list of content, that is, the part of the list
      following the keyword (see example below);
    - config: the configuration object of the current songbook. Plugins can
      change it.

A parser returns a list of instances of the Content class, defined in
this module (or of subclasses of this class).

Example: When the following piece of content is met

    ["sorted(author, @title)", "a_song.sg", "another_song.sg"]

the parser associated to keyword 'sorted' get the arguments:
    - keyword = "sorted"
    - argument = "author, @title"
    - contentlist = ["a_song.sg", "another_song.sg"]
    - config = <the config file of the current songbook>.

# Keyword

A keyword is either an identifier (alphanumeric characters, and underscore),
or such an identifier, with some text surrounded by parenthesis (like a
function definition); this text is called the argument to the keyword.
Examples:
    - sorted
    - sorted(author, @title)
    - cwd(some/path)

If the keyword has an argument, it can be anything, given that it is
surrounded by parenthesis. It is up to the plugin to parse this argument. For
intance, keyword "foo()(( bar()" is a perfectly valid keyword, and the parser
associated to "foo" will get as argument the string ")(( bar(".

# Content class

The content classes are subclasses of class Content defined in this module.
Content is a perfectly valid class, but instances of it will not generate
anything in the resulting .tex.

More documentation in the docstring of Content.

"""

import glob
import importlib
import jinja2
import logging
import os
import re

from patacrep import files
from patacrep.errors import SongbookError

LOGGER = logging.getLogger(__name__)
EOL = '\n'

#pylint: disable=no-self-use
class Content(object):
    """Content item. Will render to something in the .tex file.

    The current jinja2.runtime.Context is passed to all function defined
    here.
    """

    def render(self, __context):
        """Render this content item.

        Returns a string, to be placed verbatim in the generated .tex file.
        """
        return ""

    # Block management

    def begin_new_block(self, __previous, __context):
        """Return a boolean stating if a new block is to be created.

        # Arguments

        - __previous: the songbook.content.Content object of the previous item.
        - __context: see Content() documentation.

        # Return

        - True if the renderer has to close previous block, and begin a new
          one,
        - False otherwise (the generated code for this item is part of the
          current block).
        """
        return True

    def begin_block(self, __context):
        """Return the string to begin a block."""
        return ""

    def end_block(self, __context):
        """Return the string to end a block."""
        return ""

class ContentError(SongbookError):
    """Error in a content plugin."""
    def __init__(self, keyword, message):
        super(ContentError, self).__init__()
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
                    'patacrep.content.{}'.format(
                        os.path.basename(name[:-len('.py')])
                        )
                    )
            for (key, value) in plugin.CONTENT_PLUGINS.items():
                if key in plugins:
                    LOGGER.warning(
                            "File %s: Keyword '%s' is already used. Ignored.",
                            files.relpath(name),
                            key,
                            )
                    continue
                plugins[key] = value
    return plugins

@jinja2.contextfunction
def render_content(context, content):
    """Render the content of the songbook as a LaTeX code.

    Arguments:
    - context: the jinja2.runtime.context of the current template
      compilation.
    - content: a list of Content() instances, as the one that was returned by
      process_content().
    """
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

def process_content(content, config=None):
    """Process content, and return a list of Content() objects.

    Arguments are:
    - content: the content field of the .sb file, which should be a list, and
      describe what is to be included in the songbook;
    - config: the configuration dictionary of the current songbook.

    Return: a list of Content objects, corresponding to the content to be
    included in the .tex file.
    """
    contentlist = []
    plugins = load_plugins()
    keyword_re = re.compile(r'^ *(?P<keyword>\w*) *(\((?P<argument>.*)\))? *$')
    if not content:
        content = [["song"]]
    for elem in content:
        if isinstance(elem, basestring):
            elem = ["song", elem]
        if len(content) == 0:
            content = ["song"]
        try:
            match = keyword_re.match(elem[0]).groupdict()
        except AttributeError:
            raise ContentError(elem[0], "Cannot parse content type.")
        (keyword, argument) = (match['keyword'], match['argument'])
        if keyword not in plugins:
            raise ContentError(keyword, "Unknown content type.")
        contentlist.extend(plugins[keyword](
            keyword,
            argument=argument,
            contentlist=elem[1:],
            config=config,
            ))
    return contentlist
