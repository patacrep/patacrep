#!/usr/bin/python
# -*- coding: utf-8 -*-

# warning: lines beginning with ## are parsed by 
# the songbook-client as rules categories 


import glob

# the dictionary has target_word:replacement_word pairs
word_dic = {
##: oe inclusion
"coeur": "cœur",
"boeuf": "bœuf",
"oeuvre": "œuvre",
"soeur": "sœur",
"noeud": "nœud",
"oeil": "œil",
"voeu": "vœu",
"oeuf": "œuf",
"oe{}": "œ",
##: Contractions
"ptit": "p'tit",
##: Punctuation
"’": "'",
"Ca ": "Ça ",
"\\musicnote{Intro": "\\musicnote{intro",
"\\musicnote{Outro": "\\musicnote{outro",
"...": "\\dots ",
"…": "\\dots",
#replace tabs with two spaces
"	": "  ",
##: Typo
"New-York": "New York",
" i ": " I ",
"avant hier": "avant-hier",
##: Conversion from anglo-saxon conventions
"\\[A": "\\[La",
"\\[B": "\\[Si",
"\\[C": "\\[Do",
"\\[D]": "\\[Ré]",
"\\[E": "\\[Mi",
"\\[F]": "\\[Fa]",
"\\[G": "\\[Sol",
##: Guitar tabs
"\\[Re]": "\\[Ré]",
"b]": "&]",
#Do
"032010": "X32010",
#La
"002220": "X02220",
"002020": "X02020",
"002210": "X02210",
#Ré
"000232": "XX0232",
"X00232": "XX0232",
"000212": "XX0212",
"000231": "XX0231",
"X00231": "XX0231",
#Si
"021202": "X21202",
### end of rules
}
 
# Process song files
songfiles = glob.glob('songs/*/*.sg')
for filename in songfiles:
   with open(filename, 'r+') as songfile:
       data = songfile.read()
       for search, replace in word_dic.items():
             data = data.replace(search, replace)
       songfile.seek(0)
       songfile.write(data)
       songfile.truncate()

