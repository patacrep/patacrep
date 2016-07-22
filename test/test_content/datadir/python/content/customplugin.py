"""Fake plugin for test purposes."""

from patacrep.content import ContentItem, ContentList, validate_parser_argument

class FakeContent(ContentItem):
    """Fake content."""

    def to_dict(self):
        return {'customname':''}

def parse(keyword, argument, config):
    return ContentList([FakeContent()])

CONTENT_PLUGINS = {'customname': parse}

