"""Errors in song definition (syntax errors, and so on)"""

class SongError:
    """Generic song error"""
    # pylint: disable=too-few-public-methods

    type = "generic"

    def __init__(self, message):
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
        return "Line {}: {}".format(self.line, self.message)

# class FileError(SongError):
#     type = "file"
#
# class LanguageError(SongError):
#     type = "language"
