"""Abstract Syntax Tree for ChordPro code."""

# pylint: disable=too-few-public-methods

import logging

LOGGER = logging.getLogger()

class OrderedLifoDict:
    """Ordered (LIFO) dictionary.

    Mimics the :class:`dict` dictionary, with:
    - dictionary is ordered: the order the keys are kept (as with
      :class:`collections.OrderedDict`), excepted that:
    - LIFO: the last item is reterned first when iterating.
    """

    def __init__(self, default=None):
        if default is None:
            self._keys = []
            self._values = {}
        else:
            self._keys = list(default.keys())
            self._values = default.copy()

    def values(self):
        """Same as :meth:`dict.values`."""
        for key in self:
            yield self._values[key]

    def __iter__(self):
        yield from self._keys

    def __setitem__(self, key, value):
        if key not in self._keys:
            self._keys.insert(0, key)
        self._values[key] = value

    def __getitem__(self, key):
        return self._values[key]

    def get(self, key, default=None):
        """Same as :meth:`dict.get`."""
        return self._values.get(key, default)

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
    }

def directive_name(text):
    """Return name of the directive, considering eventual shortcuts."""
    return DIRECTIVE_SHORTCUTS.get(text, text)


class AST:
    """Generic object representing elements of the song."""
    _template = None
    inline = False

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

    def __init__(self):
        super().__init__()
        self.line = []

    def prepend(self, data):
        """Add an object at the beginning of line."""
        self.line.insert(0, data)
        return self

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
        self.chords = chords

class Chord(AST):
    """A chord."""

    _template = "chord"

    def __init__(self, chord):
        # pylint: disable=too-many-arguments
        self.chord = chord

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
        - meta: Every other metadata.
        """

    #: Some directives are added to the song using special methods.
    METADATA_ADD = {
        "title": "add_title",
        "subtitle": "add_subtitle",
        "artist": "add_author",
        "key": "add_key",
        "define": "add_cumulative",
        "language": "add_cumulative",
        }

    def __init__(self, filename):
        super().__init__()
        self.content = []
        self.meta = OrderedLifoDict()
        self._authors = []
        self._titles = []
        self._subtitles = []
        self._keys = []
        self.filename = filename

    def add(self, data):
        """Add an element to the song"""
        if isinstance(data, Error):
            return self
        elif data is None:
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
            # methods listed in ``METADATA_ADD``.
            if data.keyword in self.METADATA_ADD:
                getattr(self, self.METADATA_ADD[data.keyword])(data)
            else:
                self.meta[data.keyword] = data
        else:
            raise Exception()
        return self

    def add_title(self, data):
        """Add a title"""
        self._titles.insert(0, data.argument)

    def add_cumulative(self, data):
        """Add a cumulative argument into metadata"""
        if data.keyword not in self.meta:
            self.meta[data.keyword] = []
        self.meta[data.keyword].insert(0, data)

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
        self._subtitles.insert(0, data.argument)

    @property
    def titles(self):
        """Return the list of titles (and subtitles)."""
        return self._titles + self._subtitles

    def add_author(self, data):
        """Add an auhor."""
        self._authors.insert(0, data.argument)

    @property
    def authors(self):
        """Return the list of (raw) authors."""
        return self._authors

    def add_key(self, data):
        """Add a new {key: foo: bar} directive."""
        key, *argument = data.argument.split(":")
        if 'keys' not in self.meta:
            self.meta['keys'] = []
        self.meta['keys'].insert(0, Directive(
            key.strip(),
            ":".join(argument).strip(),
            ))

class Newline(AST):
    """New line"""
    _template = "newline"

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

    @property
    def inline(self):
        """True iff this directive is to be rendered in the flow on the song.
        """
        return self.keyword in INLINE_PROPERTIES

    def __str__(self):
        return self.argument

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

    def __str__(self):
        return None

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
