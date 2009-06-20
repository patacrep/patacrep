#!/usr/bin/python
#

import os.path
import glob

def formatSongsDatabase( file, songs ):
    sdb = open( file, 'w' )

    dir = ['img']+map(os.path.dirname, songs)
    dir = set( dir )
    sdb.write('\graphicspath{\n')
    for dirname in dir:
        sdb.write('  {{{imagedir}/}},\n'.format(imagedir=dirname))
    sdb.write('}\n')
    for song in songs:
        sdb.write('\input{{{songfile}}}\n'.format(songfile=song.strip()))
    sdb.close();


def main():
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


if __name__ == '__main__':
    main()
