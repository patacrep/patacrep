"""ChordPro lexer"""

import functools
import logging

import ply.lex as lex

from patacrep.songs import errors

LOGGER = logging.getLogger()

#pylint: disable=invalid-name
tokens = (
    'LBRACE',
    'RBRACE',
    'ENDOFLINE',
    'COLON',
    'WORD',
    'SPACE',
    'CHORD',
    'TEXT',
    'KEYWORD',
    'SOC',
    'EOC',
    'SOB',
    'EOB',
    'SOT',
    'EOT',
    'SE',
    'EE',
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

    t_chord_CHORD = r'[^\]]+'

    t_directive_SPACE = r'[ \t]+'
    t_directive_KEYWORD = r'[a-zA-Z_]+'
    t_directiveargument_TEXT = r'[^\\}]+'

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

    @staticmethod
    def t_SE(token):
        r'{(se|start_echo)}'
        return token

    @staticmethod
    def t_EE(token):
        r'{(ee|end_echo)}'
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

    t_tablature_TEXT = r'[^\n\r]+'
    t_tablature_ENDOFLINE = r'\r?\n'

    def __init__(self, *, filename=None):
        self.__class__.lexer = lex.lex(module=self)
        self.error_builders = []
        self.filename = filename

    # Define a rule so we can track line numbers
    @staticmethod
    def t_ENDOFLINE(token):
        r'\r?\n'
        token.lexer.lineno += 1
        return token

    @staticmethod
    def t_COMMENT(token):
        r'\#.*'
        pass

    @staticmethod
    def t_WORD(token):
        r'[^{}\\\r\n\]\[\t ]+'
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
    def t_ESCAPED(token):
        r'\\[{} #\\]'
        token.value = token.value[1]
        token.type = "WORD"
        return token

    @staticmethod
    def t_directiveargument_ESCAPED(token):
        r'\\[{} #\\]'
        token.value = token.value[1]
        token.type = "TEXT"
        return token

    def error(self, token, more=""):
        """Display error message, and skip illegal token."""
        message = "Illegal character '{char}'{more}.".format(
            char=token.value[0],
            more=more,
            )
        self.error_builders.append(functools.partial(
            errors.SongSyntaxError,
            line=token.lexer.lineno,
            message=message,
        ))
        if self.filename is not None:
            message = "Song {}, line {}: {}".format(self.filename, token.lexer.lineno, message)
        else:
            message = "Line {}: {}".format(token.lexer.lineno, message)
        LOGGER.warning(message)
        token.lexer.skip(1)

    def t_error(self, token):
        """Manage errors"""
        self.error(token)

    def t_chord_error(self, token):
        """Manage errors"""
        self.error(token, more=" in chord")

    def t_tablature_error(self, token):
        """Manage errors"""
        self.error(token, more=" in tablature")

    def t_directive_error(self, token):
        """Manage errors"""
        self.error(token, more=" in directive")

    def t_directiveargument_error(self, token):
        """Manage errors"""
        return self.t_directive_error(token)
