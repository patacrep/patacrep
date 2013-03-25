#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plasTeX.TeX import TeX
import codecs
import copy

from utils import songs

class SongParser:
    """Classe singleton, pour ne charger qu'une fois les modules LaTeX"""
    _tex = None

    @classmethod
    def _create_TeX(cls):
        cls._tex = TeX()
        cls._tex.disableLogging()
        cls._tex.ownerDocument.context.loadBaseMacros()
        cls._tex.ownerDocument.context.loadPackage(cls._tex, "babel")

    @classmethod
    def parse(cls, filename):
        if not cls._tex:
            cls._create_TeX()
        tex = copy.copy(cls._tex)
        tex.input(codecs.open(filename, 'r+', 'utf-8', 'replace'))
        return tex.parse()

def parsetex(filename):
    """Analyse syntaxique d'un fichier .sg

    Renvoie un dictionnaire contenant les métadonnées lues dans le fichier. Les
    clefs sont :
    - languages: l'ensemble des langages utilisés (recherche des
      \selectlanguages{}).
    """
    # Analyse syntaxique
    doc = SongParser.parse(filename)

    # Extraction des données
    data = {
            "languages": set(),
            }
    for node in doc.allChildNodes:
        if node.nodeName == "selectlanguage":
            data["languages"].add(node.argSource)

    return data
