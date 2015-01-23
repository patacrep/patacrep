
from patacrep import encoding
from patacrep.songs import Song
from patacrep.songs.chordpro.syntax import parse_song

class ChordproSong(Song):
    """Chordpros song parser."""

    def parse(self):
        """Parse content, and return the dictinory of song data."""
        with encoding.open_read(self.fullpath, encoding=self.encoding) as song:
            self.data = parse_song(song.read(), self.fullpath)
        print(self.data)
        import sys; sys.exit(1)
        self.titles = self.data['@titles']
        del self.data['@titles']
        self.languages = self.data['@languages']
        del self.data['@languages']
        self.authors = self.data['by']
        del self.data['by']

SONG_PARSERS = {
    'sgc': ChordproSong,
    }
