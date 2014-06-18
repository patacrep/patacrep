#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Songbook exceptions and errors."""

class SongbookError(Exception):
    """Generic songbook error.

    Songbook errors should inherit from this one.
    """
    pass

class SBFileError(SongbookError):
    """Error during songbook file decoding"""

    def __init__(self, message=None):
        super(SBFileError, self).__init__()
        self.message = message

    def __str__(self):
        if self.message is None:
            return str(self.original)
        else:
            return self.message

class TemplateError(SongbookError):
    """Error during template generation"""

    def __init__(self, original, message=None):
        super(TemplateError, self).__init__()
        self.original = original
        self.message = message

    def __str__(self):
        if self.message is None:
            return str(self.original)
        else:
            return self.message

class LatexCompilationError(SongbookError):
    """Error during LaTeX compilation."""

    def __init__(self, basename):
        super(LatexCompilationError, self).__init__()
        self.basename = basename

    def __str__(self):
        return ("""Error while pdfLaTeX compilation of "{basename}.tex" """
                """(see {basename}.log for more information)."""
                ).format(basename=self.basename)

class StepCommandError(SongbookError):
    """Error during custom command compilation."""

    def __init__(self, command, code):
        super(StepCommandError, self).__init__()
        self.command = command
        self.code = code

    def __str__(self):
        return ("""Error while running custom command "{command}": got return"""
                " code {code}.").format(command=self.command, code=self.code)

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

class UnknownStep(SongbookError):
    """Unknown compilation step."""

    def __init__(self, step):
        super(UnknownStep, self).__init__()
        self.step = step

    def __str__(self):
        return """Compilation step "{step}" unknown.""".format(step=self.step)

