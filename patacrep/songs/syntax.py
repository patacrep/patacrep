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

    def p_error(self, token):
        """Manage parsing errors."""
        if token:
            LOGGER.error(
                "Error in file {}, line {}:{}.".format(
                    str(self.filename),
                    token.lineno,
                    self.__find_column(token),
                    )
                )

