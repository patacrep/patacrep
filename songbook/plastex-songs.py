#!/usr/bin/env python
# -*- coding: utf-8 -*-

import plasTeX

from songbook.plastex import processUnbreakableSpace

def split_linebreak(texlist):
    return_list = []
    current = []
    for token in texlist:
        if token.nodeName == '\\':
            return_list.append(current)
            current = []
        else:
            current.append(processUnbreakableSpace(token).textContent.encode('utf-8'))
    if current:
        return_list.append(current)
    return return_list

class beginsong(plasTeX.Command):
    args = '{titles}[ args:dict ]'
    def invoke(self, tex):
        plasTeX.Command.invoke(self, tex)

        # Parsing title
        titles = []
        for tokens in split_linebreak(self.attributes['titles'].allChildNodes):
            titles.append("".join(tokens))
        self.attributes['titles'] = titles

        # Parsing keyval arguments
        args = {}
        for (key, val) in self.attributes['args'].iteritems():
            if isinstance(val, plasTeX.DOM.Element):
                args[key] = processUnbreakableSpace(val).textContent.encode('utf-8')
            elif isinstance(val, unicode):
                args[key] = val.encode('utf-8')
            elif isinstance(val, str):
                args[key] = val.encode('utf-8')
            else:
                args[key] = unicode(val)
        self.attributes['args'] = args
