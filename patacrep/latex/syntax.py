import ply.yacc as yacc
import inspect # TODO supprimer

from patacrep.latex.lexer import tokens, SimpleLexer, SongLexer
from patacrep.latex import ast
from patacrep.latex.detex import detex

class Parser:

    def __init__(self, filename=None):
        self.tokens = tokens
        self.ast = ast.AST
        self.ast.init_metadata()
        self.filename = filename

    def __find_column(self, token):
        last_cr = token.lexer.lexdata.rfind('\n',0,token.lexpos)
        if last_cr < 0:
            last_cr = 0
        column = (token.lexpos - last_cr) + 1
        return column

    def p_error(self, p):
        print("Erreur fichier {}, ligne {}, position {}.".format( # TODO
            str(self.filename),
            p.lineno,
            self.__find_column(p),
            )
            )

    def p_expression(self, p):
        """expression : brackets expression
                      | braces expression
                      | command expression
                      | NEWLINE expression
                      | beginsong expression
                      | word expression
                      | SPACE expression
                      | empty
        """
        if len(p) == 3:
            if p[2] is None:
                p[0] = ast.Expression(p[1])
            else:
                p[0] = p[2].prepend(p[1])
        else:
            p[0] = None

    def p_empty(self, p):
        """empty :"""
        return None

    def p_brackets(self, p):
        """brackets : LBRACKET expression RBRACKET"""
        p[0] = p[2]

    def p_braces(self, p):
        """braces : LBRACE expression RBRACE"""
        p[0] = p[2]

    def p_command(self, p):
        """command : COMMAND brackets_list braces_list"""
        p[0] = ast.Command(p[1], p[2], p[3])

    def p_brackets_list(self, p):
        """brackets_list : brackets brackets_list
                         | empty
        """
        if len(p) == 3:
            p[0] = p[2]
            p[0].insert(0, p[1])
        else:
            p[0] = []

    def p_braces_list(self, p):
        """braces_list : braces braces_list
                       | empty
        """
        if len(p) == 3:
            p[0] = p[2]
            p[0].insert(0, p[1])
        else:
            p[0] = []

    def p_word(self, p):
        """word : CHARACTER word_next
                | COMMA word_next
                | EQUAL word_next
        """
        p[0] = p[1] + p[2]

    def p_word_next(self, p):
        """word_next : CHARACTER word_next
                     | empty
        """
        if len(p) == 2:
            p[0] = ""
        else:
            p[0] = p[1] + p[2]

    def p_beginsong(self, p):
        """beginsong : BEGINSONG separator songbraces separator songbrackets"""
        self.ast.metadata["@titles"] = p[3]
        self.ast.metadata.update(p[5])

    def p_songbrackets(self, p):
        """songbrackets : SONG_LOPTIONS separator dictionary separator SONG_ROPTIONS
                        | empty
        """
        if len(p) == 6:
            p[0] = p[3]
        else:
            p[0] = {}

    def p_songbraces(self, p):
        """songbraces : SONG_LTITLE separator titles separator SONG_RTITLE
                      | empty
        """
        if len(p) == 6:
            p[0] = p[3]
        else:
            p[0] = []

    def p_dictionary(self, p):
        """dictionary : identifier EQUAL braces dictionary_next
                      | identifier EQUAL error dictionary_next
        """
        if isinstance(p[3], ast.Expression):
            p[0] = {}
            p[0][p[1]] = p[3]
            p[0].update(p[4])
        else:
            raise Exception("Do enclose arguments between braces.") # TODO

    def p_identifier(self, p):
        """identifier : CHARACTER identifier
                      | empty
        """
        if len(p) == 2:
            p[0] = ""
        else:
            p[0] = p[1] + p[2]

    def p_separator(self, p):
        """separator : SPACE
                     | empty
        """
        p[0] = None

    def p_dictonary_next(self, p):
        """dictionary_next : separator COMMA separator dictionary
                           | empty
        """
        if len(p) == 5:
            p[0] = p[4]
        else:
            p[0] = {}

    def p_titles(self, p):
        """titles : title titles_next"""
        p[0] = [p[1]] + p[2]

    def p_titles_next(self, p):
        """titles_next : NEWLINE title titles_next
                       | empty
        """
        if len(p) == 2:
            p[0] = []
        else:
            p[0] = [p[2]] + p[3]

    def p_title(self, p):
        """title : brackets title
                 | braces title
                 | command title
                 | word title
                 | SPACE title
                 | empty
        """
        if len(p) == 2:
            p[0] = None
        else:
            if p[2] is None:
                p[0] = ast.Expression(p[1])
            else:
                p[0] = p[2].prepend(p[1])


def tex2plain(string):
    return detex(yacc.yacc(module = Parser()).parse(string, lexer = SimpleLexer().lexer))

def parsesong(string, filename=None):
    return detex(yacc.yacc(module = Parser(filename)).parse(string, lexer = SongLexer().lexer).metadata)

