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
        LOGGER.error("Error in file {}, line {}:{}.".format(
            str(self.filename),
            token.lineno,
            self.__find_column(token),
            )
            )

    @staticmethod
    def p_expression(symbols):
        """expression : brackets expression
                      | braces expression
                      | command expression
                      | NEWLINE expression
                      | word expression
                      | SPACE expression
                      | empty
        """
        if len(symbols) == 3:
            if symbols[2] is None:
                symbols[0] = ast.Expression(symbols[1])
            else:
                symbols[0] = symbols[2].prepend(symbols[1])
        else:
            symbols[0] = None

    @staticmethod
    def p_empty(__symbols):
        """empty :"""
        return None

    @staticmethod
    def p_brackets(symbols):
        """brackets : LBRACKET expression RBRACKET"""
        symbols[0] = symbols[2]

    @staticmethod
    def p_braces(symbols):
        """braces : LBRACE expression COLON expression RBRACE"""
        symbols[0] = symbols[2]


def parsesong(string, filename=None):
    """Parse song and return its metadata."""
    return yacc.yacc(module=Parser(filename)).parse(
                     string,
                     lexer=ChordProLexer().lexer,
                     )
