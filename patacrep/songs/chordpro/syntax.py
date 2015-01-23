# -*- coding: utf-8 -*-
"""ChordPro parser"""

import logging
import ply.yacc as yacc

from patacrep.songs.chordpro.lexer import tokens, ChordProLexer
from patacrep.songs.chordpro import ast
from patacrep.errors import SongbookError

LOGGER = logging.getLogger()

class ParsingError(SongbookError):
    """Parsing error."""

    def __init__(self, message):
        super().__init__(self)
        self.message = message

    def __str__(self):
        return self.message


class Parser:
    """ChordPro parser class"""

    def __init__(self, filename=None):
        self.tokens = tokens
        self.filename = filename

    @staticmethod
    def __find_column(token):
        """Return the column of ``token``."""
        last_cr = token.lexer.lexdata.rfind('\n', 0, token.lexpos)
        if last_cr < 0:
            last_cr = 0
        column = (token.lexpos - last_cr) + 1
        return column

    def p_error(self, token):
        """Manage parsing errors."""
        if token: # TODO remove this test
            LOGGER.error("Error in file {}, line {}:{}.".format(
                str(self.filename),
                token.lineno,
                self.__find_column(token),
                )
                )

    @staticmethod
    def p_song(symbols):
        """song : block song
                | empty
        """
        if len(symbols) == 2:
            symbols[0] = ('song')
        else:
            symbols[0] = ('song', symbols[1], symbols[2])

    @staticmethod
    def p_block(symbols):
        """block : directive NEWLINE newlines
                 | stanza NEWLINE newlines
        """
        symbols[0] = ('block', symbols[1])

    @staticmethod
    def p_newlines(symbols):
        """newlines : NEWLINE newlines
                    | empty"""
        symbols[0] = ('newlines')

    @staticmethod
    def p_directive(symbols):
        """directive : LBRACE WORD RBRACE"""
        symbols[0] = ('directive', symbols[1])

    @staticmethod
    def p_line(symbols):
        """line : WORD line_next
                | CHORD line_next
                | SPACE line_next
        """
        symbols[0] = ('line', symbols[1], symbols[2])

    @staticmethod
    def p_line_next(symbols):
        """line_next : WORD line_next
                     | SPACE line_next
                     | CHORD line_next
                     | empty
        """
        if len(symbols) == 2:
            symbols[0] = ('line-next')
        else:
            symbols[0] = ('line-next', symbols[1], symbols[2])

    @staticmethod
    def p_stanza(symbols):
        """stanza : line NEWLINE stanza_next
        """
        symbols[0] = ('stanza', symbols[1], symbols[3])

    @staticmethod
    def p_stanza_next(symbols):
        """stanza_next : line NEWLINE stanza_next
                       | empty
        """
        if len(symbols) == 2:
            symbols[0] = ('stanza-next')
        else:
            symbols[0] = ('stanza-next', symbols[1], symbols[3])

    #@staticmethod
    #def p_braces(symbols):
    #    """braces : LBRACE expression COLON expression RBRACE"""
    #    symbols[0] = symbols[2]

    @staticmethod
    def p_empty(symbols):
        """empty :"""
        symbols[0] = None

    #@staticmethod
    #def p_comment(symbols):
    #    """comment : COMMENT"""
    #    symbols[0] = ('comment', symbols[1])



def parse_song(content, filename=None):
    """Parse song and return its metadata."""
    return yacc.yacc(module=Parser(filename)).parse(
                     content,
                     lexer=ChordProLexer().lexer,
                     )
