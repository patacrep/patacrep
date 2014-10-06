"""ChordPro lexer"""

import logging
import ply.lex as lex

LOGGER = logging.getLogger()

#pylint: disable=invalid-name
tokens = (
   'LBRACKET',
   'RBRACKET',
   'LBRACE',
   'RBRACE',
   'NEWLINE',
   'COLON',
   'WORD',
   'SPACE',
   'NUMBER'
)

class ChordProLexer:
    """ChordPro Lexer class"""

    tokens = tokens

    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_LBRACE = r'{'
    t_RBRACE = r'}'
    t_SPACE = r'[ \t]+'
    t_COLON = r':'
    t_WORD = r'[a-zA-Z_]+'  #TODO: handle unicode

    def __init__(self):
        self.__class__.lexer = lex.lex(module=self)

    # Define a rule so we can track line numbers
    @staticmethod
    def t_NEWLINE(token):
        r'[\n\r]'
        token.lexer.lineno += 1
        return token

    @staticmethod
    def t_comment(token):
        r'\#.*'
        pass
    
    @staticmethod
    def t_NUMBER(token):
        r'[0-9]+'
        token.value = int(token.value)
        return token

    @staticmethod
    def t_error(token):
        """Manage errors"""
        LOGGER.error("Illegal character '{}'".format(token.value[0]))
        token.lexer.skip(1)