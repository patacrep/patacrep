"""Chordpro parser"""

from jinja2 import Environment, FileSystemLoader, contextfunction
import pkg_resources
import os

from patacrep import encoding, files
from patacrep.songs import Song
from patacrep.songs.chordpro.syntax import parse_song
from patacrep.templates import Renderer

class ChordproSong(Song):
    """Chordpros song parser."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.template_paths = [os.path.abspath(pkg_resources.resource_filename(__name__, 'data'))]

    def add_template_path(self, absolute_path):
        """Add a template path (at the beginning, so that it's choosen first)."""
        self.template_paths.insert(0, absolute_path)

    def get_template_paths(self, output_format):
        """Get the template path for a given output_format."""
        return [os.path.join(path, output_format) for path in self.template_paths]

    def _parse(self, config):
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

    def render(self, output, output_format, content=None, template="song"): # pylint: disable=arguments-differ
        if content is None:
            content = self.cached['song'].content
        context = {
            'language': self.languages[0],
            "titles": self.titles,
            "authors": self.authors,
            "metadata": self.data,
            "render": self._render_ast,
            "config": self.config,
            "content": content,
            }

        jinjaenv = Environment(loader=FileSystemLoader(
            self.get_template_paths(output_format)
            ))
        jinjaenv.filters['search_image'] = self.search_image
        jinjaenv.filters['search_partition'] = self.search_partition

        return Renderer(
            template=template,
            encoding='utf8',
            jinjaenv=jinjaenv,
            ).template.render(context)

    @staticmethod
    @contextfunction
    def _render_ast(context, content):
        """Render ``content``."""
        context.vars['content'] = content
        return context.environment.get_template(content.template()).render(context)

SONG_PARSERS = {
    'sgc': ChordproSong,
    }
