"""Allow 'songchapter' and 'songsection' as content of a songbook."""

from patacrep.content import ContentItem, ContentError, ContentList, EmptyContentList

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

    def render(self, __context):
        """Render this section or chapter."""
        return r'\{}{{{}}}'.format(self.keyword, self.name)

#pylint: disable=unused-argument
def parse(keyword, argument, contentlist, config):
    """Parse the contentlist.

    Arguments:
    - keyword ("songsection" or "songchapter"): the section to use;
    - argument: unused;
    - contentlist: a list of one string, which is the name of the section;
    - config: configuration dictionary of the current songbook.
    """
    try:
        if (keyword not in KEYWORDS) and (len(contentlist) != 1):
            raise ContentError(
                keyword,
                "Starred section names must have exactly one argument.",
                )
        return ContentList([SongSection(keyword, contentlist[0])])
    except ContentError as error:
        return EmptyContentList(errors=[error])


CONTENT_PLUGINS = dict([
    (word, parse)
    for word
    in KEYWORDS
    ])
