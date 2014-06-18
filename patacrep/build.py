#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Build a songbook, according to parameters found in a .sb file."""

import codecs
import glob
import logging
import os.path
from subprocess import Popen, PIPE, call

from patacrep import __DATADIR__, authors, content, errors
from patacrep.index import process_sxd
from patacrep.templates import TexRenderer

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
        'lang': 'english',
        'content': [],
        'titleprefixwords': [],
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
        self.contentlist = []
        # Some special keys have their value processed.
        self._set_datadir()

    def _set_datadir(self):
        """Set the default values for datadir"""
        try:
            if isinstance(self.config['datadir'], basestring):
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
                os.path.join(path, 'songs')
                for path in self.config['datadir']
                ]

    def write_tex(self, output):
        """Build the '.tex' file corresponding to self.

        Arguments:
        - output: a file object, in which the file will be written.
        """
        # Updating configuration
        config = DEFAULT_CONFIG
        config.update(self.config)
        renderer = TexRenderer(
                config['template'],
                config['datadir'],
                config['lang'],
                )
        config.update(self.config)
        config.update(renderer.get_variables())

        config['authwords'] = authors.compile_authwords(config['authwords'])

        self.config = config
        # Configuration set

        self.contentlist = content.process_content(
                self.config.get('content', []),
                self.config,
                )
        self.config['render_content'] = content.render_content
        self.config['titleprefixkeys'] = ["after", "sep", "ignore"]
        self.config['content'] = self.contentlist
        self.config['filename'] = output.name[:-4]

        renderer.render_tex(output, self.config)


class SongbookBuilder(object):
    """Provide methods to compile a songbook."""

    # if False, do not expect anything from stdin.
    interactive = False
    # if True, allow unsafe option, like adding the --shell-escape to pdflatex
    unsafe = False
    # Options to add to pdflatex
    _pdflatex_options = []
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
        """
        if function not in self._called_functions:
            self._called_functions[function] = function(*args, **kwargs)
        return self._called_functions[function]

    def _set_latex(self):
        """Set LaTeX options."""
        if self.unsafe:
            self._pdflatex_options.append("--shell-escape")
        if not self.interactive:
            self._pdflatex_options.append("-halt-on-error")

    def build_steps(self, steps=None):
        """Perform steps on the songbook by calling relevant self.build_*()

        Arguments:
        - steps: list of steps to perform to compile songbook. Available steps
          are:
          - tex: build .tex file from templates;
          - pdf: compile .tex using pdflatex;
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
        process = Popen(
                ["pdflatex"] + self._pdflatex_options + [self.basename],
                stdin=PIPE,
                stdout=PIPE,
                stderr=PIPE,
                env=os.environ)
        if not self.interactive:
            process.stdin.close()
        log = ''
        line = process.stdout.readline()
        while line:
            log += line
            line = process.stdout.readline()
        LOGGER.debug(log)

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

    @staticmethod
    def build_custom(command):
        """Run a shell command"""
        LOGGER.info("Running '{}'…".format(command))
        exit_code = call(command, shell=True)
        if exit_code:
            raise errors.StepCommandError(command, exit_code)

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
