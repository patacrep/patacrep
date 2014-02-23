#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""PlasTeX module to process song files."""

from plasTeX.TeX import TeX
from plasTeX.Base.LaTeX import Sentences

import codecs
import locale
import os
import sys


def processUnbreakableSpace(node):
    r"""Replace '~' and '\ ' in node by nodes that
    will be rendered as unbreakable space.

    Return node object for convenience.
    """
    if (type(node) == Sentences.InterWordSpace or
        (type(node) == Sentences.NoLineBreak and node.source == '~ ')):
        node.unicode = unichr(160)
    for child in node.childNodes:
        processUnbreakableSpace(child)

    return node


def simpleparse(text):
    """Parse a simple LaTeX string.
    """
    tex = TeX()
    tex.input(text.decode('utf8'))
    doc = tex.parse()
    return processUnbreakableSpace(doc.textContent)


class SongParser:
    """Analyseur syntaxique de fichiers .sg"""

    @staticmethod
    def _create_TeX():
        """Create a TeX object, ready to parse a tex file."""
        tex = TeX()
        tex.disableLogging()
        tex.ownerDocument.context.loadBaseMacros()
        sys.path.append(os.path.dirname(__file__))
        tex.ownerDocument.context.loadPackage(tex, "plastex-patchedbabel")
        tex.ownerDocument.context.loadPackage(tex, "plastex-songs")
        sys.path.pop()
        return tex

    @classmethod
    def parse(cls, filename):
        """Parse a TeX file, and return its plasTeX representation."""
        tex = cls._create_TeX()
        tex.input(codecs.open(filename, 'r+', 'utf-8', 'replace'))
        return tex.parse()


def parsetex(filename):
    r"""Analyse syntaxique d'un fichier .sg

    Renvoie un dictionnaire contenant les métadonnées lues dans le fichier. Les
    clefs sont :
    - languages: l'ensemble des langages utilisés (recherche des
      \selectlanguages{}) ;
    - titles: la liste des titres ;
    - args: le dictionnaire des paramètres passés à \beginsong.
    """
    # /* BEGIN plasTeX patch
    # The following lines, and another line a few lines later, are used to
    # circumvent a plasTeX bug. It has been reported, with a patch.
    # To see if you can delete those lines, set your LC_TIME locale to French,
    # during a month containing diacritics (e.g. Février), and run songbook. If
    # no plasTeX bug appears, it is safe to remove those lines.
    oldlocale = locale.getlocale(locale.LC_TIME)
    locale.setlocale(locale.LC_TIME, 'C')
    # plasTeX patch END */

    # Analyse syntaxique
    doc = SongParser.parse(filename)

    # /* BEGIN plasTeX patch
    if oldlocale[0] and oldlocale[1]:
        locale.setlocale(locale.LC_TIME, "%s.%s" % oldlocale)
    # plasTeX patch END */

    # Extraction des données
    data = {
            "languages": set(),
            }
    for node in doc.allChildNodes:
        if node.nodeName == "selectlanguage":
            data["languages"].add(node.attributes['lang'])
        if node.nodeName == "beginsong":
            data["titles"] = node.attributes["titles"]
            data["args"] = node.attributes["args"]

    return data
