"""Fake plugin for test purposes."""

from patacrep.content import ContentItem, ContentList, validate_parser_argument

class FakeContent(ContentItem):
    """Fake content."""

    def file_entry(self):
        return {'customzippedname:':''}

def parse(keyword, argument, config):
    return ContentList([FakeContent()])

CONTENT_PLUGINS = {'customzipedname': parse}

