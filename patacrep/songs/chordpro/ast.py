"""Abstract Syntax Tree for ChordPro code."""

# pylint: disable=too-few-public-methods

import functools
import logging
import os

LOGGER = logging.getLogger()

def _indent(string):
    """Return and indented version of argument."""
    return "\n".join(["  {}".format(line) for line in string.split('\n')])

#: List of properties that are to be displayed in the flow of the song (not as
#: metadata at the beginning or end of song.
INLINE_PROPERTIES = {
    "partition",
    "comment",
    "guitar_comment",
    "image",
    }

#: List of properties that are listed in the `\beginsong` LaTeX directive.
BEGINSONG_PROPERTIES = {
    "album",
    "copyright",
    "cov",
    "vcov",
    "tag",
    }

#: Some directive have alternative names. For instance `{title: Foo}` and `{t:
#: Foo}` are equivalent.
DIRECTIVE_SHORTCUTS = {
    "t": "title",
    "st": "subtitle",
    "a": "album",
    "by": "artist",
    "c": "comment",
    "gc": "guitar_comment",
    "cover": "cov",
    "vcover": "vcov",
    }

def directive_name(text):
    """Return name of the directive, considering eventual shortcuts."""
    return DIRECTIVE_SHORTCUTS.get(text, text)


class AST:
    """Generic object representing elements of the song."""
    _template = None
    inline = False

    def template(self, extension):
        """Return the template to be used to render this object."""
        if self._template is None:
            LOGGER.warning("No template defined for {}.".format(self.__class__))
            base = "error"
        else:
            base = self._template
        return "content_{}.{}".format(base, extension)

class Line(AST):
    """A line is a sequence of (possibly truncated) words, spaces and chords."""

    _template = "line"

    def __init__(self):
        super().__init__()
        self.line = []

    def prepend(self, data):
        """Add an object at the beginning of line."""
        self.line.insert(0, data)
        return self

    def __str__(self):
        return "".join([str(item) for item in self.line])

    def strip(self):
        """Remove spaces at the beginning and end of line."""
        while True:
            if not self.line:
                return self
            if isinstance(self.line[0], Space):
                del self.line[0]
                continue
            if isinstance(self.line[-1], Space):
                del self.line[-1]
                continue
            return self

class LineElement(AST):
    """Something present on a line."""
    pass

class Word(LineElement):
    """A chunk of word."""
    _template = "word"

    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return self.value

class Space(LineElement):
    """A space between words"""
    _template = "space"

    def __init__(self):
        super().__init__()

    def __str__(self):
        return " "

class Chord(LineElement):
    """A chord."""

    _template = "chord"

    def __init__(self, key, alteration, modifier, add_note, bass):
        # pylint: disable=too-many-arguments
        super().__init__()
        self.key = key
        self.alteration = alteration
        self.modifier = modifier
        self.add_note = add_note
        self.bass = bass

    def __str__(self):
        text = ""
        text += self.key
        if self.alteration is not None:
            text += self.alteration
        if self.modifier is not None:
            text += self.modifier
        if self.add_note is not None:
            text += str(self.add_note)
        if self.bass is not None:
            text += "/" + self.bass[0]
            if self.bass[1] is not None:
                text += self.bass[1]
        return "[{}]".format(text)

class Verse(AST):
    """A verse (or bridge, or chorus)"""
    _template = "verse"
    type = "verse"
    inline = True

    def __init__(self):
        super().__init__()
        self.lines = []

    def prepend(self, data):
        """Add data at the beginning of verse."""
        self.lines.insert(0, data)
        return self

    def __str__(self):
        return '{{start_of_{type}}}\n{content}\n{{end_of_{type}}}'.format(
            type=self.type,
            content=_indent("\n".join([str(line) for line in self.lines])),
            )

class Chorus(Verse):
    """Chorus"""
    type = 'chorus'

class Bridge(Verse):
    """Bridge"""
    type = 'bridge'

class Song(AST):
    r"""A song

    Attributes:
        - content: the song content, as a list of objects `foo` such that
          `foo.inline` is True.
        - titles: The list of titles
        - language: The language (if set), None otherwise
        - authors: The list of authors
        - meta_beginsong: The list of directives that are to be set in the
          `\beginsong{}` LaTeX directive.
        - meta: Every other metadata.
        """

    #: Some directives are added to the song using special methods.
    METADATA_TYPE = {
        "title": "add_title",
        "subtitle": "add_subtitle",
        "artist": "add_author",
        "key": "add_key",
        }

    #: Some directives have to be processed before being considered.
    PROCESS_DIRECTIVE = {
        "cov": "_process_relative",
        "partition": "_process_relative",
        "image": "_process_relative",
        }

    def __init__(self, filename):
        super().__init__()
        self.content = []
        self.meta = []
        self._authors = []
        self._titles = []
        self._subtitles = []
        self._keys = []
        self.filename = filename

    def add(self, data):
        """Add an element to the song"""
        if isinstance(data, Directive):
            # Some directives are preprocessed
            name = directive_name(data.keyword)
            if name in self.PROCESS_DIRECTIVE:
                data = getattr(self, self.PROCESS_DIRECTIVE[name])(data)

        if data is None:
            # New line
            if not (self.content and isinstance(self.content[0], Newline)):
                self.content.insert(0, Newline())
        elif isinstance(data, Line):
            # Add a new line, maybe in the current verse.
            if not (self.content and isinstance(self.content[0], Verse)):
                self.content.insert(0, Verse())
            self.content[0].prepend(data.strip())
        elif data.inline:
            # Add an object in the content of the song.
            self.content.insert(0, data)
        elif isinstance(data, Directive):
            # Add a metadata directive. Some of them are added using special
            # methods listed in ``METADATA_TYPE``.
            name = directive_name(data.keyword)
            if name in self.METADATA_TYPE:
                getattr(self, self.METADATA_TYPE[name])(*data.as_tuple)
            else:
                self.meta.append(data)
        else:
            raise Exception()
        return self

    def str_meta(self):
        """Return an iterator over *all* metadata, as strings."""
        for title in self.titles:
            yield "{{title: {}}}".format(title)
        for author in self.authors:
            yield "{{by: {}}}".format(author)
        for key in sorted(self.keys):
            yield "{{key: {}}}".format(str(key))
        for key in sorted(self.meta):
            yield str(key)

    def __str__(self):
        return (
            "\n".join(self.str_meta()).strip()
            +
            "\n========\n"
            +
            "\n".join([str(item) for item in self.content]).strip()
            )


    def add_title(self, __ignored, title):
        """Add a title"""
        self._titles.insert(0, title)

    def add_subtitle(self, __ignored, title):
        """Add a subtitle"""
        self._subtitles.insert(0, title)

    @property
    def titles(self):
        """Return the list of titles (and subtitles)."""
        return self._titles + self._subtitles

    def add_author(self, __ignored, title):
        """Add an auhor."""
        self._authors.insert(0, title)

    @property
    def authors(self):
        """Return the list of (raw) authors."""
        return self._authors

    def get_directive(self, key, default=None):
        """Return the first directive with a given key."""
        for directive in self.meta:
            if directive.keyword == directive_name(key):
                return directive.argument
        return default

    def get_directives(self, key):
        """Return the list of directives with a given key."""
        values = []
        for directive in self.meta:
            if directive.keyword == directive_name(key):
                values.append(directive.argument)
        return values

    def add_key(self, __ignored, argument):
        """Add a new {key: foo: bar} directive."""
        key, *argument = argument.split(":")
        self._keys.append(Directive(
            key.strip(),
            ":".join(argument).strip(),
            ))

    @property
    def keys(self):
        """Return the list of keys.

        That is, directive that where given of the form ``{key: foo: bar}``.
        """
        return self._keys

    def meta_beginsong(self):
        r"""Return the meta information to be put in \beginsong."""
        for directive in BEGINSONG_PROPERTIES:
            if self.get_directive(directive) is not None:
                yield (directive, self.get_directive(directive))
        for (key, value) in self.keys:
            yield (key, value)


    def _process_relative(self, directive):
        """Return the directive, in which the argument is given relative to file

        This argument is expected to be a path (as a string).
        """
        return Directive(
            directive.keyword,
            os.path.join(
                os.path.dirname(self.filename),
                directive.argument,
                ),
            )

class Newline(AST):
    """New line"""
    _template = "newline"

    def __str__(self):
        return ""

@functools.total_ordering
class Directive(AST):
    """A directive"""

    def __init__(self, keyword="", argument=None):
        super().__init__()
        self._keyword = None
        self.keyword = keyword
        self.argument = argument

    @property
    def _template(self):
        """Name of the template to use to render this keyword.

        This only applies if ``self.inline == True``
        """
        return self.keyword

    @property
    def keyword(self):
        """Keyword of the directive."""
        return self._keyword

    @property
    def inline(self):
        """True iff this directive is to be rendered in the flow on the song.
        """
        return self.keyword in INLINE_PROPERTIES

    @keyword.setter
    def keyword(self, value):
        """self.keyword setter

        Replace keyword by its canonical name if it is a shortcut.
        """
        self._keyword = directive_name(value.strip())

    def __str__(self):
        if self.argument is not None:
            return "{{{}: {}}}".format(
                self.keyword,
                self.argument,
                )
        else:
            return "{{{}}}".format(self.keyword)

    @property
    def as_tuple(self):
        """Return the directive as a tuple."""
        return (self.keyword, self.argument)

    def __eq__(self, other):
        return self.as_tuple == other.as_tuple

    def __lt__(self, other):
        return self.as_tuple < other.as_tuple

class Tab(AST):
    """Tablature"""

    inline = True

    def __init__(self):
        super().__init__()
        self.content = []

    def prepend(self, data):
        """Add an element at the beginning of content."""
        self.content.insert(0, data)
        return self

    def __str__(self):
        return '{{start_of_tab}}\n{}\n{{end_of_tab}}'.format(
            _indent("\n".join(self.content)),
            )

