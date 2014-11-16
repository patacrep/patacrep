"""Very simple LaTeX parser"""

import logging
import ply.yacc as yacc

from patacrep.latex.lexer import tokens, SimpleLexer, SongLexer
from patacrep.latex import ast
from patacrep.errors import SongbookError
from patacrep.latex.detex import detex

LOGGER = logging.getLogger()

class ParsingError(SongbookError):
    """Parsing error."""

    def __init__(self, message):
        super().__init__(self)
        self.message = message

    def __str__(self):
        return self.message

# pylint: disable=line-too-long
class Parser:
    """LaTeX parser."""

    def __init__(self, filename=None):
        self.tokens = tokens
        self.ast = ast.AST
        self.ast.init_metadata()
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
        LOGGER.error(
            "Error in file {}, line {} at position {}.".format(
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

    @staticmethod
    def p_dictionary(symbols):
        """dictionary : identifier EQUAL braces dictionary_next
                      | identifier EQUAL error dictionary_next
        """
        if isinstance(symbols[3], ast.Expression):
            symbols[0] = {}
            symbols[0][symbols[1]] = symbols[3]
            symbols[0].update(symbols[4])
        else:
            raise ParsingError("Do enclose arguments between braces.")

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
        """titles_next : NEWLINE title titles_next
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
            module=Parser(),
            ).parse(
                string,
                lexer=SimpleLexer().lexer,
                )
        )

def parsesong(string, filename=None):
    """Parse song and return its metadata."""
    return detex(
        silent_yacc(module=Parser(filename)).parse(
            string,
            lexer=SongLexer().lexer,
            ).metadata
        )

