#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob
import getopt, sys
import re
import logging
import locale
re.LOCALE

from utils.utils import recursiveFind

# the dictionary has target_word:replacement_word pairs
word_dic = {
##: oe inclusion
"coeur": "cœur",
"choeur": "chœur",
"boeuf": "bœuf",
"oeuvre": "œuvre",
"soeur": "sœur",
"noeud": "nœud",
"oeil": "œil",
"voeu": "vœu",
"oeuf": "œuf",
"oe{}": "œ",
"\\œ": "œ",
##: Contractions
"ptit": "p'tit",
"Y a": "Y'a",
"ptê": "p't'ê",
"p'tê": "p't'ê",
"p't-ê": "p't'ê",
##: Punctuation
"’": "'",
"‘": "'",
"´": "'",
"Ca ": "Ça ",
"...": "{\\dots}",
"…": "{\\dots}",
"say: ``":"say, ``",
"says: ``":"says, ``",
"said: ``":"said, ``",
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
"[Fa\\": "[F\\",
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
"tab{La": "tab{A",
"tab{Si": "tab{B",
"tab{Do": "tab{C",
"tab{Ré": "tab{D",
"tab{Mi": "tab{E",
"tab{Fa": "tab{F",
"tab{Sol": "tab{G",
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
## LaTeX
"beginchorus": "begin{chorus}",
"endchorus": "end{chorus}",
"beginverse*": "begin{verse*}",
"beginverse": "begin{verse}",
"endverse": "end{verse}",
"}[by=": "}\n  [by=",
### end of rules
}


def usage():
   print '''
Usage: rules.py [OPTION]

OPTIONS
    -h, --help
      display this help and exit

    -f, --files=FILES
      apply the set of rules on FILES
      default is songs/*/*.sg

    -l, --log=LEVEL
      set the logging level to LEVEL
      outputs logging information to rules.log
      possible LEVEL values are : debug, info, warning, error and critical
'''

def replace_words(string):
   '''
   Search the data string for words defined in the dictionary and
   replace them. This method avoids usual spelling and typos mistakes
   when writing a song.
   '''
   logging.info("replace_words: search and replace words from dictionary into song data")
   for search, replace in word_dic.items():
      string = string.replace(search, replace)
   return string

#language based typographical rules
def language_rules(string):
   '''
   Search the data string for common typographical mistakes.
   Implemented rules depend on the current song language that is
   defined by babel for every .sg file through the macro
   \selectlanguage{<lang>}
   '''
   logging.info("language_rules: looking for common typographical mistakes")
   if (re.compile("selectlanguage{french}").search(string)):
      logging.info("  song language is set to : french")
      #ensure non-breaking spaces before symbols ? ! ; :
      string = re.sub("(?P<last_char>\S)(?P<symbol>[!?;:])","\g<last_char> \g<symbol>", string)
      #... except for gtabs macros with capos
      string = re.sub("(?P<gtab>tab.?{.*)\s:","\g<gtab>:", string)
      #... and for urls
      string = re.sub("http\s:","http:", string)
      #and apply a second time for cases like \gtab{Gm}{10:X02210:}
      string = re.sub("(?P<gtab>tab.?{.*)\s:","\g<gtab>:", string)
      #ensure no spaces after symbols (
      string = re.sub("(?P<symbol>[\(])\s(?P<next_char>\S)","\g<symbol>\g<next_char>", string)
      #convert inverted commas
      string = re.sub("``","{\\og}", string)
      string = re.sub("''","{\\\\fg}", string)
   elif (re.compile("selectlanguage{english}").search(string)):
      logging.info("  song language is set to : english")
      #ensure no spaces before symbols ? ! ; : )
      string = re.sub("(?P<last_char>\S)\s(?P<symbol>[!?;:\)])","\g<last_char>\g<symbol>", string)
      #ensure no spaces after symbols (
      string = re.sub("(?P<symbol>[\(])\s(?P<next_char>\S)","\g<symbol>\g<next_char>", string)
   elif (re.compile("selectlanguage{spanish}").search(string)):
      logging.info("  song language is set to : spanish")
      #ensure no spaces before symbols ? ! ; : )
      string = re.sub("(?P<last_char>\S)\s(?P<symbol>[!?;:\)])","\g<last_char>\g<symbol>", string)
      #ensure no spaces after symbols ¿ ¡ (
      string = re.sub("(?P<symbol>[¿¡\(])\s(?P<next_char>\S)","\g<symbol>\g<next_char>", string)
   elif (re.compile("selectlanguage{portuguese}").search(string)):
      logging.info("  song language is set to : portuguese")
      #convert inverted commas
      string = re.sub("``","{\\og}", string)
      string = re.sub("''","{\\\\fg}", string)
   else :
      print "Warning: language is not defined for song : " + filename
   return string

def process_lines(lines):
   '''
   Removes trailing punctuation and multi-spaces from lines.  Note
   that it preserves whitespaces at the beginning of lines that
   correspond to indentation.
   '''
   logging.info("process_lines: handling song data line by line")
   star = False
   for index, line in enumerate(lines):
      if re.compile("begin{verse\*}").search(line):
         star = True

      if re.compile("end{verse\*}").search(line):
         star = False

      if star == True and re.compile("end{verse}").search(line):
         line = line.replace("verse", "verse*")
         star = False

      #remove trailing spaces and punctuation
      line = line.rstrip().rstrip(',.;').rstrip()
      #remove multi-spaces within lines
      line = re.sub("(?P<last_char>\S)\s{2,}","\g<last_char> ", line)
      lines[index] = line
   return lines


def main():
   locale.setlocale(locale.LC_ALL, '')
   try:
      opts, args = getopt.getopt(sys.argv[1:],
                                 "hf:l:",
                                 ["help", "files=", "log="])
   except getopt.GetoptError:
      usage()
      sys.exit(2)

   songfiles = recursiveFind(os.path.join(library, 'songs'), '*.sg')
   loglevel  = "warning"

   for option, arg in opts:
      if option in ("-h", "--help"):
         usage()
         sys.exit()
      elif option in ("-f", "--files"):
         songfiles = glob.glob(arg)
      elif option in ("-l", "--log"):
         loglevel = arg
         numeric_level = getattr(logging, loglevel.upper(), None)
         if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % loglevel)
         logging.basicConfig(level=numeric_level, filename='rules.log', filemode='w')
      else:
         assert False, "unhandled option"

   for filename in songfiles:
      with open(filename, 'r+') as songfile:
         logging.info("checking file: "+filename)
         data = songfile.read()
         #no dots for acronyms
         #data = re.sub("(?P<capital_letter>[A-Z])\.","\g<capital_letter>", data)
         data = replace_words(data)
         data = language_rules(data)
         lines = process_lines(data.split('\n'))
         data = "\n".join(lines)
         songfile.seek(0)
         songfile.write(data)
         songfile.truncate()
      
if __name__ == '__main__':
    main()
