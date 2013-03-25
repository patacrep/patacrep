#coding:utf8

import re
import warnings
import locale

iecPattern = re.compile(r"\IeC {\\(.*?)}")
replacePattern = {
     '`A': 'À',
     '`a': 'à',
     '^a': 'â',
     "'a": 'á',
     "~a": 'ã',
     'oe': 'œ',
     "'e" : 'é',
     "`e" : 'è',
     "^e" : 'ê',
     '"e' : 'ë',
     "'E" : 'É',
     "`E" : 'È',
     "'o" : 'ó',
     "^o" : 'ô',
     r'"\i' : 'i',
     r'^\i' : 'i',
     '"u' : 'ü',
     '`u' : 'ù',
     '`u' : 'ù',
     '~n' : 'ñ',
     "c C" : 'Ç',
     "c c" : 'ç',
     "textquoteright" : "'",
}

def sortkey(value):
    '''
    From a title, return something usable for sorting. It handles locale (but
    don't forget to call locale.setlocale(locale.LC_ALL, '')). It also try to
    handle the sort with crappy latex escape sequences. Some chars may not be
    handled by this function, so add them to *replacePattern* dictionnary.
    '''
    def repl(match):
        try:
            return replacePattern[match.group(1).strip()]
        except KeyError:
            warnings.warn("Error, no match to replace %s in %s. You should add it in the coresponding table in title_sort.py" % (match.group(0), match.group(1)))

    return locale.strxfrm(iecPattern.sub(repl, value).replace(' ', 'A'))
