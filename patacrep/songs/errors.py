"""Errors in song definition (syntax errors, and so on)"""

class SongError(Exception):
    """Generic song error"""
    # pylint: disable=too-few-public-methods

    type = "generic"

    def __init__(self, message):
        super().__init__()
        self.message = message

    def __str__(self):
        raise NotImplementedError()

class SongSyntaxError(SongError):
    """Syntax error"""
    # pylint: disable=too-few-public-methods

    type = "syntax"

    def __init__(self, line, message):
        super().__init__(message)
        #: Line of error. May be `None` if irrelevant.
        self.line = line

    def __str__(self):
        if self.line is not None:
            return "Line {}: {}".format(self.line, self.message)
        else:
            return self.message

# class FileError(SongError):
#     type = "file"
#
# class LanguageError(SongError):
#     type = "language"
