import ply.lex as lex

tokens = (
   'LBRACKET',
   'RBRACKET',
   'LBRACE',
   'RBRACE',
   'COMMAND',
   'NEWLINE',
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

    tokens = tokens

    # Regular expression rules for simple tokens
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_LBRACE = r'{'
    t_RBRACE = r'}'
    t_COMMAND = r'\\([@a-zA-Z]+|[^\\])'
    t_NEWLINE = r'\\\\'
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
        self.__class__.lexer = lex.lex(module = self)

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_comment(self, t):
        r'%.*'
        pass

    # Error handling rule
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0]) # TODO log
        t.lexer.skip(1)

class SongLexer(SimpleLexer):

    states = (
        ('beginsong', 'inclusive'),
        )

    # State beginsong
    def t_INITIAL_BEGINSONG(self, t):
        r'\\beginsong'
        t.lexer.push_state('beginsong')
        t.lexer.open_brackets = 0
        t.lexer.open_braces = 0
        return t

    def t_beginsong_LBRACKET(self, t):
        r'\['
        if t.lexer.open_brackets == 0:
            t.type = 'SONG_LOPTIONS'
            t.lexer.open_braces += 1 # TODO Explain
        t.lexer.open_brackets += 1
        return t

    def t_beginsong_RBRACKET(self, t):
        r'\]'
        t.lexer.open_brackets -= 1
        if t.lexer.open_brackets == 0:
            t.type = 'SONG_ROPTIONS'
            t.lexer.open_braces -= 1 # TODO Explain
            t.lexer.pop_state()
            for __ignored in t.lexer: # TODO Explain
                pass
        return t

    def t_beginsong_LBRACE(self, t):
        r'{'
        if t.lexer.open_braces == 0:
            t.type = 'SONG_LTITLE'
        t.lexer.open_braces += 1
        return t

    def t_beginsong_RBRACE1(self, t):
        r'}(?![ \t\r\n]*\[)'
        t.lexer.open_braces -= 1
        t.type = 'RBRACE'
        if t.lexer.open_braces == 0:
            t.lexer.pop_state()
            t.type = 'SONG_RTITLE'
        return t

    def t_beginsong_RBRACE2(self, t):
        r'}(?=[ \t\r\n]*\[)'
        t.lexer.open_braces -= 1
        t.type = 'RBRACE'
        if t.lexer.open_braces == 0:
            t.type = 'SONG_RTITLE'
        return t

