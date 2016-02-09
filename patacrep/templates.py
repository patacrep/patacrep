"""Template for .tex generation settings and utilities"""

import logging
import re

import yaml

from jinja2 import Environment, FileSystemLoader, ChoiceLoader, \
        TemplateNotFound, nodes
from jinja2.ext import Extension
from jinja2.meta import find_referenced_templates

from patacrep import errors, files, utils
from patacrep.latex import lang2babel, UnknownLanguage
import patacrep.encoding

LOGGER = logging.getLogger(__name__)

_LATEX_SUBS = (
    (re.compile(r'\\'), r'\\textbackslash'),
    (re.compile(r'([{}_#%&$])'), r'\\\1'),
    (re.compile(r'~'), r'\~{}'),
    (re.compile(r'\^'), r'\^{}'),
    (re.compile(r'"'), r"''"),
    (re.compile(r'\.\.\.+'), r'\\ldots'),
)

_VARIABLE_REGEXP = re.compile(
    r"""
    \(\*-?\ *variables\ *\*\)    # Match (* variables *) or (*- variables *)
    (                            # Match and capture the following:
    (?:                          # Start of non-capturing group, used to match a single character
    (?!                          # only if it's impossible to match the following:
    \(\*-?\ *                    # - a literal (* or (*-
    (?:                          # Inner non-capturing group, used for the following alternation:
    variables                    # - Either match the word variables
    |                            # or
    endvariables                 # - the word endvariables
    )                            # End of inner non-capturing group
    \ *-?\*\)                    # - a literal *) or -*)
    )                            # End of negative lookahead assertion
    .                            # Match any single character
    )*                           # Repeat as often as possible
    )                            # End of capturing group 1
    \(\*\ *endvariables\ *-?\*\) # until (* endvariables *) or (* endvariables -*) is matched.
    """,
    re.VERBOSE|re.DOTALL)

def _escape_tex(value):
    '''Escape TeX special characters'''
    newval = value
    for pattern, replacement in _LATEX_SUBS:
        newval = pattern.sub(replacement, newval)
    return newval

DEFAULT_FILTERS = {
    "escape_tex": _escape_tex,
    "iter_datadirs": files.iter_datadirs,
    "path2posix": files.path2posix,
    }

class VariablesExtension(Extension):
    """Extension to jinja2 to silently ignore variable block.
    Instead, they are parsed by this module.
    """
    # pylint: disable=too-few-public-methods
    tags = set(['variables'])

    def parse(self, parser):
        next(parser.stream)
        parser.parse_statements(
            end_tokens=['name:endvariables'],
            drop_needle=True,
            )
        return nodes.Const("") # pylint: disable=no-value-for-parameter


class Renderer:
    """Render a template to a LaTeX file."""
    # pylint: disable=too-few-public-methods

    def __init__(self, template, jinjaenv, encoding=None):
        self.errors = []
        self.encoding = encoding
        self.jinjaenv = jinjaenv
        self.jinjaenv.block_start_string = '(*'
        self.jinjaenv.block_end_string = '*)'
        self.jinjaenv.variable_start_string = '(('
        self.jinjaenv.variable_end_string = '))'
        self.jinjaenv.comment_start_string = '(% comment %)'
        self.jinjaenv.comment_end_string = '(% endcomment %)'
        self.jinjaenv.line_comment_prefix = '%!'
        self.jinjaenv.trim_blocks = True
        self.jinjaenv.lstrip_blocks = True
        # Fill default filters
        for key, value in self.filters().items():
            if key not in self.jinjaenv.filters:
                self.jinjaenv.filters[key] = value

        self.template = self.jinjaenv.get_template(template)

    def filters(self):
        """Return a dictionary of jinja2 filters."""
        filters = DEFAULT_FILTERS.copy()
        filters.update({
            "lang2babel": self.lang2babel,
            })
        return filters

    def lang2babel(self, lang):
        """Return the LaTeX babel code corresponding to `lang`.

        Add an error to the list of errors if argument is invalid.
        """
        try:
            return lang2babel(lang)
        except UnknownLanguage as error:
            error.message = "Songbook: {}".format(error.message)
            LOGGER.warning(error.message)
            self.errors.append(error)
            return error.babel

class TexBookRenderer(Renderer):
    """Tex renderer for the whole songbook"""

    def __init__(self, template, datadirs, lang, encoding=None):
        '''Start a new jinja2 environment for .tex creation.

        Arguments:
        - template: name of the template to use.
        - datadirs: list of locations of the data directory
          (which may contain file <datadir>/templates/<template>).
        - lang: main language of songbook.
        - encoding: if set, encoding of the template.
        '''
        self.lang = lang
        # Load templates in filesystem ...
        loaders = [
            FileSystemLoader(datadir)
            for datadir in files.iter_datadirs(datadirs, 'templates')
            ]
        jinjaenv = Environment(
            loader=ChoiceLoader(loaders),
            extensions=[VariablesExtension],
            )
        try:
            super().__init__(template, jinjaenv, encoding)
        except TemplateNotFound as exception:
            # Only works if all loaders are FileSystemLoader().
            paths = [
                item
                for loader in self.jinjaenv.loader.loaders
                for item in loader.searchpath
                ]
            raise errors.TemplateError(
                exception,
                errors.notfound(
                    exception.name,
                    paths,
                    message='Template "{name}" not found in {paths}.'
                    ),
                )

    def get_all_variables(self, user_config):
        '''Validate template variables (and set defaults when needed)
        '''
        data = self.get_template_variables(self.template)
        variables = dict()
        for templatename, param in data.items():
            template_config = user_config.get(templatename, {})
            variables[templatename] = self._get_variables(param, template_config)
        return variables

    @staticmethod
    def _get_variables(parameter, user_config):
        '''Get the default value for the parameter, according to the language.

        May raise an errors.SBFileError if the data does not respect the schema
        '''
        data = utils.DictOfDict(parameter.get('default', {}))
        data.update(user_config)

        schema = parameter.get('schema', {})
        utils.validate_yaml_schema(data, schema)

        return data

    def get_template_variables(self, basetemplate):
        """Parse the template to extract the variables as a dictionary.

        If the template includes or extends other templates, load them as well.

        Arguments:
        - basetemplate: the name of the template, as a string.
          in 'template' (or one of its subtemplates), it is not parsed.
        """
        variables = {}
        for templatename, template in self._iter_template_content(basetemplate):
            match = re.findall(_VARIABLE_REGEXP, template)
            if not match:
                continue
            if templatename not in variables:
                variables[templatename] = {}
            for variables_string in match:
                try:
                    variables[templatename].update(yaml.load(variables_string))
                except ValueError as exception:
                    raise errors.TemplateError(
                        exception,
                        (
                            "Error while parsing yaml in file "
                            "{filename}. The yaml string was:"
                            "\n'''\n{yamlstring}\n'''"
                        ).format(
                            filename=template.filename,
                            yamlstring=variables_string,
                            )
                        )
        return variables

    def _iter_template_content(self, templatename, *, skip=None):
        """Iterate over template (and subtemplate) content."""
        if skip is None:
            skip = []
        template = self.jinjaenv.get_template(templatename)
        with patacrep.encoding.open_read(
            template.filename,
            encoding=self.encoding
            ) as contentfile:
            content = contentfile.read()
            for subtemplatename in find_referenced_templates(self.jinjaenv.parse(content)):
                if subtemplatename not in skip:
                    yield from self._iter_template_content(
                        subtemplatename,
                        skip=skip + [templatename],
                        )
            yield template.name, content

    def render_tex(self, output, context):
        '''Render a template into a .tex file

        Arguments:
        - output: a file object to write the result
        - context: a dict of all the data to populate the template
        '''

        output.write(self.template.render(context))


def _transform_options(config, equivalents):
    """
    Get the equivalent name of the checked options
    """
    for option in config:
        if config[option] and option in equivalents:
            yield equivalents[option]

def iter_bookoptions(config):
    """
    Extract the bookoptions from the config structure
    """
    if config['chords']['show']:
        yield 'chorded'
    else:
        yield 'lyrics'

    book_equivalents = {
        'pictures':         'pictures',
        'onesongperpage':   'onesongperpage',
    }
    yield from _transform_options(config['book'], book_equivalents)

    chords_equivalents = {
        'lilypond':     'lilypond',
        'tablatures':   'tabs',
        'repeatchords': 'repeatchords',
    }
    yield from _transform_options(config['chords'], chords_equivalents)

    if config['chords']['show']:
        if config['chords']['diagramreminder'] == "important":
            yield 'importantdiagramonly'
        elif config['chords']['diagramreminder'] == "all":
            yield 'diagram'

        yield config['chords']['instrument']
