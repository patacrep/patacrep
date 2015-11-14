"""Generic parsing classes and methods"""

import logging

from patacrep.songs import errors

LOGGER = logging.getLogger()

class Parser:
    """Parser class"""
    # pylint: disable=too-few-public-methods

    def __init__(self):
        self.filename = "" # Will be overloaded
        self._errors = []

    @staticmethod
    def __find_column(token):
        """Return the column of ``token``."""
        last_cr = token.lexer.lexdata.rfind('\n', 0, token.lexpos)
        if last_cr < 0:
            last_cr = 0
        column = (token.lexpos - last_cr) + 1
        return column

    def error(self, *, line=None, column=None, message=""):
        """Display an error message"""
        coordinates = []
        if line is not None:
            coordinates.append("line {}".format(line))
        if column is not None:
            coordinates.append("column {}".format(column))
        text = ", ".join(coordinates)
        if message and text:
            text += ": " + message
        elif message:
            text += message
        else:
            text += "."
        if self.filename is None:
            LOGGER.error(text)
        else:
            LOGGER.error("File {}: {}".format(self.filename, text))

    def p_error(self, token):
        """Manage parsing errors."""
        if token is None:
            error = errors.SongSyntaxError(
                line=None,
                message="Unexpected end of file.",
                )
            self.error(message=error.message)
        else:
            error = errors.SongSyntaxError(
                line=token.lineno,
                message="Syntax error",
                )
            self.error(
                line=error.line,
                column=self.__find_column(token),
                )
