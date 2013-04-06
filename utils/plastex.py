#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plasTeX.TeX import TeX
import codecs
import copy
import os
import sys

class SongParser:
    """Analyseur syntaxique de fichiers .sg"""

    @staticmethod
    def _create_TeX():
        tex = TeX()
        tex.disableLogging()
        tex.ownerDocument.context.loadBaseMacros()
        sys.path.append(os.path.dirname(__file__))
        tex.ownerDocument.context.loadPackage(tex, "patchedbabel")
        tex.ownerDocument.context.loadPackage(tex, "songs")
        sys.path.pop()
        return tex

    @classmethod
    def parse(cls, filename):
        tex = cls._create_TeX()
        tex.input(codecs.open(filename, 'r+', 'utf-8', 'replace'))
        return tex.parse()

def parsetex(filename):
    """Analyse syntaxique d'un fichier .sg

    Renvoie un dictionnaire contenant les métadonnées lues dans le fichier. Les
    clefs sont :
    - languages: l'ensemble des langages utilisés (recherche des
      \selectlanguages{}) ;
    - titles: la liste des titres ;
    - args: le dictionnaire des paramètres passés à \\beginsong.
    """
    # Analyse syntaxique
    doc = SongParser.parse(filename)

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
