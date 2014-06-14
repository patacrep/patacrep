#!/usr/bin/env python
# -*- coding: utf-8 -*-

from songbook_core.content import Content

KEYWORDS = [
        "songchapter",
        "songsection",
        ]

class SongSection(Content):
    def __init__(self, keyword, name):
        self.keyword = keyword
        self.name = name

    def render(self):
        return r'\{}{{{}}}'.format(self.keyword, self.name)

def parse(keyword, config, *arguments):
    if (keyword not in KEYWORDS) and (len(arguments) != 1):
        raise ContentError(keyword, "Starred section names must have exactly one argument.")
    return [SongSection(keyword, *arguments)]


CONTENT_PLUGINS = dict([(keyword, parse) for keyword in KEYWORDS])
