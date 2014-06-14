#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Song management."""

from unidecode import unidecode
import locale
import re

from songbook_core.authors import processauthors
from songbook_core.plastex import parsetex

# pylint: disable=too-few-public-methods
class Song(object):
    """Song management"""

    #: Ordre de tri
    sort = []
    #: Préfixes à ignorer pour le tri par titres
    prefixes = []
    #: Dictionnaire des options pour le traitement des auteurs
    authwords = {"after": [], "ignore": [], "sep": []}

    def __init__(self, filename):
        # Data extraction from the song with plastex
        data = parsetex(filename)
        self.titles = data['titles']
        self.normalized_titles = [
                locale.strxfrm(
                    unprefixed_title(
                        unidecode(unicode(title, "utf-8")),
                        self.prefixes
                        )
                    )
                for title
                in self.titles
                ]
        self.args = data['args']
        self.path = filename
        self.languages = data['languages']
        if "by" in self.args.keys():
            self.normalized_authors = [
                locale.strxfrm(author)
                for author
                in processauthors(self.args["by"], **self.authwords)
                ]
        else:
            self.normalized_authors = []

    def __repr__(self):
        return repr((self.titles, self.args, self.path))

    def __cmp__(self, other):
        if not isinstance(other, Song):
            return NotImplemented
        for key in self.sort:
            if key == "@title":
                self_key = self.normalized_titles
                other_key = other.normalized_titles
            elif key == "@path":
                self_key = locale.strxfrm(self.path)
                other_key = locale.strxfrm(other.path)
            elif key == "by":
                self_key = self.normalized_authors
                other_key = other.normalized_authors
            else:
                self_key = locale.strxfrm(self.args.get(key, ""))
                other_key = locale.strxfrm(other.args.get(key, ""))

            if self_key < other_key:
                return -1
            elif self_key > other_key:
                return 1
        return 0


def unprefixed_title(title, prefixes):
    """Remove the first prefix of the list in the beginning of title (if any).
    """
    for prefix in prefixes:
        match = re.compile(r"^(%s)\b\s*(.*)$" % prefix).match(title)
        if match:
            return match.group(2)
    return title


