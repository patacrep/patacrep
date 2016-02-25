"""Allows to set an arbitrary value to any LaTeX counter (like `songnum`)."""

from patacrep.content import ContentItem, ContentList, validate_parser_argument

class CounterSetter(ContentItem):
    """Set a counter."""
    # pylint: disable=too-few-public-methods

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def render(self, __context):
        """Set the value of the counter."""
        return r'\setcounter{{{}}}{{{}}}'.format(self.name, self.value)

#pylint: disable=unused-argument
@validate_parser_argument("""
type: //any
of:
  - //nil
  - //int
  - type: //rec
    optional:
      name: //str
      value: //int
""")
def parse(keyword, argument, config):
    """Parse the counter setter.

    Arguments:
    - nothing
        reset the "songnum" counter to 1
    - an int
        reset the "songnum" counter to this value
    - a dict:
        - name ("songnum"): the counter to set;
        - value: value to set the counter to;
    """
    if argument is None:
        argument = {}
    if isinstance(argument, int):
        argument = {'value': argument}
    name = argument.get('name', 'songnum')
    value = argument.get('value', 1)
    return ContentList([CounterSetter(name, value)])

CONTENT_PLUGINS = {'setcounter': parse}
