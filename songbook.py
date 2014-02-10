#!/usr/bin/python
# -*- coding: utf-8 -*-
#

from songbook.build import buildsongbook

import getopt
import json
import locale
import os.path
import sys


def usage():
    print "No usage information yet."

def main():
    locale.setlocale(locale.LC_ALL, '') # set script locale to match user's
    try:
        opts, args = getopt.getopt(sys.argv[1:], 
                                   "hs:l:",
                                   ["help","songbook=","library="])
    except getopt.GetoptError, err:
        # print help and exit
        print str(err)
        usage()
        sys.exit(2)

    sbFile = None
    library = './'

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-s", "--songbook"):
            sbFile = a
        elif o in ("-l", "--library"):
            if not a.endswith('/'):
                a += '/'
            library = a
        else:
            assert False, "unhandled option"

    basename = os.path.basename(sbFile)[:-3]

    f = open(sbFile)
    sb = json.load(f)
    f.close()

    buildsongbook(sb, basename, library)

if __name__ == '__main__':
    main()
