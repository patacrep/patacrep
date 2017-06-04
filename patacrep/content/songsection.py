"""Allow 'songchapter' and 'songsection' as content of a songbook."""

from patacrep.content import ContentItem, ContentList, validate_parser_argument

KEYWORDS = [
    "songchapter",
    "songsection",
    ]

class SongSection(ContentItem):
    """A songsection or songchapter."""
    # pylint: disable=too-few-public-methods

    def __init__(self, keyword, name):
        self.keyword = keyword
        self.name = name

    def render(self, context):
        """Render this section or chapter."""
        return r'\{}{{{}}}'.format(self.keyword, self.name)

    def to_dict(self):
        return {self.keyword: self.name}

#pylint: disable=unused-argument
@validate_parser_argument("""
//str
""")
def parse(keyword, argument, config):
    """Parse the songsection.

    Arguments:
    - keyword ("songsection" or "songchapter"): the section to use;
    - argument: name of the section;
    - config: configuration dictionary of the current songbook.
    """
    return ContentList([SongSection(keyword, argument)])

CONTENT_PLUGINS = dict([
    (keyword, parse)
    for keyword
    in KEYWORDS
    ])
