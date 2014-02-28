Templates
=========

- [ ] Implémenter le moteur de templates

Songs
=====

- [x] Dans un fichier .sb, si la clef 'songs' n'est pas définie, toutes les chansons de 'datadir/songs' sont incluses dans le carnet de chants.
- [ ] Dans songbook-data, modifier les fichiers .sb où 'songs' est défini à 'all', et supprimer cette clef.

\DataImgDirectory
=================

- [x] La commande LaTeX dataImgDirectory n'est plus traitée de manière particulière.
- [ ] Ajouter dans le moteur de templates un « truc » pour pouvoir, dans le template, accéder à datadir. Par exemple, un template veut inclure un fichier tex 'preface.tex', peut apparaitre dans le template quelque chose du genre '\include{<datadir>/preface}'. Le moteur de template remplacera alors '<datadir>' par le répertoire contenu dans Songbook().config['datadir'].
- [ ] Modifier les templates (songbook-data) pour remplacer la chaîne '\DataImgDirectory' (ou assimilée) à quelque chose du genre '<datadir>/img'.
