#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import glob
import codecs
 
def replace_words(text, word_dic):
    """
    take a text and <strong class="highlight">replace</strong> words
    that match a key in a dictionary with the associated value, 
    return the changed text
    """
    rc = re.compile('|'.join(map(re.escape, word_dic)))
    def translate(match):
        return word_dic[match.group(0)]
    return rc.sub(translate, text)
 
# the dictionary has target_word:replacement_word pairs
word_dic = {
#oe inclusion
"coeur": "cœur",
"boeuf": "bœuf",
"oeuvre": "œuvre",
"soeur": "sœur",
"noeud": "nœud",
"oeil": "œil",
"oe{}": "œ",
#punctuation
"’": "'",
"Ca ": "Ça ",
"...": "\\dots ",
#Chords
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
}
 
# Process song files
songfiles = glob.glob('songs/*/*.sg')
for file in songfiles:
    songfile = codecs.open(file, "r", "utf-8")
    data = songfile.read().encode("utf-8")
    data = replace_words(data, word_dic)
    songfile.close()
    songfile = open(file, "w")
    songfile.write(data)
    songfile.close()
 
 
