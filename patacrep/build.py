"""Build a songbook, according to parameters found in a .sb file."""

import codecs
import copy
import glob
import logging
import threading
import os.path
from subprocess import Popen, PIPE, call

from patacrep import __DATADIR__, authors, content, errors, files
from patacrep.index import process_sxd
from patacrep.templates import TexBookRenderer
from patacrep.songs import DataSubpath

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
DEFAULT_CONFIG = {
    'template': "default.tex",
    'lang': 'en',
    'content': [],
    'titleprefixwords': [],
    'encoding': None,
    'datadir': [],
    }



# pylint: disable=too-few-public-methods
class Songbook(object):
    """Represent a songbook (.sb) file.

    - Low level: provide a Python representation of the values stored in the
      '.sb' file.
    - High level: provide some utility functions to manipulate these data.
    """

    def __init__(self, raw_songbook, basename):
        super(Songbook, self).__init__()
        self.config = raw_songbook
        self.basename = basename
        # Some special keys have their value processed.
        self._set_datadir()

    def _set_datadir(self):
        """Set the default values for datadir"""
        try:
            if isinstance(self.config['datadir'], str):
                self.config['datadir'] = [self.config['datadir']]
        except KeyError:  # No datadir in the raw_songbook
            self.config['datadir'] = [os.path.abspath('.')]

        abs_datadir = []
        for path in self.config['datadir']:
            if os.path.exists(path) and os.path.isdir(path):
                abs_datadir.append(os.path.abspath(path))
            else:
                LOGGER.warning(
                    "Ignoring non-existent datadir '{}'.".format(path)
                    )

        abs_datadir.append(__DATADIR__)

        self.config['datadir'] = abs_datadir
        self.config['_songdir'] = [
            DataSubpath(path, 'songs')
            for path in self.config['datadir']
            ]

    def write_tex(self, output):
        """Build the '.tex' file corresponding to self.

        Arguments:
        - output: a file object, in which the file will be written.
        """
        # Updating configuration
        config = DEFAULT_CONFIG.copy()
        config.update(self.config)
        renderer = TexBookRenderer(
            config['template'],
            config['datadir'],
            config['lang'],
            config['encoding'],
            )
        config.update(renderer.get_variables())
        config.update(self.config)

        config['_compiled_authwords'] = authors.compile_authwords(
            copy.deepcopy(config['authwords'])
            )

        # Loading custom plugins
        config['_content_plugins'] = files.load_plugins(
            datadirs=config.get('datadir', []),
            root_modules=['content'],
            keyword='CONTENT_PLUGINS',
            )
        config['_song_plugins'] = files.load_plugins(
            datadirs=config.get('datadir', []),
            root_modules=['songs'],
            keyword='SONG_RENDERERS',
            )['latex']

        # Configuration set
        config['render'] = content.render
        config['content'] = content.process_content(
            config.get('content', []),
            config,
            )
        config['filename'] = output.name[:-4]

        renderer.render_tex(output, config)

def _log_pipe(pipe):
    """Log content from `pipe`."""
    while 1:
        line = pipe.readline()
        if not bool(line):
            break
        LOGGER.debug(line.strip())

class SongbookBuilder(object):
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

    def __init__(self, raw_songbook, basename):
        # Representation of the .sb songbook configuration file.
        self.songbook = Songbook(raw_songbook, basename)
        # Basename of the songbook to be built.
        self.basename = basename

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
        for datadir in self.songbook.config["datadir"]:
            self._lualatex_options.append(
                '--include-directory="{}"'.format(datadir)
                )

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

        try:
            process = Popen(
                ["lualatex"] + self._lualatex_options + [self.basename],
                stdin=PIPE,
                stdout=PIPE,
                stderr=PIPE,
                env=os.environ,
                cwd=os.getcwd(),
                universal_newlines=True,
                )
        except Exception as error:
            LOGGER.debug(error)
            LOGGER.debug(os.getcwd())
            import subprocess
            LOGGER.debug(subprocess.check_output(
                ['dir', os.getcwd()],
                stderr=subprocess.STDOUT,
                universal_newlines=True
                ))
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

        if process.returncode:
            raise errors.LatexCompilationError(self.basename)

    def build_sbx(self):
        """Make index"""
        LOGGER.info("Building indexes…")
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
