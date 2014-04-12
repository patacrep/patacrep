#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Song management."""

from unidecode import unidecode
import glob
import locale
import os.path
import re
import logging

from songbook_core.authors import processauthors
from songbook_core.plastex import parsetex

LOGGER = logging.getLogger(__name__)

# pylint: disable=too-few-public-methods
class Song(object):
    """Song management"""

    #: Ordre de tri
    sort = []
    #: Préfixes à ignorer pour le tri par titres
    prefixes = []
    #: Dictionnaire des options pour le traitement des auteurs
    authwords = {"after": [], "ignore": [], "sep": []}

    def __init__(self, path, languages, titles, args):
        self.titles = titles
        self.normalized_titles = [
                locale.strxfrm(
                    unprefixed_title(
                        unidecode(unicode(title, "utf-8")),
                        self.prefixes
                        )
                    )
                for title
                in titles
                ]
        self.args = args
        self.path = path
        self.languages = languages
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


class SongsList(object):
    """Manipulation et traitement de liste de chansons"""

    def __init__(self, library):
        self._songdir = os.path.join(library, 'songs')

        # Liste triée des chansons
        self.songs = []

    def append(self, filename):
        """Ajout d'une chanson à la liste

        Effets de bord : analyse syntaxique plus ou moins sommaire du fichier
        pour en extraire et traiter certaines information (titre, langue,
        album, etc.).
        """
        LOGGER.debug('Parsing file "{}"…'.format(filename))
        # Exécution de PlasTeX
        data = parsetex(filename)

        song = Song(filename, data['languages'], data['titles'], data['args'])
        low, high = 0, len(self.songs)
        while low != high:
            middle = (low + high) / 2
            if song < self.songs[middle]:
                high = middle
            else:
                low = middle + 1
        self.songs.insert(low, song)

    def append_list(self, filelist):
        """Ajoute une liste de chansons à la liste

        L'argument est une liste de chaînes, représentant des noms de fichiers
        sous la forme d'expressions régulières destinées à être analysées avec
        le module glob.
        """
        for regexp in filelist:
            before = len(self.songs)
            for filename in glob.iglob(os.path.join(self._songdir, regexp)):
                self.append(filename)
            if len(self.songs) == before:
                # No songs were added
                LOGGER.warning(
                        "Expression '{}' did not match any file".format(regexp)
                        )

    def languages(self):
        """Renvoie la liste des langues utilisées par les chansons"""
        return set().union(*[set(song.languages) for song in self.songs])
