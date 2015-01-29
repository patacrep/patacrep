"""ChordPro lexer"""

import logging
import ply.lex as lex

LOGGER = logging.getLogger()

#pylint: disable=invalid-name
tokens = (
    'LBRACE',
    'RBRACE',
    'CHORD',
    'NEWLINE',
    'COLON',
    'WORD',
    'SPACE',
    'TEXT',
    'KEYWORD',
    'SOC',
    'EOC',
    'SOB',
    'EOB',
    'SOT',
    'EOT',
)

class ChordProLexer:
    """ChordPro Lexer class"""
    # pylint: disable=too-many-public-methods

    tokens = tokens

    states = (
        ('chord', 'exclusive'),
        ('directive', 'exclusive'),
        ('directiveargument', 'exclusive'),
        ('tablature', 'exclusive'),
        )

    t_SPACE = r'[ \t]+'

    t_chord_CHORD = r'[A-G7#m]+' # TODO This can be refined

    t_directive_SPACE = r'[ \t]+'
    t_directive_KEYWORD = r'[a-zA-Z_]+'
    t_directiveargument_TEXT = r'[^}]+'

    @staticmethod
    def t_SOC(token):
        r'{(soc|start_of_chorus)}'
        return token

    @staticmethod
    def t_EOC(token):
        r'{(eoc|end_of_chorus)}'
        return token

    @staticmethod
    def t_SOB(token):
        r'{(sob|start_of_bridge)}'
        return token

    @staticmethod
    def t_EOB(token):
        r'{(eob|end_of_bridge)}'
        return token

    def t_SOT(self, token):
        r'{(sot|start_of_tab)}'
        self.lexer.push_state('tablature')
        return token

    def t_tablature_EOT(self, token):
        r'{(eot|end_of_tab)}'
        self.lexer.pop_state()
        return token

    @staticmethod
    def t_tablature_SPACE(token):
        r'[ \t]+'
        return token

    t_tablature_TEXT = r'[^\n]+'
    t_tablature_NEWLINE = r'\n'

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
        r'[^{}\n\][\t ]+'
        return token

    def t_LBRACKET(self, __token):
        r'\['
        self.lexer.push_state('chord')

    def t_chord_RBRACKET(self, __token):
        r'\]'
        self.lexer.pop_state()

    def t_LBRACE(self, token):
        r'{'
        self.lexer.push_state('directive')
        return token

    def t_directive_RBRACE(self, token):
        r'}'
        self.lexer.pop_state()
        return token

    def t_directiveargument_RBRACE(self, token):
        r'}'
        self.lexer.pop_state()
        self.lexer.pop_state()
        return token

    def t_directive_COLON(self, token):
        r':'
        self.lexer.push_state('directiveargument')
        return token

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

    @staticmethod
    def t_tablature_error(token):
        """Manage errors"""
        LOGGER.error("Illegal character '{}' in tablature..".format(token.value[0]))
        token.lexer.skip(1)

    @staticmethod
    def t_directive_error(token):
        """Manage errors"""
        LOGGER.error("Illegal character '{}' in directive..".format(token.value[0]))
        token.lexer.skip(1)

    def t_directiveargument_error(self, token):
        """Manage errors"""
        return self.t_directive_error(token)
