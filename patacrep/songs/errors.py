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
        return "Song {}: {}".format(self.song, self.message)

class SongSyntaxError(SongError):
    """Syntax error"""
    # pylint: disable=too-few-public-methods

    def __init__(self, song, line, message):
        super().__init__(song, message)
        #: Line of error. May be `None` if irrelevant.
        self.line = line

    def __str__(self):
        if self.line is not None:
            return "Song {}, line {}: {}".format(self.song, self.line, self.message)
        else:
            return "Song {}: {}".format(self.song, self.message)

class FileNotFound(SongError):
    """File not found error"""

    def __init__(self, song, filename):
        super().__init__(song, "File '{}' not found.".format(filename))
