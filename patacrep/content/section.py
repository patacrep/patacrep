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
        if self.short is None or self.keyword not in KEYWORDS:
            return r'\{}{{{}}}'.format(self.keyword, self.name)
        else:
            return r'\{}[{}]{{{}}}'.format(self.keyword, self.short, self.name)

#pylint: disable=unused-argument
def parse(keyword, argument, config):
    """Parse the contentlist.

    Arguments:
    - keyword (one of "part", "chapter", "section", ... , "subparagraph", and
      their starred versions "part*", "chapter*", ... , "subparagraph*"): the
      section to use;
    - argument:
        either a string describing the section name
        or a dict
            name: Name of the section
            short: Shortname of the section (only for non starred sections)
    - config: configuration dictionary of the current songbook.
    """
    if isinstance(argument, str):
        argument = {'name': argument}
    return ContentList([Section(keyword, **argument)])


CONTENT_PLUGINS = dict([
    (word, parse)
    for word
    in FULL_KEYWORDS
    ])
