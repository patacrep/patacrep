"""ChordPro lexer"""

import logging
import ply.lex as lex

LOGGER = logging.getLogger()

#pylint: disable=invalid-name
tokens = (
   #'LBRACKET',
   #'RBRACKET',
   'CHORD',
   'LBRACE',
   'RBRACE',
   'NEWLINE',
   #'COLON',
   'WORD',
   'SPACE',
   #'NUMBER',
)

class ChordProLexer:
    """ChordPro Lexer class"""

    tokens = tokens

    states = (
        ('chord', 'exclusive'),
        )

    t_LBRACE = r'{'
    t_RBRACE = r'}'
    t_SPACE = r'[ \t]+'
    #t_COLON = r':'
    t_chord_CHORD = r'[A-G7#m]+' # TODO This can be refined

    def __init__(self):
        self.__class__.lexer = lex.lex(module=self)

    # Define a rule so we can track line numbers
    @staticmethod
    def t_NEWLINE(token):
        r'[\n\r]'
        token.lexer.lineno += 1
        return token

    @staticmethod
    def t_COMMENT(token):
        r'\#.*'
        pass

    @staticmethod
    def t_WORD(token):
        r'[^\n\][\t ]+'
        return token

    def t_LBRACKET(self, token):
        r'\['
        self.lexer.push_state('chord')

    def t_chord_RBRACKET(self, token):
        r'\]'
        self.lexer.pop_state()

    #@staticmethod
    #def t_NUMBER(token):
    #    r'[0-9]+'
    #    token.value = int(token.value)
    #    return token

    @staticmethod
    def t_error(token):
        """Manage errors"""
        LOGGER.error("Illegal character '{}'".format(token.value[0]))
        token.lexer.skip(1)

    @staticmethod
    def t_chord_error(token):
        """Manage errors"""
        LOGGER.error("Illegal character '{}' in chord..".format(token.value[0]))
        token.lexer.skip(1)
