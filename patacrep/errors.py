"""Songbook exceptions and errors."""

class SongbookError(Exception):
    """Generic songbook error.

    Songbook errors should inherit from this one.
    """
    pass

class YAMLError(SongbookError):
    """Error during songbook file decoding"""

    def __init__(self, message=None):
        super().__init__()
        self.message = message

    def __str__(self):
        return self.message

class TemplateError(SongbookError):
    """Error during template generation"""

    def __init__(self, original, message=None):
        super().__init__()
        self.original = original
        self.message = message

    def __str__(self):
        if self.message is None:
            return str(self.original)
        else:
            return self.message

class ExecutableNotFound(SongbookError):
    """Couldn't find a LaTeX executable."""

    def __init__(self, executable):
        super().__init__(
            (
                """Could not find the following executable: {executable}"""
                ).format(executable=executable)
            )

class StepError(SongbookError):
    """Error during execution of one compilation step."""

    def __init__(self, message):
        super().__init__()
        self.message = message

    def __str__(self):
        return self.message

class LatexCompilationError(StepError):
    """Error during LaTeX compilation."""

    def __init__(self, basename):
        super().__init__(
            (
                """Error while LaTeX compilation of "{basename}.tex" """
                """(see {basename}.log for more information)."""
                ).format(basename=basename)
            )

class StepCommandError(StepError):
    """Error during custom command compilation."""

    def __init__(self, command, code):
        super().__init__((
            """Error while running custom command "{command}": got return"""
            " code {code}."
            ).format(command=command, code=code))


class CleaningError(SongbookError):
    """Error during cleaning of LaTeX auxiliary files."""

    def __init__(self, filename, exception):
        super().__init__()
        self.filename = filename
        self.exception = exception

    def __str__(self):
        return """Error while removing "{filename}": {exception}.""".format(
            filename=self.filename,
            exception=str(self.exception)
            )

class UnknownStep(StepError):
    """Unknown compilation step."""

    def __init__(self, step):
        super().__init__(
            """Compilation step "{step}" unknown.""".format(step=step)
        )

class ParsingError(SongbookError):
    """Parsing error."""

    def __init__(self, message):
        super().__init__(self)
        self.message = message

    def __str__(self):
        return self.message

class SharedError(SongbookError):
    """Error that is meant to be shared to third party tools using patacrep."""

    def __str__(self):
        raise NotImplementedError()

    @property
    def __dict__(self):
        return {
            'type': self.__class__.__name__,
            'message': str(self),
            'full_message': str(self),
            }

def notfound(filename, paths, message=None):
    """Return a string saying that file was not found in paths."""
    if message is None:
        message = 'File "{name}" not found in directories {paths}.'
    unique_paths = []
    #pylint: disable=expression-not-assigned
    [unique_paths.append(item) for item in paths if item not in unique_paths]
    return message.format(
        name=filename,
        paths=", ".join(['"{}"'.format(item) for item in unique_paths]),
        )
