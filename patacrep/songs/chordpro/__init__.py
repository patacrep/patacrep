"""Chordpro parser"""

import logging
import operator
import os

from jinja2 import Environment, FileSystemLoader, ChoiceLoader
from jinja2 import contextfunction
import jinja2

from patacrep import encoding, files, pkg_datapath
from patacrep.songs import Song
from patacrep.songs.chordpro.syntax import parse_song
from patacrep.songs.errors import FileNotFound, SongUnknownLanguage
from patacrep.templates import Renderer
from patacrep.latex import lang2babel, UnknownLanguage

LOGGER = logging.getLogger(__name__)

def sort_directive_argument(directives):
    """Sort directives by their argument."""
    return sorted(directives, key=operator.attrgetter("argument"))

DEFAULT_FILTERS = {
    'sortargs': sort_directive_argument,
    }

class ChordproSong(Song):
    """Chordpro song parser"""
    # pylint: disable=abstract-method

    output_language = None
    _translation_map = {}

    def _parse(self):
        """Parse content, and return the dictionary of song data."""
        with encoding.open_read(self.fullpath, encoding=self.encoding) as song:
            song = parse_song(song.read(), self.fullpath)
        self.authors = song.authors
        self.titles = song.titles
        self.lang = song.get_data_argument('language', self.lang)
        self.data = song.meta
        self.errors = [error(song=self) for error in song.error_builders]
        self.cached = {
            'song': song,
            }

    def _filters(self):
        """Return additional jinja2 filters."""
        filters = DEFAULT_FILTERS.copy()
        filters.update({
            'search_image': self.search_image,
            'search_partition': self.search_partition,
            'escape_specials': self._escape_specials,
        })
        return filters

    def render(self, template="song"): # pylint: disable=arguments-differ
        context = {
            'lang': self.lang,
            "titles": self.titles,
            "authors": self.authors,
            "metadata": self.data,
            "render": self._render_ast,
            "content": self.cached['song'].content,
            }

        jinjaenv = Environment(loader=FileSystemLoader(
            self.iter_datadirs("templates", "songs", "chordpro", self.output_language)
            ))
        jinjaenv.filters.update(self._filters())

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

    def _escape_specials(self, content, chars):
        return str(content).translate(str.maketrans({
            key: value
            for key, value in self._translation_map.items()
            if key in chars
            }))

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
            message = "Song '{}' (datadir '{}'): Score '{}' not found.".format(
                self.subpath, self.datadir, filename
                )
            self.errors.append(FileNotFound(self, filename))
            LOGGER.warning(message)
            return None

    def search_image(self, filename):
        try:
            return os.path.join("img", super().search_image(filename))
        except FileNotFoundError:
            message = "Song '{}' (datadir '{}'): Image '{}' not found.".format(
                self.subpath, self.datadir, filename
                )
            self.errors.append(FileNotFound(self, filename))
            LOGGER.warning(message)
            return None

    def _filters(self):
        parent = super()._filters()
        parent.update({
            'lang2babel': self.lang2babel,
            })
        return parent

    def lang2babel(self, lang):
        """Return the LaTeX babel code corresponding to `lang`.

        Add an error to the list of errors if argument is invalid.
        """
        try:
            return lang2babel(lang)
        except UnknownLanguage as error:
            new_error = SongUnknownLanguage(
                self,
                error.original,
                error.fallback,
                error.message,
                )
            LOGGER.warning(new_error)
            self.errors.append(new_error)
            return error.babel

class Chordpro2ChordproSong(ChordproSong):
    """Render chordpro song to chordpro code"""

    output_language = "chordpro"
    _translation_map = {
        '{': r'\{',
        '}': r'\}',
        '\\': '\\\\',
        '#': r'\#',
    }

    def search_file(self, filename, extensions=None, *, datadirs=None):
        # pylint: disable=unused-variable
        return filename

SONG_RENDERERS = {
    "tsg": {
        'csg': Chordpro2LatexSong,
        },
    "html": {
        'csg': Chordpro2HtmlSong,
        },
    "csg": {
        'csg': Chordpro2ChordproSong,
        },
    }
