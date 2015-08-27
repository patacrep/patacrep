"""Generic parsing classes and methods"""

import logging

LOGGER = logging.getLogger()

class Parser:
    """Parser class"""
    # pylint: disable=too-few-public-methods

    def __init__(self):
        self.filename = "" # Will be overloaded

    @staticmethod
    def __find_column(token):
        """Return the column of ``token``."""
        last_cr = token.lexer.lexdata.rfind('\n', 0, token.lexpos)
        if last_cr < 0:
            last_cr = 0
        column = (token.lexpos - last_cr) + 1
        return column

    @staticmethod
    def error(*, line, column=None, message=""):
        """Display an error message"""
        text = "Line {}".format(line)
        if column is not None:
            text += ", column {}".format(column)
        if message:
            text += ": " + message
        else:
            text += "."
        LOGGER.error(text)

    def p_error(self, token):
        """Manage parsing errors."""
        if token is None:
            self.error(
                line=token.lineno,
                message="Unexpected end of file.",
                )
        else:
            self.error(
                line=token.lineno,
                column=self.__find_column(token),
                )
