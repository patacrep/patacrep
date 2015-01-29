"""Chordpro parser"""

from jinja2 import Environment, FileSystemLoader
import pkg_resources
import os

from patacrep import encoding, files
from patacrep.songs import Song
from patacrep.songs.chordpro.syntax import parse_song
from patacrep.templates import TexRenderer

class ChordproSong(Song):
    """Chordpros song parser."""

    def parse(self, config):
        """Parse content, and return the dictinory of song data."""
        with encoding.open_read(self.fullpath, encoding=self.encoding) as song:
            song = parse_song(song.read(), self.fullpath)
        self.authors = song.authors
        self.titles = song.titles
        self.languages = song.get_directives('language')
        self.data = dict([meta.as_tuple for meta in song.meta])
        self.cached = {
                'song': song,
                }

    def tex(self, output):
        context = {
            'language': self.cached['song'].get_directive('language', self.config['lang']),
            'columns': self.cached['song'].get_directive('columns', 1),
            "path": files.relpath(self.fullpath, os.path.dirname(output)),
            "titles": r"\\".join(self.titles),
            "authors": ", ".join(["{} {}".format(name[1], name[0]) for name in self.authors]),
            "metadata": self.data,
            "beginsong": self.cached['song'].meta_beginsong(),
            "content": self.cached['song'].content,
            }
        return TexRenderer(
                template="chordpro.tex",
                encoding='utf8',
                texenv=Environment(loader=FileSystemLoader(os.path.join(
                        os.path.abspath(pkg_resources.resource_filename(__name__, 'data')),
                        'latex'
                    ))),
                ).template.render(context)

SONG_PARSERS = {
    'sgc': ChordproSong,
    }
