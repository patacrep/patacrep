"""Chordpro parser"""

from jinja2 import Environment, FileSystemLoader, contextfunction, ChoiceLoader
import jinja2
import logging
import operator
import os

from patacrep import encoding, files, pkg_datapath
from patacrep.songs import Song
from patacrep.songs.chordpro.syntax import parse_song
from patacrep.templates import Renderer
from patacrep.latex import lang2babel
from patacrep.files import path2posix

LOGGER = logging.getLogger(__name__)

def sort_directive_argument(directives):
    """Sort directives by their argument."""
    return sorted(directives, key=operator.attrgetter("argument"))

class ChordproSong(Song):
    """Chordpro song parser"""
    # pylint: disable=abstract-method

    output_language = None

    def _parse(self):
        """Parse content, and return the dictionary of song data."""
        with encoding.open_read(self.fullpath, encoding=self.encoding) as song:
            song = parse_song(song.read(), self.fullpath)
        self.authors = song.authors
        self.titles = song.titles
        self.lang = song.get_data_argument('language', self.default_lang)
        self.data = song.meta
        self.cached = {
            'song': song,
            }

    def render(self, template="song"): # pylint: disable=arguments-differ
        context = {
            'lang': self.lang,
            "titles": self.titles,
            "authors": self.authors,
            "metadata": self.data,
            "render": self._render_ast,
            "config": self.config,
            "content": self.cached['song'].content,
            }

        jinjaenv = Environment(loader=FileSystemLoader(
            self.iter_datadirs("templates", "songs", "chordpro", self.output_language)
            ))
        jinjaenv.filters['search_image'] = self.search_image
        jinjaenv.filters['search_partition'] = self.search_partition
        jinjaenv.filters['lang2babel'] = lang2babel
        jinjaenv.filters['sortargs'] = sort_directive_argument
        jinjaenv.filters['path2posix'] = path2posix

        try:
            return Renderer(
                template=template,
                encoding='utf8',
                jinjaenv=jinjaenv,
                ).template.render(context)
        except jinja2.exceptions.TemplateNotFound:
            raise NotImplementedError("Cannot convert to format '{}'.".format(self.output_language))

    @staticmethod
    @contextfunction
    def _render_ast(context, content):
        """Render ``content``."""
        context.vars['content'] = content
        return context.environment.get_template(content.template()).render(context)

class Chordpro2HtmlSong(ChordproSong):
    """Render chordpro song to html code"""

    output_language = "html"

    def search_file(self, filename, extensions=None, *, datadirs=None):
        try:
            datadir, filename, extension = self.search_datadir_file(filename, extensions, datadirs)
            return os.path.join(datadir, filename + extension)
        except FileNotFoundError:
            LOGGER.warning(
                "Song '%s' (datadir '%s'): File '%s' not found.",
                self.subpath, self.datadir, filename,
                )
            return None

class Chordpro2LatexSong(ChordproSong):
    """Render chordpro song to latex code"""

    output_language = "latex"

    def search_file(self, filename, extensions=None, *, datadirs=None):
        _datadir, filename, _extension = self.search_datadir_file(
            filename,
            extensions,
            datadirs,
            )
        return filename

    def search_partition(self, filename):
        try:
            return os.path.join("scores", super().search_partition(filename))
        except FileNotFoundError:
            LOGGER.warning(
                "Song '%s' (datadir '%s'): Score '%s' not found.",
                self.subpath, self.datadir, filename,
                )
            return None

    def search_image(self, filename):
        try:
            return os.path.join("img", super().search_image(filename))
        except FileNotFoundError:
            LOGGER.warning(
                "Song '%s' (datadir '%s'): Image '%s' not found.",
                self.subpath, self.datadir, filename,
                )
            return None

class Chordpro2ChordproSong(ChordproSong):
    """Render chordpro song to chordpro code"""

    output_language = "chordpro"

    def search_file(self, filename, extensions=None, *, datadirs=None):
        # pylint: disable=unused-variable
        return filename

SONG_RENDERERS = {
    "latex": {
        'sgc': Chordpro2LatexSong,
        },
    "html": {
        'sgc': Chordpro2HtmlSong,
        },
    "chordpro": {
        'sgc': Chordpro2ChordproSong,
        },
    }
