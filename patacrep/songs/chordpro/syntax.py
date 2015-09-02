"""ChordPro parser"""

import ply.yacc as yacc
import re

from patacrep.songs.syntax import Parser
from patacrep.songs.chordpro import ast
from patacrep.songs.chordpro.lexer import tokens, ChordProLexer

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
    def _parse_define(groups):
        """Parse a `{define: KEY base-fret BASE frets FRETS fingers FINGERS}` directive

        Return a :class:`ast.Define` object.
        """
        # pylint: disable=too-many-branches
        if not groups['key'].strip():
            return None
        else:
            key = ast.Chord(groups['key'].strip())

        if groups['basefret'] is None:
            basefret = None
        else:
            basefret = int(groups['basefret'])

        if groups['frets'] is None:
            frets = None
        else:
            frets = []
            for fret in groups['frets'].split():
                if fret == "x":
                    frets.append(None)
                else:
                    frets.append(int(fret))

        if groups['fingers'] is None:
            fingers = None
        else:
            fingers = []
            for finger in groups['fingers'].split():
                if finger == '-':
                    fingers.append(None)
                else:
                    fingers.append(int(finger))

        return ast.Define(
            key=key,
            basefret=basefret,
            frets=frets,
            fingers=fingers,
            )

    def p_directive(self, symbols):
        """directive : LBRACE KEYWORD directive_next RBRACE
                     | LBRACE SPACE KEYWORD directive_next RBRACE
        """
        if len(symbols) == 5:
            keyword = symbols[2]
            argument = symbols[3]
        else:
            keyword = symbols[3]
            argument = symbols[4]

        if keyword == "define":
            match = re.compile(
                r"""
                    ^
                    (?P<key>[^\ ]*)\ *
                    (base-fret\ *(?P<basefret>[2-9]))?\ *
                    frets\ *(?P<frets>((\d+|x)\ *)+)\ *
                    (fingers\ *(?P<fingers>(([0-4-])\ *)*))?
                    $
                """,
                re.VERBOSE
                ).match(argument)

            if match is None:
                if argument.strip():
                    self.error(
                        line=symbols.lexer.lineno,
                        message="Invalid chord definition '{}'.".format(argument),
                        )
                else:
                    self.error(
                        line=symbols.lexer.lineno,
                        message="Invalid empty chord definition.",
                        )
                symbols[0] = ast.Error()
                return

            symbols[0] = self._parse_define(match.groupdict())
            if symbols[0] is None:
                self.error(
                    line=symbols.lexer.lineno,
                    message="Invalid chord definition '{}'.".format(argument),
                    )
                symbols[0] = ast.Error()

        else:
            symbols[0] = ast.Directive(keyword, argument)

    @staticmethod
    def p_directive_next(symbols):
        """directive_next : SPACE COLON TEXT
                          | COLON TEXT
                          | COLON
                          | empty
        """
        if len(symbols) == 3:
            symbols[0] = symbols[2].strip()
        elif len(symbols) == 4:
            symbols[0] = symbols[3].strip()
        elif len(symbols) == 2 and symbols[1] == ":":
            symbols[0] = ""
        else:
            symbols[0] = None

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
        symbols[0] = ast.ChordList(*[ast.Chord(chord) for chord in symbols[1].split()])

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
