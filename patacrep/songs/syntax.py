"""Generic parsing classes and methods"""

import functools
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
        """Record and display an error message"""
        self._errors.append(functools.partial(
            errors.SongSyntaxError,
            line=line,
            message=message,
        ))

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
            LOGGER.warning(text)
        else:
            LOGGER.warning("Song {}: {}".format(self.filename, text))

    def p_error(self, token):
        """Manage parsing errors."""
        if token is None:
            self.error(message="Unexpected end of file.")
        else:
            self.error(
                message="Syntax error",
                line=token.lineno,
                column=self.__find_column(token),
                )
