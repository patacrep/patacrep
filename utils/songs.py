#!/usr/bin/env python
# -*- coding: utf-8 -*-

import plasTeX

def split_linebreak(texlist):
    return_list = []
    current = []
    for token in texlist:
        if token.nodeName == '\\':
            return_list.append(current)
            current = []
        else:
            current.append(token.textContent.encode('utf-8'))
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
            args[key] = val.textContent.encode('utf-8')
        self.attributes['args'] = args
