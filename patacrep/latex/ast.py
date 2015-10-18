"""Abstract Syntax Tree for LaTeX code."""

# pylint: disable=too-few-public-methods

DEFAULT_LANGUAGE = "english"

class AST:
    """Base class for the tree."""
    # pylint: disable=no-init

    metadata = None

    @classmethod
    def init_metadata(cls):
        """Clear metadata

        As this attribute is a class attribute, it as to be reset at each new
        parsing.
        """
        cls.metadata = {
            '@language': DEFAULT_LANGUAGE,
            }

class Expression(AST):
    """LaTeX expression"""

    def __init__(self, value):
        super().__init__()
        self.content = [value]

    def prepend(self, value):
        """Add a value at the beginning of the content list."""
        if value is not None:
            self.content.insert(0, value)
        return self

    def __str__(self):
        return "".join([str(item) for item in self.content])

class Command(AST):
    """LaTeX command"""

    def __init__(self, name, optional, mandatory):
        self.name = name
        self.mandatory = mandatory
        self.optional = optional

        if name == r'\selectlanguage':
            self.metadata['@language'] = self.mandatory[0]

    def __str__(self):
        if self.name in [r'\emph']:
            return str(self.mandatory[0])
        return "{}{}{}".format(
            self.name,
            "".join(["[{}]".format(item) for item in self.optional]),
            "".join(["{{{}}}".format(item) for item in self.mandatory]),
            )


class BeginSong(AST):
    """Beginsong command"""

    def __init__(self, titles, arguments):
        self.titles = titles
        self.arguments = arguments
