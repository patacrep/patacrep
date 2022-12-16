"""Content plugin management.

Content that can be included in a songbook is controlled by plugins. From the
user (or .yaml file) point of view, each piece of content is introduced by a
keyword. This keywold is associated with a plugin (a submodule of this very
module), which parses the content, and return a ContentList object, which is
little more than a list of instances of the ContentItem class.

# Plugin definition

A plugin is a submodule of this module, (or a python file in directory
<datadir>/python/content), which have a variable CONTENT_PLUGINS, which is a
dictionary where:
    - keys are keywords,
    - values are parsers (see below).

When analysing the content field of the .yaml file, when those keywords are
met, the corresponding parser is called.

# Keyword examples

    - sort
    - section*
    - cd

# Parsers

A parser is a function which takes as arguments:
    - keyword: the keyword triggering this function;
    - argument: the argument of the keyword (see below);
    - config: the configuration object of the current songbook. Plugins can
      change it.

A parser returns a ContentList object (a list of instances of the ContentItem
class), defined in this module (or of subclasses of this class).

Example: When the following piece of content is met
    sort:
      key: ["author", "title"]
      content:
        - "a_song.sg"
        - "another_song.sg"

the parser associated to keyword 'sort' get the arguments:
    - keyword = "sort"
    - argument = {
        'key': ["author", "title"],
        'content': ["a_song.sg", "another_song.sg"],
    }
    - config = <the config file of the current songbook>.

# ContentItem class

The content classes are subclasses of class ContentItem defined in this module.
ContentItem is a perfectly valid class, but instances of it will not generate
anything in the resulting .tex.

More documentation in the docstring of ContentItem.

"""

import glob
import logging
import os
import re
import sys

import jinja2
import yaml

from patacrep import files, Rx
from patacrep.errors import SharedError

LOGGER = logging.getLogger(__name__)
EOL = '\n'

#pylint: disable=no-self-use
class ContentItem:
    """Content item. Will render to something in the .tex file.

    The current jinja2.runtime.Context is passed to all function defined
    here.
    """

    def render(self, context):
        """Render this content item.

        Returns a string, to be placed verbatim in the generated .tex file.
        """
        return ""

    # Block management

    def begin_new_block(self, previous, context):
        """Return a boolean stating if a new block is to be created.

        # Arguments

        - __previous: the songbook.content.ContentItem object of the previous item.
        - __context: see ContentItem() documentation.

        # Return

        - True if the renderer has to close previous block, and begin a new
          one,
        - False otherwise (the generated code for this item is part of the
          current block).
        """
        return True

    def begin_block(self, context):
        """Return the string to begin a block."""
        return ""

    def end_block(self, context):
        """Return the string to end a block."""
        return ""

    def to_dict(self):
        """Return the dict representation (as in the yaml file)."""
        raise NotImplementedError()

class ContentError(SharedError):
    """Error in a content plugin."""
    def __init__(self, keyword=None, message=None):
        super().__init__()
        self.keyword = keyword
        self.message = message

    def __str__(self):
        text = "Content"
        if self.keyword is not None:
            text += ": " + self.keyword
        if self.message is not None:
            text += ": " + self.message
        return text

    @property
    def __dict__(self):
        parent = vars(super())
        parent.update({
            'keyword': self.keyword,
            'message': self.message,
            })
        return parent

class ContentList:
    """List of content items"""

    def __init__(self, *args, **kwargs):
        self._content = list(*args, **kwargs)
        self._errors = []

    def __iter__(self):
        yield from self._content

    def extend(self, iterator):
        """Extend content list with an iterator.

        If the argument is of the same type, the list of errors is
        also extended.
        """
        self._content.extend(iterator)
        if isinstance(iterator, ContentList):
            self._errors.extend(iterator.iter_errors())

    def append(self, item):
        """Append an item to the content list."""
        return self._content.append(item)

    def __len__(self):
        return len(self._content)

    def append_error(self, error):
        """Log and append an error to the error list."""
        LOGGER.warning(error)
        self._errors.append(error)

    def extend_error(self, errors):
        """Extend the error list with the argument, which is logged."""
        for error in errors:
            self.append_error(error)

    def iter_errors(self):
        """Iterate over errors."""
        yield from self._errors
        for item in self:
            if not hasattr(item, "iter_errors"):
                continue
            yield from item.iter_errors()

    def has_errors(self):
        """Return `True` iff errors has been found."""
        for _ in self.iter_errors():
            return True
        return False

class EmptyContentList(ContentList):
    """Empty content list: contain only errors."""
    def __init__(self, *, errors):
        super().__init__()
        for error in errors:
            self.append_error(error)

@jinja2.pass_context
def render(context, content):
    """Render the content of the songbook as a LaTeX code.

    Arguments:
    - context: the jinja2.runtime.context of the current template
      compilation.
    - content: a list of ContentItem() instances, as the one that was returned by
      process_content().
    """
    rendered = ""
    previous = None
    last = None
    for elem in content:
        if not isinstance(elem, ContentItem):
            LOGGER.warning("Ignoring bad content item '{}'.".format(elem))
            continue

        last = elem
        if elem.begin_new_block(previous, context):
            if previous:
                rendered += previous.end_block(context) + EOL
            rendered += elem.begin_block(context) + EOL
        rendered += elem.render(context) + EOL
        previous = elem

    if last is not None:
        rendered += last.end_block(context) + EOL

    return rendered

def validate_parser_argument(raw_schema):
    """Check that the parser argument respects the schema

    Will raise `ContentError` if the schema is not respected.
    """
    schema = Rx.make_schema(yaml.safe_load(raw_schema))

    def wrap(parse):
        """Wrap the parse function"""
        def wrapped(keyword, argument, config):
            """Check the argument schema before calling the plugin parser"""
            try:
                schema.validate(argument)
            except Rx.SchemaMismatch as exception:
                msg = 'Invalid syntax:\n---\n{}---\n{}'.format(
                    yaml.dump({keyword: argument}, default_flow_style=False),
                    str(exception)
                )
                raise ContentError(keyword, msg)
            return parse(keyword, argument=argument, config=config)
        return wrapped
    return wrap


def process_content(content, config=None):
    """Process content, and return a list of ContentItem() objects.

    Arguments are:
    - content: the content field of the .yaml file, which should be a nested list
    and describe what is to be included in the songbook;
    - config: the configuration dictionary of the current songbook.

    Return: a list of ContentItem objects, corresponding to the content to be
    included in the .tex file.
    """
    contentlist = ContentList()
    plugins = files.load_content_plugins(config['_datadir'])
    if not content:
        content = [{'song': None}]
    elif isinstance(content, dict):
        content = [content]
    for elem in content:
        if isinstance(elem, str):
            elem = {'song': elem}
        if isinstance(elem, dict):
            for keyword, argument in elem.items():
                try:
                    if keyword not in plugins:
                        raise ContentError(keyword, "Unknown content keyword.")
                    contentlist.extend(plugins[keyword](
                        keyword,
                        argument=argument,
                        config=config,
                        ))
                except ContentError as error:
                    contentlist.append_error(error)
        else:
            contentlist.append_error(ContentError(str(elem), "Unknown content type."))
    if contentlist.has_errors() and config['_error'] in ("failonsong", "failonbook"):
        raise ContentError(
            "Error while parsing the 'content' section of the songbook. Stopping as requested."
        )
    return contentlist
