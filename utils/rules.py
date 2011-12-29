#!/usr/bin/python
# -*- coding: utf-8 -*-

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
"...": "{\\dots}",
"…": "{\\dots}",
#replace tabs with two spaces
"	": "  ",
##: Typo
"New-York": "New York",
" i ": " I ",
"avant hier": "avant-hier",
##: Conversion to anglo-saxon chords
"Lam ": "Am ",
"La7": "A7",
"Lasus2": "Asus2",
"Sim ": "Bm ",
"Sim}": "Bm}",
"Sim]": "Bm]",
"Si7": "B7",
"Dom ": "Cm ",
"Do7": "C7",
"Do9": "C9",
"Ré ": "D ",
"Rém ": "Dm ",
"Rém]": "Dm]",
"Ré7": "D7",
"Ré#": "D#",
"Mim ": "Em ",
"Mim]": "Em]",
"Mim7": "Em7",
"Mim}": "Em}",
"Mi7": "E7",
"Mi7sus4": "E7sus4",
"Fa ": "F ",
"Fa}": "F}",
"Fa\\": "F\\",
"Fam ": "Fm ",
"Fa7": "F7",
"Sol ": "G ",
"Sol]": "G]",
"Solm ": "Gm ",
"Solm]": "Gm]",
"Sol7": "G7",
"/La": "/A",
"/Si": "/B",
"/Do": "/C",
"/Ré": "/D",
"/Mi": "/E",
"/Fa": "/F",
"/Sol": "/G",
"gtab{La": "gtab{A",
"gtab{Si": "gtab{B",
"gtab{Do": "gtab{C",
"gtab{Ré": "gtab{D",
"gtab{Mi": "gtab{E",
"gtab{Fa": "gtab{F",
"gtab{Sol": "gtab{G",
"\\[La": "\\[A",
"\\[Si": "\\[B",
"\\[Do": "\\[C",
"\\[Ré": "\\[D",
"\\[Mi": "\\[E",
"\\[Fa": "\\[F",
"\\[Sol": "\\[G",
"\\[Re": "\\[D",
"b]": "&]",
"b7]": "&7]",
#C
"032010": "X32010",
#A
"002220": "X02220",
"002020": "X02020",
"002210": "X02210",
#D
"000232": "XX0232",
"X00232": "XX0232",
"000212": "XX0212",
"000231": "XX0231",
"X00231": "XX0231",
#B
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

