"""Fake plugin for test purposes."""

from patacrep.content import ContentItem, ContentList, validate_parser_argument

class FakeContent(ContentItem):
    """Fake content."""

    def render(self, __context):
        return 'fakecontent'

    def file_entry(self):
        return {'customname:':''}

#pylint: disable=unused-argument
def parse(keyword, argument, config):
    """
    """
    return ContentList([FakeContent()])

CONTENT_PLUGINS = {'customname': parse}

