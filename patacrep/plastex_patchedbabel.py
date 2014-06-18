#!/usr/bin/env python
# -*- coding: utf-8 -*-

r"""Patch pour le paquet Babel de PlasTeX

Un bug dans PlasTeX intervient lorsqu'on essaye d'analyser une commande LaTeX
\selectlanguage{}, que nous voulons utiliser ici. Un patch a été proposé aux
développeurs de plasTeX, et accepté. Mais il faut que cette correction arrive
en production. En attendant, nous utilisons cette version modifiée.

Dés que la correction sera entrée en production, il faudra supprimer ce
fichier, et remplater l'occurence à "patchedbabel" par "babel" dans le fichier
"plastex.py".
La correction à suveiller est la révision
41a48c0c229dd46b69fb0e3720595000a71b17d8 du fichier babel.py :
https://github.com/tiarno/plastex/commit/41a48c0c229dd46b69fb0e3720595000a71b17d8

# Comment vérifier si on peut supprimer ce fichier ?

1) Remplacer l'occurence à patchedbabel par babel dans le fichier plastex.py.

2) Générer un fichier .tex à partir d'un fichier .sb, ce dernier faisant
intervenir des chansons dans lesquelles \selectlanguage est utilisé (par
exemple, "make -B matteo.tex" ou "make -B naheulbeuk.tex" pour des fichiers pas
trop gros.

3) Si l'erreur suivante apparaît, c'est qu'il faut encore attendre.

> Traceback (most recent call last):
>     [...]
> File "/usr/lib/pymodules/python2.7/plasTeX/Packages/babel.py", line 18, in
>     invoke context.loadLanguage(self.attributes['lang'], self.ownerDocument)
> NameError: global name 'context' is not defined

3 bis) Si elle n'apparait pas : youpi ! Supprimez ce fichier !

# Contact et commentaires

Mercredi 27 mars 2013
Louis <spalax(at)gresille.org>

"""

from plasTeX import Command

# pylint: disable=invalid-name,too-many-public-methods
class selectlanguage(Command):
    """Patch of vanilla selectlanguage class.

    See module docstring for more information."""
    args = 'lang:str'

    def invoke(self, tex):
        res = Command.invoke(self, tex)
        self.ownerDocument.context.loadLanguage( # pylint: disable=no-member
                self.attributes['lang'],
                self.ownerDocument
                )
        return res
