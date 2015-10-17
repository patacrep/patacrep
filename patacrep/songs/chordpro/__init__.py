"""Chordpro parser"""

from jinja2 import Environment, FileSystemLoader, contextfunction
import jinja2
import os
import pkg_resources

from patacrep import encoding, files
from patacrep.songs import Song
from patacrep.songs.chordpro.syntax import parse_song
from patacrep.templates import Renderer

class ChordproSong(Song):
    """Chordpros song parser."""

    @staticmethod
    def iter_template_paths(templatedirs, output_format):
        """Iterate over paths in which templates are to be searched.

        :param iterator templatedirs: Iterators of additional directories (the
            default hard-coded template directory is returned last).
        :param str output_format: Song output format, which is appended to
            each directory.
        """
        for directory in templatedirs:
            yield os.path.join(directory, output_format)
        yield os.path.join(
            os.path.abspath(pkg_resources.resource_filename(__name__, 'data')),
            output_format,
            )

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

    def render(self, output_format, output=None, template="song", templatedirs=None): # pylint: disable=arguments-differ
        if templatedirs is None:
            templatedirs = []

        context = {
            'language': self.languages[0],
            "titles": self.titles,
            "authors": self.authors,
            "metadata": self.data,
            "render": self._render_ast,
            "config": self.config,
            "content": self.cached['song'].content,
            }

        jinjaenv = Environment(loader=FileSystemLoader(
            self.iter_template_paths(templatedirs, output_format)
            ))
        jinjaenv.filters['search_image'] = self.search_image
        jinjaenv.filters['search_partition'] = self.search_partition

        try:
            return Renderer(
                template=template,
                encoding='utf8',
                jinjaenv=jinjaenv,
                ).template.render(context)
        except jinja2.exceptions.TemplateNotFound:
            raise NotImplementedError("Cannot convert to format '{}'.".format(output_format))

    @staticmethod
    @contextfunction
    def _render_ast(context, content):
        """Render ``content``."""
        context.vars['content'] = content
        return context.environment.get_template(content.template()).render(context)

SONG_PARSERS = {
    'sgc': ChordproSong,
    }
