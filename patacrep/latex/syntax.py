"""Very simple LaTeX parser"""

import logging
import ply.yacc as yacc

from patacrep.latex import ast
from patacrep.latex.detex import detex
from patacrep.latex.lexer import tokens, SimpleLexer, SongLexer
from patacrep.songs.syntax import Parser

LOGGER = logging.getLogger()

# pylint: disable=line-too-long
class LatexParser(Parser):
    """LaTeX parser."""

    def __init__(self, filename=None):
        super().__init__()
        self.tokens = tokens
        self.ast = ast.AST
        self.ast.init_metadata()
        self.filename = filename

    @staticmethod
    def p_expression(symbols):
        """expression : brackets expression
                      | braces expression
                      | command expression
                      | ENDOFLINE expression
                      | beginsong expression
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
        """braces : LBRACE expression RBRACE"""
        symbols[0] = symbols[2]

    @staticmethod
    def p_command(symbols):
        """command : COMMAND brackets_list braces_list"""
        symbols[0] = ast.Command(symbols[1], symbols[2], symbols[3])

    @staticmethod
    def p_brackets_list(symbols):
        """brackets_list : brackets brackets_list
                         | empty
        """
        if len(symbols) == 3:
            symbols[0] = symbols[2]
            symbols[0].insert(0, symbols[1])
        else:
            symbols[0] = []

    @staticmethod
    def p_braces_list(symbols):
        """braces_list : braces braces_list
                       | empty
        """
        if len(symbols) == 3:
            symbols[0] = symbols[2]
            symbols[0].insert(0, symbols[1])
        else:
            symbols[0] = []

    @staticmethod
    def p_word(symbols):
        """word : CHARACTER word_next
                | COMMA word_next
                | EQUAL word_next
        """
        symbols[0] = symbols[1] + symbols[2]

    @staticmethod
    def p_word_next(symbols):
        """word_next : CHARACTER word_next
                     | empty
        """
        if len(symbols) == 2:
            symbols[0] = ""
        else:
            symbols[0] = symbols[1] + symbols[2]

    def p_beginsong(self, symbols):
        """beginsong : BEGINSONG separator songbraces separator songbrackets"""
        self.ast.metadata["@titles"] = symbols[3]
        self.ast.metadata.update(symbols[5])

    @staticmethod
    def p_songbrackets(symbols):
        """songbrackets : SONG_LOPTIONS separator dictionary separator SONG_ROPTIONS
                        | empty
        """
        if len(symbols) == 6:
            symbols[0] = symbols[3]
        else:
            symbols[0] = {}

    @staticmethod
    def p_songbraces(symbols):
        """songbraces : SONG_LTITLE separator titles separator SONG_RTITLE
                      | empty
        """
        if len(symbols) == 6:
            symbols[0] = symbols[3]
        else:
            symbols[0] = []

    def p_dictionary(self, symbols):
        """dictionary : identifier EQUAL braces dictionary_next
                      | identifier EQUAL error dictionary_next
                      | empty
        """
        symbols[0] = {}
        if len(symbols) == 2:
            pass
        elif isinstance(symbols[3], ast.Expression):
            symbols[0][symbols[1]] = symbols[3]
            symbols[0].update(symbols[4])
        else:
            self.error(
                line=symbols.lexer.lineno,
                message="Argument '{}' should be enclosed between braces.".format(symbols[1]),
                )

    @staticmethod
    def p_identifier(symbols):
        """identifier : CHARACTER identifier
                      | empty
        """
        if len(symbols) == 2:
            symbols[0] = ""
        else:
            symbols[0] = symbols[1] + symbols[2]

    @staticmethod
    def p_separator(symbols):
        """separator : SPACE
                     | empty
        """
        symbols[0] = None

    @staticmethod
    def p_dictonary_next(symbols):
        """dictionary_next : separator COMMA separator dictionary
                           | empty
        """
        if len(symbols) == 5:
            symbols[0] = symbols[4]
        else:
            symbols[0] = {}

    @staticmethod
    def p_titles(symbols):
        """titles : title titles_next"""
        symbols[0] = [symbols[1]] + symbols[2]

    @staticmethod
    def p_titles_next(symbols):
        """titles_next : ENDOFLINE title titles_next
                       | empty
        """
        if len(symbols) == 2:
            symbols[0] = []
        else:
            symbols[0] = [symbols[2]] + symbols[3]

    @staticmethod
    def p_title(symbols):
        """title : brackets title
                 | braces title
                 | command title
                 | word title
                 | SPACE title
                 | empty
        """
        if len(symbols) == 2:
            symbols[0] = None
        else:
            if symbols[2] is None:
                symbols[0] = ast.Expression(symbols[1])
            else:
                symbols[0] = symbols[2].prepend(symbols[1])

def silent_yacc(*args, **kwargs):
    """Call yacc, suppressing (as far as possible) output and generated files.
    """
    return yacc.yacc(
        write_tables=0,
        debug=0,
        *args,
        **kwargs
        )

def tex2plain(string):
    """Parse string and return its plain text version."""
    return detex(
        silent_yacc(
            module=LatexParser(),
            ).parse(
                string,
                lexer=SimpleLexer().lexer,
                )
        )

def parse_song(content, filename=None):
    """Parse some LaTeX code, expected to be a song.

    Arguments:
    - content: the code to parse.
    - filename: the name of file where content was read from. Used only to
      display error messages.
    """
    return detex(
        silent_yacc(module=LatexParser(filename)).parse(
            content,
            lexer=SongLexer().lexer,
            ).metadata
        )
