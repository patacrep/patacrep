"""Errors in song definition (syntax errors, and so on)"""

from patacrep.errors import SharedError

class SongError(SharedError):
    """Generic song error"""
    # pylint: disable=too-few-public-methods

    def __init__(self, song, message):
        super().__init__()
        self.song = song
        self.message = message

    def __str__(self):
        return "{}: {}".format(self._human_song(), self.message)

    def _human_song(self):
        return "Datadir '{}', song '{}'".format(
            self.song.datadir,
            self.song.subpath,
            )

class SongSyntaxError(SongError):
    """Syntax error"""
    # pylint: disable=too-few-public-methods

    def __init__(self, song, line, message):
        super().__init__(song, message)
        #: Line of error. May be `None` if irrelevant.
        self.line = line

    def __str__(self):
        if self.line is not None:
            return "{}, line {}: {}".format(self._human_song(), self.line, self.message)
        else:
            return "{}: {}".format(self._human_song(), self.message)

class FileNotFound(SongError):
    """File not found error"""

    def __init__(self, song, filename):
        super().__init__(song, "File '{}' not found.".format(filename))

class SongUnknownLanguage(SongError):
    """Song language is not known."""

    def __init__(self, song, original, fallback, message):
        super().__init__(song, message)
        self.original = original
        self.fallback = fallback
