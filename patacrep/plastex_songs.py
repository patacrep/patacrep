#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module to process song LaTeX environment.
"""

import plasTeX

from patacrep.plastex import process_unbr_spaces


def split_linebreak(texlist):
    """Return a list of alternative title.

    A title can be defined with alternative names :

        A real name\\
        Alternative name\\
        Another alternative name

    This function takes the object representation of a list of titles, and
    return a list of titles.
    """
    return_list = []
    current = []
    for token in texlist:
        if token.nodeName == '\\':
            return_list.append(current)
            current = []
        else:
            current.append(
                    process_unbr_spaces(token).textContent.encode('utf-8'))
    if current:
        return_list.append(current)
    return return_list


class beginsong(plasTeX.Command): # pylint: disable=invalid-name,too-many-public-methods
    """Class parsing the LaTeX song environment."""

    args = '{titles}[ args:dict ]'

    def invoke(self, tex):
        """Parse an occurence of song environment."""

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
                args[key] = process_unbr_spaces(val).textContent.encode('utf-8')
            elif isinstance(val, basestring):
                args[key] = val.encode('utf-8')
            else:
                args[key] = unicode(val)
        self.attributes['args'] = args
