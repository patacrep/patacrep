"""Abstract Syntax Tree for ChordPro code."""

# pylint: disable=too-few-public-methods

from collections import OrderedDict
import functools
import logging

from patacrep.songs import errors

LOGGER = logging.getLogger()

def _indent(string):
    """Return and indented version of argument."""
    return "\n".join(["  {}".format(line) for line in string.split('\n')])

#: Available directives, that is, directives that we know how to deal with
AVAILABLE_DIRECTIVES = [
    "album",
    "artist",
    "capo",
    "comment",
    "copyright",
    "columns",
    "cover",
    "define",
    "guitar_comment",
    "image",
    "key",
    "language",
    "newline",
    "partition",
    "subtitle",
    "tag",
    "title",
    ]

#: List of properties that are to be displayed in the flow of the song (not as
#: metadata at the beginning or end of song.
INLINE_DIRECTIVES = {
    "partition",
    "comment",
    "guitar_comment",
    "image",
    "newline",
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
    "cov": "cover",
    "lang": "language",
    }

def directive_name(text):
    """Return name of the directive, considering eventual shortcuts."""
    return DIRECTIVE_SHORTCUTS.get(text, text)


class AST:
    """Generic object representing elements of the song."""
    _template = None
    inline = False
    lexer = None

    def __init__(self):
        self.lineno = self.lexer.lineno

    def template(self):
        """Return the template to be used to render this object."""
        if self._template is None:
            LOGGER.warning("No template defined for {}.".format(self.__class__))
            base = "error"
        else:
            base = self._template
        return "content_{}".format(base)

class Error(AST):
    """Parsing error. To be ignored."""

class Line(AST):
    """A line is a sequence of (possibly truncated) words, spaces and chords."""

    _template = "line"

    def __init__(self, *items):
        super().__init__()
        self.line = list(items)

    def __iter__(self):
        yield from self.line

    def prepend(self, data):
        """Add an object at the beginning of line.

        Does nothing if argument is `None`.
        """
        if data is not None:
            self.line.insert(0, data)
        return self

    def strip(self):
        """Remove spaces at the beginning and end of line."""
        while True:
            if not self.line:
                return self
            if isinstance(self.line[0], Space) or isinstance(self.line[0], Error):
                del self.line[0]
                continue
            if isinstance(self.line[-1], Space) or isinstance(self.line[-1], Error):
                del self.line[-1]
                continue
            return self

    def is_empty(self):
        """Return `True` iff line is empty."""
        return len(self.strip().line) == 0

class Echo(AST):
    """An inline echo"""
    _template = "echo"
    type = 'echo'

    def __init__(self, line):
        super().__init__()
        self.line = line

class LineElement(AST):
    """Something present on a line."""
    # pylint: disable=abstract-method
    pass

class Word(LineElement):
    """A chunk of word."""
    _template = "word"

    def __init__(self, value):
        super().__init__()
        self.value = value

class Space(LineElement):
    """A space between words"""
    _template = "space"

    def __init__(self):
        super().__init__()

class ChordList(LineElement):
    """A list of chords."""
    _template = "chordlist"

    def __init__(self, *chords):
        super().__init__()
        self.chords = chords

class Chord(AST):
    """A chord."""

    _template = "chord"

    def __init__(self, chord):
        super().__init__()
        self.chord = chord

    @property
    def pretty_chord(self):
        """Return the chord with nicer (utf8) alteration"""
        return self.chord.replace('b', '♭').replace('#', '♯')

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

    def directive(self):
        """Return `True` iff the verse is composed only of directives."""
        for line in self.lines:
            for element in line:
                if not isinstance(element, Directive):
                    return False
        return True

    @property
    def nolyrics(self):
        """Return `True` iff verse contains only notes (no lyrics)"""
        for line in self.lines:
            for item in line.line:
                if not (isinstance(item, Space) or isinstance(item, ChordList)):
                    return False
        return True

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
        - lang: The language code (if set), None otherwise
        - authors: The list of authors
        - meta: Every other metadata.
        """

    #: Some directives are added to the song using special methods.
    METADATA_ADD = {
        "title": "add_title",
        "subtitle": "add_subtitle",
        "artist": "add_author",
        "key": "add_key",
        "define": "add_cumulative",
        "tag": "add_cumulative",
        }

    def __init__(self, filename, directives, *, error_builders=None):
        super().__init__()
        self.content = []
        self.meta = OrderedDict()
        self._authors = []
        self._titles = []
        self._subtitles = []
        self.filename = filename
        if error_builders is None:
            self.error_builders = []
        else:
            self.error_builders = error_builders
        for directive in directives:
            self.add(directive)

    def add(self, data):
        """Add an element to the song"""
        # pylint: disable=too-many-branches
        if isinstance(data, Error):
            pass
        elif data is None:
            # New line
            if not (self.content and isinstance(self.content[0], EndOfLine)):
                self.content.insert(0, EndOfLine())
        elif isinstance(data, Line):
            # Add a new line, maybe in the current verse.
            if not data.is_empty():
                if not (self.content and isinstance(self.content[0], Verse)):
                    self.content.insert(0, Verse())
                self.content[0].prepend(data.strip())
        elif isinstance(data, Directive) and data.inline:
            # Add a directive in the content of the song.
            # It is useless to check if directive is in AVAILABLE_DIRECTIVES,
            # since it is in INLINE_DIRECTIVES.
            self.content.append(data)
        elif data.inline:
            # Add an object in the content of the song.
            self.content.insert(0, data)
        elif isinstance(data, Directive):
            # Add a metadata directive. Some of them are added using special
            # methods listed in ``METADATA_ADD``.
            if data.keyword not in AVAILABLE_DIRECTIVES:
                message = "Ignoring unknown directive '{}'.".format(data.keyword)
                LOGGER.warning("Song {}, line {}: {}".format(self.filename, data.lineno, message))
                self.error_builders.append(functools.partial(
                    errors.SongSyntaxError,
                    line=data.lineno,
                    message=message,
                    ))
            if data.keyword in self.METADATA_ADD:
                getattr(self, self.METADATA_ADD[data.keyword])(data)
            else:
                self.meta[data.keyword] = data
        else:
            raise Exception()
        return self

    def add_title(self, data):
        """Add a title"""
        self._titles.append(data.argument)

    def add_cumulative(self, data):
        """Add a cumulative argument into metadata"""
        if data.keyword not in self.meta:
            self.meta[data.keyword] = []
        self.meta[data.keyword].append(data)

    def get_data_argument(self, keyword, default):
        """Return `self.meta[keyword].argument`.

        Return `default` if `self.meta[keyword]` does not exist.

        If `self.meta[keyword]` is a list, return the list of `item.argument`
        for each item in the list.
        """
        if keyword not in self.meta:
            return default
        if isinstance(self.meta[keyword], list):
            return [item.argument for item in self.meta[keyword]]
        else:
            return self.meta[keyword].argument

    def add_subtitle(self, data):
        """Add a subtitle"""
        self._subtitles.append(data.argument)

    @property
    def titles(self):
        """Return the list of titles (and subtitles)."""
        return self._titles + self._subtitles

    def add_author(self, data):
        """Add an auhor."""
        self._authors.append(data.argument)

    @property
    def authors(self):
        """Return the list of (raw) authors."""
        return self._authors

    def add_key(self, data):
        """Add a new {key: foo: bar} directive."""
        key, *argument = data.argument.split(":")
        if 'morekeys' not in self.meta:
            self.meta['morekeys'] = []
        self.meta['morekeys'].append(Directive(
            key.strip(),
            ":".join(argument).strip(),
            ))

class EndOfLine(AST):
    """New line"""
    _template = "endofline"

class Directive(AST):
    """A directive"""

    def __init__(self, keyword, argument=None):
        super().__init__()
        self.keyword = directive_name(keyword.strip())
        self.argument = argument

    @property
    def _template(self):
        """Name of the template to use to render this keyword.

        This only applies if ``self.inline == True``
        """
        return self.keyword

    def __str__(self):
        return str(self.argument)

    @property
    def inline(self):
        """Return `True` iff `self` is an inline directive."""
        return self.keyword in INLINE_DIRECTIVES

class Define(Directive):
    """A chord definition.

    Attributes:

    .. attribute:: key
        The key, as a :class:`Chord` object.
    .. attribute:: basefret
        The base fret, as an integer. Can be `None` if no base fret is defined.
    .. attribute:: frets
        The list of frets, as a list of integers, or `None`, if this fret is not to be played.
    .. attribute:: fingers
        The list of fingers to use on frets, as a list of integers, or `None`
        if no information is given (this string is not played, or is played
        open). Can be `None` if not defined.
    """

    def __init__(self, key, basefret, frets, fingers):
        self.key = key
        self.basefret = basefret # Can be None
        self.frets = frets
        self.fingers = fingers # Can be None
        super().__init__("define", None)

    @property
    def pretty_key(self):
        """Return the key with nicer (utf8) alteration"""
        return self.key.chord.replace('&', '♭').replace('#', '♯')

    def __str__(self):
        return None

class Image(Directive):
    """An image

    .. attribute:: filename
        The filename of the image.
    .. attribute:: size
        An iterable of tuples ``(type, float, unit)``.
    """

    def __init__(self, filename, size=None):
        self.filename = filename
        if size is None:
            size = []
        self.size = size
        super().__init__("image", None)

class Tab(AST):
    """Tablature"""

    inline = True
    _template = "tablature"

    def __init__(self):
        super().__init__()
        self.content = []

    def prepend(self, data):
        """Add an element at the beginning of content."""
        self.content.insert(0, data)
        return self
