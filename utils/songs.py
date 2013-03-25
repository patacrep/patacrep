#!/usr/bin/env python
# -*- coding: utf-8 -*-

import plasTeX

class beginsong(plasTeX.Command):
    args = '{titles}[ args:dict ]'
    def invoke(self, tex):
        plasTeX.Command.invoke(self, tex)

        # Parsing title
        titles = []
        for token in self.attributes['titles'].allChildNodes:
            if token.nodeName != '\\':
                titles.append(token.source.encode('utf-8'))
        self.attributes['titles'] = titles

        # Parsing keyval arguments
        pass
