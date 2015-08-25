"""ChordPro parser"""

import logging
import ply.yacc as yacc
import re

from patacrep.songs.syntax import Parser
from patacrep.songs.chordpro import ast
from patacrep.songs.chordpro.lexer import tokens, ChordProLexer

LOGGER = logging.getLogger()

CHORD_RE = re.compile(
    r"""
        (?P<key>[A-G])
        (?P<alteration>[b#])?
        (?P<modifier>(maj|sus|dim|m))?
        (?P<addnote>[2-9])?
        (
            /
            (?P<basskey>[A-G])
            (?P<bassalteration>[b#])?
        )?
    """,
    re.VERBOSE
    )

def _parse_chords(string):
    """Parse a list of chords.

    Iterate over :class:`ast.Chord` objects.
    """
    for chord in string.split():
        match = CHORD_RE.match(chord)
        if match is None:
            TODO
        yield ast.Chord(**match.groupdict())

def _parse_define(key, basefret, frets, fingers):
    """Parse a `{define: KEY base-fret BASE frets FRETS fingers FINGERS}` directive

    Return a :class:`ast.Define` object.
    """
    # pylint: disable=too-many-branches
    key = list(_parse_chords(key))
    if len(key) != 1:
        TODO
    else:
        processed_key = key[0]

    if basefret is None:
        processed_basefret = None
    else:
        processed_basefret = int(basefret)

    if frets is None:
        processed_frets = None
    else:
        processed_frets = []
        for fret in frets.split():
            if fret == "x":
                processed_frets.append(None)
            else:
                processed_frets.append(int(fret))

    if fingers is None:
        processed_fingers = None
    else:
        processed_fingers = []
        for finger in fingers.split():
            if finger == '-':
                processed_fingers.append(None)
            else:
                processed_fingers.append(int(finger))

    return ast.Define(
        key=processed_key,
        basefret=processed_basefret,
        frets=processed_frets,
        fingers=processed_fingers,
        )

class ChordproParser(Parser):
    """ChordPro parser class"""
    # pylint: disable=too-many-public-methods

    start = "song"

    def __init__(self, filename=None):
        super().__init__()
        self.tokens = tokens
        self.filename = filename

    def p_song(self, symbols):
        """song : block song
                | empty
        """
        if len(symbols) == 2:
            symbols[0] = ast.Song(self.filename)
        else:
            symbols[0] = symbols[2].add(symbols[1])

    @staticmethod
    def p_block(symbols):
        """block : SPACE block
                 | directive NEWLINE
                 | line NEWLINE
                 | chorus NEWLINE
                 | tab NEWLINE
                 | bridge NEWLINE
                 | NEWLINE
        """
        if len(symbols) == 3 and isinstance(symbols[1], str):
            symbols[0] = symbols[2]
        elif (symbols[1] is None) or (len(symbols) == 2):
            symbols[0] = None
        else:
            symbols[0] = symbols[1]

    @staticmethod
    def p_maybespace(symbols):
        """maybespace : SPACE
                      | empty
        """
        symbols[0] = None

    @staticmethod
    def p_directive(symbols):
        """directive : LBRACE KEYWORD directive_next RBRACE
                     | LBRACE SPACE KEYWORD directive_next RBRACE
        """
        if len(symbols) == 5:
            symbols[3].keyword = symbols[2]
            symbols[0] = symbols[3]
        else:
            symbols[4].keyword = symbols[3]
            symbols[0] = symbols[4]
        if symbols[0].keyword == 'define':
            match = re.compile(
                r"""
                    (?P<key>[^\ ]*)\ *
                    (base-fret\ *(?P<basefret>[2-9]))?\ *
                    frets\ *(?P<frets>((\d+|x)\ *)+)\ *
                    (fingers\ *(?P<fingers>(([0-4-])\ *)*))?
                """,
                re.VERBOSE
                ).match(symbols[0].argument)

            if match is None:
                TODO

            symbols[0] = _parse_define(**match.groupdict())

    @staticmethod
    def p_directive_next(symbols):
        """directive_next : SPACE COLON TEXT
                          | COLON TEXT
                          | empty
        """
        symbols[0] = ast.Directive()
        if len(symbols) == 3:
            symbols[0].argument = symbols[2].strip()
        elif len(symbols) == 4:
            symbols[0].argument = symbols[3].strip()

    @staticmethod
    def p_line(symbols):
        """line : word line_next
                | chord line_next
        """
        symbols[0] = symbols[2].prepend(symbols[1])

    @staticmethod
    def p_line_next(symbols):
        """line_next : word line_next
                     | space line_next
                     | chord line_next
                     | empty
        """
        if len(symbols) == 2:
            symbols[0] = ast.Line()
        else:
            symbols[0] = symbols[2].prepend(symbols[1])

    @staticmethod
    def p_word(symbols):
        """word : WORD"""
        symbols[0] = ast.Word(symbols[1])

    @staticmethod
    def p_space(symbols):
        """space : SPACE"""
        symbols[0] = ast.Space()

    @staticmethod
    def p_chord(symbols):
        """chord : CHORD"""
        symbols[0] = ast.ChordList(*_parse_chords(symbols[1]))

    @staticmethod
    def p_chorus(symbols):
        """chorus : SOC maybespace NEWLINE chorus_content EOC maybespace
        """
        symbols[0] = symbols[4]

    @staticmethod
    def p_chorus_content(symbols):
        """chorus_content : line NEWLINE chorus_content
                          | SPACE chorus_content
                          | empty
        """
        if len(symbols) == 2:
            symbols[0] = ast.Chorus()
        elif len(symbols) == 3:
            symbols[0] = symbols[2]
        else:
            symbols[0] = symbols[3].prepend(symbols[1])

    @staticmethod
    def p_bridge(symbols):
        """bridge : SOB maybespace NEWLINE bridge_content EOB maybespace
        """
        symbols[0] = symbols[4]

    @staticmethod
    def p_bridge_content(symbols):
        """bridge_content : line NEWLINE bridge_content
                          | SPACE bridge_content
                          | empty
        """
        if len(symbols) == 2:
            symbols[0] = ast.Bridge()
        elif len(symbols) == 3:
            symbols[0] = symbols[2]
        else:
            symbols[0] = symbols[3].prepend(symbols[1])


    @staticmethod
    def p_tab(symbols):
        """tab : SOT maybespace NEWLINE tab_content EOT maybespace
        """
        symbols[0] = symbols[4]

    @staticmethod
    def p_tab_content(symbols):
        """tab_content : NEWLINE tab_content
                       | TEXT tab_content
                       | SPACE tab_content
                       | empty
        """
        if len(symbols) == 2:
            symbols[0] = ast.Tab()
        else:
            if symbols[1].strip():
                symbols[2].prepend(symbols[1])
            symbols[0] = symbols[2]

    @staticmethod
    def p_empty(symbols):
        """empty :"""
        symbols[0] = None

def parse_song(content, filename=None):
    """Parse song and return its metadata."""
    return yacc.yacc(
        module=ChordproParser(filename),
        debug=0,
        write_tables=0,
        ).parse(
            content,
            lexer=ChordProLexer().lexer,
            )
