#!/usr/bin/env python
# -*- coding: utf-8 -*-

import plasTeX
from plasTeX.TeX import TeX

def parsetex(filename):
    """Analyse syntaxique d'un fichier .sg

    Renvoie un dictionnaire contenant les métadonnées lues dans le fichier. Les
    clefs sont :
    - languages: l'ensemble des langages utilisés (recherche des
      \selectlanguages{}).
    """
    # Chargement du fichier .sg (.tex), et des modules nécessaires
    tex = TeX(file = filename)
    tex.disableLogging()
    tex.ownerDocument.context.loadPackage(tex, "babel")

    # Analyse syntaxique
    doc= tex.parse()

    # Extraction des données
    data = {
            "languages": set(),
            }
    for node in doc.allChildNodes:
        if node.nodeName == "selectlanguage":
            data["languages"].add(node.argSource)

    return data
