"""Very simple LaTeX lexer."""

import logging
import ply.lex as lex

LOGGER = logging.getLogger()

#pylint: disable=invalid-name
tokens = (
    'LBRACKET',
    'RBRACKET',
    'LBRACE',
    'RBRACE',
    'COMMAND',
    'ENDOFLINE',
    'COMMA',
    'EQUAL',
    'CHARACTER',
    'SPACE',
    'BEGINSONG',
    'SONG_LTITLE',
    'SONG_RTITLE',
    'SONG_LOPTIONS',
    'SONG_ROPTIONS',
)

class SimpleLexer:
    """Very simple LaTeX lexer."""

    tokens = tokens

    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_LBRACE = r'{'
    t_RBRACE = r'}'
    t_COMMAND = r'\\([@a-zA-Z]+|[^\\])'
    t_ENDOFLINE = r'\\\\'
    SPECIAL_CHARACTERS = (
        t_LBRACKET +
        t_RBRACKET +
        t_RBRACE +
        t_LBRACE +
        r"\\" +
        r" " +
        r"\n" +
        r"\r" +
        r"%" +
        r"=" +
        r","
        )
    t_CHARACTER = r'[^{}]'.format(SPECIAL_CHARACTERS)
    t_EQUAL = r'='
    t_COMMA = r','

    t_SPACE = r'[ \t\n\r]+'

    def __init__(self):
        self.__class__.lexer = lex.lex(module=self)

    # Define a rule so we can track line numbers
    @staticmethod
    def t_endofline(token):
        r'(\r?\n)+'
        token.lexer.lineno += len(token.value)

    @staticmethod
    def t_comment(token):
        r'%.*'
        pass

    # Error handling rule
    @staticmethod
    def t_error(token):
        """Manage errors"""
        LOGGER.warning("Illegal character '{}'".format(token.value[0]))
        token.lexer.skip(1)

class SongLexer(SimpleLexer):
    r"""Very simple song lexer.

    In the context of this class, a "song" is some LaTeX code containing the
    ``\beginsong`` (or ``\sortassong``) command.
    """

    states = (
        ('beginsong', 'inclusive'),
        )

    # State beginsong
    @staticmethod
    def t_INITIAL_BEGINSONG(token):
        r'(\\beginsong|\\sortassong)'
        token.lexer.push_state('beginsong')
        token.lexer.open_brackets = 0
        token.lexer.open_braces = 0
        return token

    @staticmethod
    def t_beginsong_LBRACKET(token):
        r'\['
        if token.lexer.open_brackets == 0:
            token.type = 'SONG_LOPTIONS'

            # Count opening and closing braces to know when to leave the
            # `beginsong` state.
            token.lexer.open_braces += 1
        token.lexer.open_brackets += 1
        return token

    @staticmethod
    def t_beginsong_RBRACKET(token):
        r'\]'
        token.lexer.open_brackets -= 1
        if token.lexer.open_brackets == 0:
            token.type = 'SONG_ROPTIONS'
            token.lexer.open_braces -= 1
            token.lexer.pop_state()
            for __ignored in token.lexer:
                # In this parser, we only want to read metadata. So, after the
                # first ``\beginsong`` command, we can stop parsing.
                pass
        return token

    @staticmethod
    def t_beginsong_LBRACE(token):
        r'{'
        if token.lexer.open_braces == 0:
            token.type = 'SONG_LTITLE'
        token.lexer.open_braces += 1
        return token

    @staticmethod
    def t_beginsong_RBRACE1(token):
        r'}(?![ \t\r\n]*\[)'
        token.lexer.open_braces -= 1
        token.type = 'RBRACE'
        if token.lexer.open_braces == 0:
            token.lexer.pop_state()
            token.type = 'SONG_RTITLE'
        return token

    @staticmethod
    def t_beginsong_RBRACE2(token):
        r'}(?=[ \t\r\n]*\[)'
        token.lexer.open_braces -= 1
        token.type = 'RBRACE'
        if token.lexer.open_braces == 0:
            token.type = 'SONG_RTITLE'
        return token

