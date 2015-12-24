"""Allow LaTeX sections (starred or not) as content of a songbook."""

from patacrep.content import ContentItem, ContentError, ContentList, EmptyContentList

KEYWORDS = [
    "part",
    "chapter",
    "section",
    "subsection",
    "subsubsection",
    "paragraph",
    "subparagraph",
    ]
FULL_KEYWORDS = KEYWORDS + ["{}*".format(word) for word in KEYWORDS]

class Section(ContentItem):
    """A LaTeX section."""
    # pylint: disable=too-few-public-methods

    def __init__(self, keyword, name, short=None):
        self.keyword = keyword
        self.name = name
        self.short = short

    def render(self, __context):
        if self.short is None:
            return r'\{}{{{}}}'.format(self.keyword, self.name)
        else:
            return r'\{}[{}]{{{}}}'.format(self.keyword, self.short, self.name)

#pylint: disable=unused-argument
def parse(keyword, argument, contentlist, config):
    """Parse the contentlist.

    Arguments:
    - keyword (one of "part", "chapter", "section", ... , "subparagraph", and
      their starred versions "part*", "chapter*", ... , "subparagraph*"): the
      section to use;
    - argument: unused;
    - contentlist: a list of one or two strings, which are the names (long
      and short) of the section;
    - config: configuration dictionary of the current songbook.
    """
    try:
        if (keyword not in KEYWORDS) and (len(contentlist) != 1):
            raise ContentError(
                keyword,
                "Starred section names must have exactly one argument."
                )
        if (len(contentlist) not in [1, 2]):
            raise ContentError(keyword, "Section can have one or two arguments.")
        return ContentList([Section(keyword, *contentlist)])
    except ContentError as error:
        return EmptyContentList(errors=[error])


CONTENT_PLUGINS = dict([
    (word, parse)
    for word
    in FULL_KEYWORDS
    ])
