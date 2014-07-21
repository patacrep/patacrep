# -*- coding: utf-8 -*-

"""Module to process song LaTeX environment.
"""

import plasTeX

from patacrep import encoding
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
            current.append(encoding.basestring2unicode(
                process_unbr_spaces(token).textContent
                ))
    if current:
        return_list.append(current)
    return return_list


class beginsong(plasTeX.Command): # pylint: disable=invalid-name,too-many-public-methods
    """Class parsing the LaTeX song environment."""

    args = '{titles}[args:dict]'

    def invoke(self, tex):
        """Parse an occurence of song environment."""

        plasTeX.Command.invoke(self, tex)

        # Parsing title
        titles = []
        for tokens in split_linebreak(self.attributes['titles'].allChildNodes):
            titles.append("".join(tokens))
        self.attributes['titles'] = encoding.list2unicode(titles)

        # Parsing keyval arguments
        args = {}
        for (key, val) in self.attributes['args'].iteritems():
            if isinstance(val, plasTeX.DOM.Element):
                args[key] = encoding.basestring2unicode(
                        process_unbr_spaces(val).textContent
                        )
            elif isinstance(val, basestring):
                args[key] = encoding.basestring2unicode(val)
            else:
                args[key] = unicode(val)
        self.attributes['args'] = args

class sortassong(beginsong): # pylint: disable=invalid-name,too-many-public-methods
    r"""Treat '\sortassong' exactly as if it were a '\beginsong'."""
    pass
