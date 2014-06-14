#!/usr/bin/env python
# -*- coding: utf-8 -*-

from songbook_core.content import Content

KEYWORDS = [
        "part",
        "chapter",
        "section",
        "subsection",
        "subsubsection",
        "paragraph",
        "subparagraph",
        ]
FULL_KEYWORDS = KEYWORDS + [ "{}*".format(keyword) for keyword in KEYWORDS]

class Section(Content):
    def __init__(self, keyword, name, short = None):
        self.keyword = keyword
        self.name = name
        self.short = short

    def render(self, __context):
        if (self.short is None):
            return r'\{}{{{}}}'.format(self.keyword, self.name)
        else:
            return r'\{}[{}]{{{}}}'.format(self.keyword, self.short, self.name)

def parse(keyword, argument, contentlist, config):
    if (keyword not in KEYWORDS) and (len(contentlist) != 1):
        raise ContentError(keyword, "Starred section names must have exactly one argument.")
    if (len(contentlist) not in [1, 2]):
        raise ContentError(keyword, "Section can have one or two arguments.")
    return [Section(keyword, *contentlist)]


CONTENT_PLUGINS = dict([(keyword, parse) for keyword in FULL_KEYWORDS])
