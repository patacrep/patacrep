
from patacrep.songs import Song

class ChordproSong(Song):
    pass

SONG_PARSERS = {
    'sgc': ChordproSong,
    }
