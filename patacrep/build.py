"""Build a songbook, according to parameters found in a .yaml file."""

import codecs
import copy
import glob
import logging
import threading
import os.path
from subprocess import Popen, PIPE, call, check_call

import yaml

from patacrep import authors, content, encoding, errors, pkg_datapath, utils
from patacrep.index import process_sxd
from patacrep.templates import TexBookRenderer, iter_bookoptions

LOGGER = logging.getLogger(__name__)
EOL = "\n"
DEFAULT_STEPS = ['tex', 'pdf', 'sbx', 'pdf', 'clean']
GENERATED_EXTENSIONS = [
    "_auth.sbx",
    "_auth.sxd",
    ".aux",
    ".log",
    ".out",
    ".sxc",
    ".tex",
    "_title.sbx",
    "_title.sxd",
    ]

# pylint: disable=too-few-public-methods
class Songbook:
    """Represent a songbook (.yaml) file.

    - Low level: provide a Python representation of the values stored in the
      '.yaml' file.
    - High level: provide some utility functions to manipulate these data.
    """

    def __init__(self, raw_songbook, basename):
        # Validate config
        schema = config_model('schema')

        try:
            utils.validate_yaml_schema(raw_songbook, schema)
        except errors.SchemaError as exception:
            exception.message = "The songbook file '{}' is not valid\n".format(basename)
            raise exception

        self._raw_config = raw_songbook
        self.basename = basename
        self._errors = list()
        self._config = dict()

    def get_content_items(self):
        """Return: a list of ContentItem objects, corresponding to the content to be
        included in the .tex file.
        """
        content_config = self._raw_config.copy()
        # Updates the '_langs' key
        content_items = content.process_content(
            content_config.get('content', []),
            content_config,
            )
        content_langs = content_config['_langs']
        return content_langs, content_items

    def write_tex(self, output):
        """Build the '.tex' file corresponding to self.

        Arguments:
        - output: a file object, in which the file will be written.
        """
        # Updating configuration
        tex_config = self._raw_config.copy()
        renderer = TexBookRenderer(
            tex_config['book']['template'],
            tex_config['_datadir'],
            tex_config['book']['lang'],
            tex_config['book']['encoding'],
            )

        try:
            tex_config['_template'] = renderer.get_all_variables(tex_config.get('template', {}))
        except errors.SchemaError as exception:
            exception.message = "The songbook file '{}' is not valid\n{}".format(
                self.basename, exception.message)
            raise exception

        tex_config['_compiled_authwords'] = authors.compile_authwords(
            copy.deepcopy(tex_config['authors'])
            )

        # Configuration set
        tex_config['render'] = content.render
        tex_config['_langs'], tex_config['content'] = self.get_content_items()
        tex_config['filename'] = output.name[:-4]

        # Processing special options
        tex_config['_bookoptions'] = iter_bookoptions(tex_config)
        tex_config['chords']['_notenames'] = self._get_chord_names(
            tex_config['chords']['notation']
            )

        renderer.render_tex(output, tex_config)

        # Get all errors, and maybe exit program
        self._errors.extend(renderer.errors)
        if tex_config['_error'] == "failonbook":
            if self.has_errors():
                raise errors.SongbookError("Some songs contain errors. Stopping as requested.")

    @staticmethod
    def _get_chord_names(notation):
        """Return a list of chord names, given the user option."""
        if notation == "alphascale":
            return ["A", "B", "C", "D", "E", "F", "G"]
        if notation == "solfedge":
            return ["La", "Si", "Do", r"R\'e", "Mi", "Fa", "Sol"]
        return notation

    def has_errors(self):
        """Return `True` iff errors have been encountered in the book.

        Note that `foo.has_errors() == False` does not means that the book has
        not any errors: it does only mean that no error has been found yet.
        """
        for _ in self.iter_errors():
            return True
        return False

    def iter_errors(self):
        """Iterate over errors of book and book content."""
        yield from self._errors
        contentlist = self._config.get('content', content.ContentList())
        yield from contentlist.iter_errors()

    def iter_flat_errors(self):
        """Iterate over errors, in an exportable format.

        This function does the same job as :func:`iter_errors`, exepted that
        the errors are represented as dictionaries of standard python types.

        Each error (dictionary) contains the following keys:
        - `type`: the error type (as the class name of the error);
        - `message`: Error message, that does not include the error location (datadir, song, etc.);
        - `full_message`: Error message, containing the full error location;
        - depending on the error type, more keys may be present in the error.
        """
        for error in self.iter_errors():
            yield vars(error)

    def requires_lilypond(self):
        """Tell if lilypond is part of the bookoptions"""
        return 'lilypond' in iter_bookoptions(self._raw_config)

def _log_pipe(pipe):
    """Log content from `pipe`."""
    while 1:
        line = pipe.readline()
        if not bool(line):
            break
        LOGGER.debug(line.strip())

class SongbookBuilder:
    """Provide methods to compile a songbook."""

    # if False, do not expect anything from stdin.
    interactive = False
    # if True, allow unsafe option, like adding the --shell-escape to lualatex
    unsafe = False
    # Options to add to lualatex
    _lualatex_options = []
    # Dictionary of functions that have been called by self._run_once(). Keys
    # are function; values are return values of functions.
    _called_functions = {}

    def __init__(self, raw_songbook):
        # Basename of the songbook to be built.
        self.basename = raw_songbook['_outputname']
        # Representation of the .yaml songbook configuration file.
        self.songbook = Songbook(raw_songbook, self.basename)

    def _run_once(self, function, *args, **kwargs):
        """Run function if it has not been run yet.

        If it as, return the previous return value.

        Warning: several function calls with different arguments return the
        same value.
        """
        if function not in self._called_functions:
            self._called_functions[function] = function(*args, **kwargs)
        return self._called_functions[function]

    def _set_latex(self):
        """Set LaTeX options."""
        if self.unsafe:
            self._lualatex_options.append("--shell-escape")
        if not self.interactive:
            self._lualatex_options.append("-halt-on-error")

    def build_steps(self, steps=None):
        """Perform steps on the songbook by calling relevant self.build_*()

        Arguments:
        - steps: list of steps to perform to compile songbook. Available steps
          are:
          - tex: build .tex file from templates;
          - pdf: compile .tex using lualatex;
          - sbx: compile song and author indexes;
          - clean: remove temporary files,
          - any string beginning with a sharp sign (#): it is interpreted as a
            command to run in a shell.
        """
        if not steps:
            steps = DEFAULT_STEPS

        for step in steps:
            if step == 'tex':
                self.build_tex()
            elif step == 'pdf':
                self.build_pdf()
            elif step == 'sbx':
                self.build_sbx()
            elif step == 'clean':
                self.clean()
            elif step.startswith("#"):
                self.build_custom(step[1:])
            else:
                # Unknown step name
                raise errors.UnknownStep(step)

    def build_tex(self):
        """Build .tex file from templates"""
        LOGGER.info("Building '{}.tex'…".format(self.basename))
        with codecs.open(
            "{}.tex".format(self.basename), 'w', 'utf-8',
            ) as output:
            self.songbook.write_tex(output)

    def build_pdf(self):
        """Build .pdf file from .tex file"""
        LOGGER.info("Building '{}.pdf'…".format(self.basename))
        self._run_once(self._set_latex)

        compiler = "lualatex"

        # Test if the LaTeX compiler is accessible
        try:
            check_call(
                [compiler, "--version"],
                stdin=PIPE,
                stdout=PIPE,
                stderr=PIPE,
                universal_newlines=True,
                )
        except FileNotFoundError as error:
            raise errors.ExecutableNotFound(compiler)

        # Test if lilypond compiler is accessible
        if self.songbook.requires_lilypond():
            lilypond_compiler = 'lilypond'
            try:
                check_call(
                    [lilypond_compiler, "--version"],
                    stdin=PIPE,
                    stdout=PIPE,
                    stderr=PIPE,
                    universal_newlines=True,
                    )
            except FileNotFoundError as error:
                raise errors.ExecutableNotFound(lilypond_compiler)

        # Perform compilation
        try:
            process = Popen(
                [compiler] + self._lualatex_options + [self.basename],
                stdin=PIPE,
                stdout=PIPE,
                stderr=PIPE,
                universal_newlines=True,
                )
        except Exception as error:
            LOGGER.debug(error)
            raise errors.LatexCompilationError(self.basename)

        if not self.interactive:
            process.stdin.close()

        standard_output = threading.Thread(
            target=_log_pipe,
            kwargs={
                'pipe' : process.stdout,
                }
            )
        standard_error = threading.Thread(
            target=_log_pipe,
            kwargs={
                'pipe' : process.stderr,
                }
            )
        standard_output.daemon = True
        standard_error.daemon = True
        standard_error.start()
        standard_output.start()
        standard_error.join()
        standard_output.join()
        process.wait()

        # Close the stdout and stderr to prevent ResourceWarning:
        process.stdout.close()
        process.stderr.close()

        if process.returncode:
            raise errors.LatexCompilationError(self.basename)

    def build_sbx(self):
        """Make .sbx indexes from .sxd files"""
        LOGGER.info("Building .sbx indexes…")
        sxd_files = glob.glob("%s_*.sxd" % self.basename)
        for sxd_file in sxd_files:
            LOGGER.debug("Processing " + sxd_file)
            idx = process_sxd(sxd_file)
            with codecs.open(sxd_file[:-3] + "sbx", "w", "utf-8") as index_file:
                index_file.write(idx.entries_to_str())

    def _get_interpolation(self):
        """Return the interpolation values for a custom command."""
        interpolation = {
            "basename": self.basename,
            }
        for index in ['title', 'auth']:
            interpolation.update({
                '{}_{}'.format(index, extension): '{}_{}.{}'.format(self.basename, index, extension)
                for extension in ['sbx', 'sxd']
                })
        interpolation.update({
            extension: '{}.{}'.format(self.basename, extension)
            for extension in ["aux", "log", "out", "pdf", "sxc", "tex"]
            })
        return interpolation

    def build_custom(self, command):
        """Run a shell command"""
        interpolation = self._run_once(self._get_interpolation)
        try:
            formatted_command = command.format(**interpolation)
        except KeyError as error:
            raise errors.StepError((
                'Custom step: Unknown key "{{{error}}}" in command "{command}".'
                ).format(error=error.args[0], command=command))
        LOGGER.info("Running '{}'…".format(formatted_command))
        exit_code = call(formatted_command, shell=True)
        if exit_code:
            raise errors.StepCommandError(formatted_command, exit_code)

    def clean(self):
        """Clean (some) temporary files used during compilation.

        Depending of the LaTeX modules used in the template, there may be others
        that are not deleted by this function."""
        LOGGER.info("Cleaning…")
        for ext in GENERATED_EXTENSIONS:
            if os.path.isfile(self.basename + ext):
                try:
                    os.unlink(self.basename + ext)
                except Exception as exception:
                    raise errors.CleaningError(self.basename + ext, exception)


def config_model(key):
    """Get the model structure

    key can be:
        - schema
        - default
        - description
    """
    model_path = pkg_datapath('templates', 'songbook_model.yml')
    with encoding.open_read(model_path) as model_file:
        data = yaml.safe_load(model_file)

    return data.get(key, {})
