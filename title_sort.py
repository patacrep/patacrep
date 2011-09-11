#coding:utf8

import re
import warnings
import locale

iecPattern = re.compile(r"\IeC {\\(.*?)}")
replacePattern = {
     '`A': 'À',
     'oe ': 'œ',
     "'e" : 'é',
     "'o" : 'ó',
     "c C" : 'ç',
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
            return replacePattern[match.group(1)]
        except KeyError:
            warnings.warn("Error, no match to replace %s in %s. You should add it in the coresponding table in title_solt.py" % (match.group(0), match.group(1)))

    return locale.strxfrm(iecPattern.sub(repl, value))
