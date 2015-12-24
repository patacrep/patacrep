"""ChordPro parser"""

import functools
import logging
import re

import ply.yacc as yacc

from patacrep.content import ContentError
from patacrep.songs.chordpro import ast
from patacrep.songs.chordpro.lexer import tokens, ChordProLexer
from patacrep.songs.syntax import Parser

LOGGER = logging.getLogger()

class ChordproParser(Parser):
    """ChordPro parser class"""
    # pylint: disable=too-many-public-methods

    start = "song"

    def __init__(self, filename=None):
        super().__init__()
        self.tokens = tokens
        self.filename = filename
        self._directives = []
        self.parser = yacc.yacc(
            module=self,
            debug=0,
            write_tables=0,
            )

    def parse(self, content, *, lexer):
        """Parse file

        This is a shortcut to `yacc.yacc(...).parse()`. The arguments are
        transmitted to this method.
        """
        lexer = ChordProLexer(filename=self.filename).lexer
        ast.AST.lexer = lexer
        return self.parser.parse(content, lexer=lexer)

    def p_song(self, symbols):
        """song : block song
                | empty
        """
        if len(symbols) == 2:
            symbols[0] = ast.Song(
                self.filename,
                directives=self._directives,
                errors=self._errors,
                )
        else:
            symbols[0] = symbols[2].add(symbols[1])

    @staticmethod
    def p_block(symbols):
        """block : SPACE block
                 | line ENDOFLINE
                 | line_error ENDOFLINE
                 | chorus ENDOFLINE
                 | tab ENDOFLINE
                 | bridge ENDOFLINE
                 | ENDOFLINE
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
                if fret in "xX":
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
                    (base-fret\ *(?P<basefret>\d{1,2}))?\ *
                    frets\ *(?P<frets>((\d+|x|X)\ *)+)\ *
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

            define = self._parse_define(match.groupdict())
            if define is None:
                self.error(
                    line=symbols.lexer.lineno,
                    message="Invalid chord definition '{}'.".format(argument),
                    )
                symbols[0] = ast.Error()
                return
            self._directives.append(define)

        else:
            directive = ast.Directive(keyword, argument)
            if directive.inline:
                symbols[0] = directive
            else:
                self._directives.append(directive)


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

    def p_line_error(self, symbols):
        """line_error : error directive"""
        self.error(
            line=symbols.lexer.lineno,
            message="Directive can only be preceded or followed by spaces",
            )
        symbols[0] = ast.Line()

    @staticmethod
    def p_line(symbols):
        """line : word line_next
                | chord line_next
                | directive maybespace
        """
        if isinstance(symbols[2], ast.Line):
            # Line with words, etc.
            symbols[0] = symbols[2].prepend(symbols[1])
        else:
            # Directive
            if symbols[1] is None:
                # Meta directive. Nothing to do
                symbols[0] = ast.Line()
            else:
                # Inline directive
                symbols[0] = ast.Line(symbols[1])

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
        """chorus : SOC maybespace ENDOFLINE chorus_content EOC maybespace
        """
        symbols[0] = symbols[4]

    @staticmethod
    def p_chorus_content(symbols):
        """chorus_content : line ENDOFLINE chorus_content
                          | line_error ENDOFLINE chorus_content
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
        """bridge : SOB maybespace ENDOFLINE bridge_content EOB maybespace
        """
        symbols[0] = symbols[4]

    @staticmethod
    def p_bridge_content(symbols):
        """bridge_content : line ENDOFLINE bridge_content
                          | line_error ENDOFLINE bridge_content
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
        """tab : SOT maybespace ENDOFLINE tab_content EOT maybespace
        """
        symbols[0] = symbols[4]

    @staticmethod
    def p_tab_content(symbols):
        """tab_content : ENDOFLINE tab_content
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

    def p_error(self, token):
        super().p_error(token)
        while True:
            token = self.parser.token()
            if not token or token.type == "ENDOFLINE":
                break
        if token:
            self.parser.errok()
        return token

def parse_song(content, filename=None):
    """Parse song and return its metadata."""
    parser = ChordproParser(filename)
    parsed_content = parser.parse(
        content,
        lexer=ChordProLexer(filename=filename).lexer,
        )
    if parsed_content is None:
        raise ContentError(message='Fatal error during song parsing.')
    return parsed_content
