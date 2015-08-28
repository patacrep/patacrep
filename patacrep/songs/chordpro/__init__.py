"""Chordpro parser"""

from jinja2 import Environment, FileSystemLoader, contextfunction
import pkg_resources
import os

from patacrep import encoding, files
from patacrep.songs import Song
from patacrep.songs.chordpro.syntax import parse_song
from patacrep.templates import TexRenderer

class ChordproSong(Song):
    """Chordpros song parser."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.texenv = None

    def parse(self, config):
        """Parse content, and return the dictionary of song data."""
        with encoding.open_read(self.fullpath, encoding=self.encoding) as song:
            song = parse_song(song.read(), self.fullpath)
        self.authors = song.authors
        self.titles = song.titles
        self.languages = song.get_data_argument('language', [self.config['lang']])
        self.data = song.meta
        self.cached = {
            'song': song,
            }

    def tex(self, output):
        context = {
            'language': self.config.get(
                'lang',
                self.cached['song'].get_data_argument('language', 'english'),
                ),
            "path": files.relpath(self.fullpath, os.path.dirname(output)),
            "titles": self.titles,
            "authors": self.authors,
            "metadata": self.data,
            "render": self.render_tex,
            }
        self.texenv = Environment(loader=FileSystemLoader(os.path.join(
            os.path.abspath(pkg_resources.resource_filename(__name__, 'data')),
            'latex'
            )))
        return self.render_tex(context, self.cached['song'].content, template="song.tex")

    @contextfunction
    def render_tex(self, context, content, template=None):
        """Render ``content`` as tex."""
        if isinstance(context, dict):
            context['content'] = content
        else:
            context.vars['content'] = content
        if template is None:
            template = content.template('tex')
        return TexRenderer(
            template=template,
            encoding='utf8',
            texenv=self.texenv,
            ).template.render(context)

SONG_PARSERS = {
    'sgc': ChordproSong,
    }
