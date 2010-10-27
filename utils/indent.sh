#!/bin/sh

#Author: Romain Goffe
#Date: 27/10/2010
#Descritpion: correctly indent all songs with emacs
#Commentary: can't manage to use a relative path to emacs-format-file.el
#            so be sure to indicate the right path

for song in songs/*/*.sg ; do
    emacs -batch $song -l ~/songbook/utils/emacs-format-file.el -f emacs-format-function ;
done;
