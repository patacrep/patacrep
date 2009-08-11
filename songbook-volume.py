#!/usr/bin/python
#

import getopt, sys
import os.path
import glob

def formatSongsDatabase( file, songs ):
    sdb = open( file, 'w' )

    dir = ['img']+map(os.path.dirname, songs)
    dir = set( dir )
    sdb.write('\graphicspath{\n')
    if sys.hexversion >= 0x20600000:
        # use string format introduced in python 2.6
        for dirname in dir:
            sdb.write('  {{{imagedir}/}},\n'.format(imagedir=dirname))
        sdb.write('}\n')
        for song in songs:
            sdb.write('\input{{{songfile}}}\n'.format(songfile=song.strip()))
    else:
        # use old formating strategy
        for dirname in dir:
            sdb.write('  {%(imagedir)s/},\n' % {'imagedir':dirname})
        sdb.write('}\n')
        for song in songs:
            sdb.write('\input{%(songfile)s}\n' % {'songfile':song.strip()})
    sdb.close();


def oldmain():
    songfiles = glob.glob('songs/*/*.sg')
    
    songvolumes = glob.glob('songs-volume-*')

    for volume in songvolumes:
        songs = []
        vol = open( volume )
        for song in vol:
            s = song.strip()
            songs.append( s )
            songfiles.remove( s )
        vol.close()
        formatSongsDatabase( 'db_'+volume+'.sdb', songs )

    formatSongsDatabase( 'songs.sdb', songfiles )

def processSongFile( file, songfile ):
    songs = []
    vol = open( songfile )
    for song in vol:
        s = song.strip()
        songs.append( s )
    vol.close()
    formatSongsDatabase( file, songs )


def usage():
    print "erf"

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 
                                   "hs:o:", 
                                   ["help","songs=","output="])
    except getopt.GetoptError, err:
        # print help and exit
        print str(err)
        usage()
        sys.exit(2)

    songFile = None
    output = None

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-s", "--songs"):
            songFile = a
        elif o in ("-o", "--output"):
            output = a
        else:
            assert False, "unhandled option"

    if songFile and output:
        processSongFile( output, songFile)

if __name__ == '__main__':
    main()
