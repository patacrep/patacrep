class AST:

    metadata = None

    @classmethod
    def init_metadata(cls):
        cls.metadata = {
                '@languages': set(),
                }

class Expression(AST):

    def __init__(self, value):
        super().__init__()
        self.content = [value]

    def prepend(self, value):
        if value is not None:
            self.content.insert(0, value)
        return self

    def __str__(self):
        return "".join([str(item) for item in self.content])

class Command(AST):

    def __init__(self, name, optional, mandatory):
        self.name = name
        self.mandatory = mandatory
        self.optional = optional

        if name == r'\selectlanguage':
            self.metadata['@languages'] |= set(self.mandatory)

    def __str__(self):
        if self.name in [r'\emph']:
            return str(self.mandatory[0])
        return "{}{}{}".format(
                self.name,
                "".join(["[{}]".format(item) for item in self.optional]),
                "".join(["{{{}}}".format(item) for item in self.mandatory]),
                )


class BeginSong(AST):

    def __init__(self, titles, arguments):
        self.titles = titles
        self.arguments = arguments
