#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Songbook exceptions and errors."""

class SongbookError(Exception):
    """Generic songbook error.

    Songbook errors should inherit from this one.
    """
    pass

class LatexCompilationError(SongbookError):
    """Error during LaTeX compilation."""

    def __init__(self, basename):
        super(LatexCompilationError, self).__init__()
        self.basename = basename

    def __str__(self):
        return (
                """Error while pdfLaTeX compilation of "{basename}.tex"
                (see {basename}.log for more information)."""
                ).format(basename=self.basename)

class CleaningError(SongbookError):
    """Error during cleaning of LaTeX auxiliary files."""

    def __init__(self, filename, exception):
        super(CleaningError, self).__init__()
        self.filename = filename
        self.exception = exception

    def __str__(self):
        return """Error while removing "{filename}": {exception}.""".format(
                filename=self.filename,
                exception=str(self.exception)
                )
