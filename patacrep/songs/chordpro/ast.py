# -*- coding: utf-8 -*-
"""Abstract Syntax Tree for ChordPro code."""

import functools

def _indent(string):
    return "\n".join(["  {}".format(line) for line in string.split('\n')])

INLINE_PROPERTIES = {
    "lilypond",
    "comment",
    "guitar_comment",
    "image",
    }

DIRECTIVE_SHORTCUTS = {
    "t": "title",
    "st": "subtitle",
    "a": "album",
    "by": "artist",
    "c": "comment",
    "gc": "guitar_comment",
    }

def directive_name(text):
    if text in DIRECTIVE_SHORTCUTS:
        return DIRECTIVE_SHORTCUTS[text]
    return text


class AST:
    inline = False

class Line(AST):
    """A line is a sequence of (possibly truncated) words, spaces and chords."""

    def __init__(self):
        super().__init__()
        self.line = []

    def prepend(self, data):
        self.line.insert(0, data)
        return self

    def __str__(self):
        return "".join([str(item) for item in self.line])

    def strip(self):
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

    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return self.value

class Space(LineElement):
    """A space between words"""

    def __init__(self):
        super().__init__()

    def __str__(self):
        return " "

class Chord(LineElement):
    """A chord."""

    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return "[{}]".format(self.value)

class Verse(AST):
    """A verse (or bridge, or chorus)"""
    type = "verse"
    inline = True

    def __init__(self, block=None):
        super().__init__()
        self.lines = [] # TODO check block

    def prepend(self, data):
        self.lines.insert(0, data)
        return self

    def __str__(self):
        return '{{start_of_{type}}}\n{content}\n{{end_of_{type}}}'.format(
                type = self.type,
                content = _indent("\n".join([str(line) for line in self.lines])),
                )

class Chorus(Verse):
    type = 'chorus'

class Bridge(Verse):
    type = 'bridge'

class Song(AST):
    """A song"""

    METADATA_TYPE = {
        "title": "add_title",
        "subtitle": "add_subtitle",
        "language": "add_language",
        "artist": "add_author",
        }

    def __init__(self):
        super().__init__()
        self.content = []
        self.meta = []
        self._authors = []
        self._titles = []
        self._subtitles = []
        self._languages = set()

    def add(self, data):
        if data is None:
            if not (self.content and isinstance(self.content[0], Newline)):
                self.content.insert(0, Newline())
        elif isinstance(data, Line):
            if not (self.content and isinstance(self.content[0], Verse)):
                self.content.insert(0, Verse())
            self.content[0].prepend(data.strip())
        elif data.inline:
            self.content.insert(0, data)
        elif isinstance(data, Directive):
            name = directive_name(data.keyword)
            if name in self.METADATA_TYPE:
                getattr(self, self.METADATA_TYPE[name])(*data.as_tuple)
            else:
                self.meta.append(data)
        else:
            raise Exception()
        return self

    def str_meta(self):
        for title in self.titles:
            yield "{{title: {}}}".format(title)
        for language in sorted(self.languages):
            yield "{{language: {}}}".format(language)
        for author in self.authors:
            yield "{{by: {}}}".format(author)
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
        self._titles.insert(0, title)

    def add_subtitle(self, __ignored, title):
        self._subtitles.insert(0, title)

    @property
    def titles(self):
        return self._titles + self._subtitles

    def add_author(self, __ignored, title):
        self._authors.insert(0, title)

    @property
    def authors(self):
        return self._authors

    def add_language(self, __ignored, language):
        self._languages.add(language)

    @property
    def languages(self):
        return self._languages



class Newline(AST):
    def __str__(self):
        return ""

@functools.total_ordering
class Directive(AST):
    """A directive"""

    def __init__(self):
        super().__init__()
        self.keyword = ""
        self.argument = None

    @property
    def keyword(self):
        return self._keyword

    @property
    def inline(self):
        return self.keyword in INLINE_PROPERTIES

    @keyword.setter
    def keyword(self, value):
        self._keyword = value.strip()

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
        self.content.insert(0, data)
        return self

    def __str__(self):
        return '{{start_of_tab}}\n{}\n{{end_of_tab}}'.format(
                _indent("\n".join(self.content)),
                )

