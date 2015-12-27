"""Template for .tex generation settings and utilities"""

import re
import json

from jinja2 import Environment, FileSystemLoader, ChoiceLoader, \
        TemplateNotFound, nodes
from jinja2.ext import Extension
from jinja2.meta import find_referenced_templates as find_templates

from patacrep import errors, files
from patacrep.latex import lang2babel
import patacrep.encoding

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


def _escape_tex(value):
    '''Escape TeX special characters'''
    newval = value
    for pattern, replacement in _LATEX_SUBS:
        newval = pattern.sub(replacement, newval)
    return newval


class Renderer:
    """Render a template to a LaTeX file."""
    # pylint: disable=too-few-public-methods

    def __init__(self, template, jinjaenv, encoding=None):
        self.encoding = encoding
        self.jinjaenv = jinjaenv
        self.jinjaenv.block_start_string = '(*'
        self.jinjaenv.block_end_string = '*)'
        self.jinjaenv.variable_start_string = '(('
        self.jinjaenv.variable_end_string = '))'
        self.jinjaenv.comment_start_string = '(% comment %)'
        self.jinjaenv.comment_end_string = '(% endcomment %)'
        self.jinjaenv.line_comment_prefix = '%!'
        self.jinjaenv.filters['escape_tex'] = _escape_tex
        self.jinjaenv.trim_blocks = True
        self.jinjaenv.lstrip_blocks = True
        self._fill_filters()
        self.template = self.jinjaenv.get_template(template)

    def _fill_filters(self):
        """Define some jinja2 filters, if not set yet."""
        for key, value in [
                ("path2posix", files.path2posix),
                ("iter_datadirs", files.iter_datadirs),
                ("lang2babel", lang2babel),
            ]:
            if key not in self.jinjaenv.filters:
                self.jinjaenv.filters[key] = value


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

    def get_variables(self):
        '''Get and return a dictionary with the default values
         for all the variables
        '''
        data = self.get_template_variables(self.template)
        variables = dict()
        for name, param in data.items():
            variables[name] = self._get_default(param)
        return variables

    def _get_default(self, parameter):
        '''Get the default value for the parameter, according to the language.
        '''
        default = None
        try:
            default = parameter['default']
        except KeyError:
            return None

        if self.lang in default:
            variable = default[self.lang]
        elif "default" in default:
            variable = default["default"]
        elif "en" in default:
            variable = default["en"]
        elif len(default):
            variable = default.popitem()[1]
        else:
            variable = None

        return variable

    def get_template_variables(self, template, skip=None):
        """Parse the template to extract the variables as a dictionary.

        If the template includes or extends other templates, load them as well.

        Arguments:
        - template: the name of the template, as a string.
        - skip: a list of templates (as strings) to skip: if they are included
          in 'template' (or one of its subtemplates), it is not parsed.
        """
        if not skip:
            skip = []
        variables = {}
        (current, templates) = self.parse_template(template)
        for subtemplate in templates:
            if subtemplate in skip:
                continue
            variables.update(
                self.get_template_variables(
                    subtemplate,
                    skip + templates
                    )
                )
        variables.update(current)
        return variables

    def parse_template(self, template):
        """Return (variables, templates).

        Argument:
        - template: name of the template to parse.

        Return values:
        - variables: a dictionary of variables contained in 'template', NOT
          recursively (included templates are not parsed).
        - templates: list of included temlates, NOT recursively.
        """

        subvariables = {}
        templatename = self.jinjaenv.get_template(template).filename
        with patacrep.encoding.open_read(
            templatename,
            encoding=self.encoding
            ) as template_file:
            content = template_file.read()
        subtemplates = list(find_templates(self.jinjaenv.parse(content)))
        match = re.findall(_VARIABLE_REGEXP, content)
        if match:
            for var in match:
                try:
                    subvariables.update(json.loads(var))
                except ValueError as exception:
                    raise errors.TemplateError(
                        exception,
                        (
                            "Error while parsing json in file "
                            "{filename}. The json string was:"
                            "\n'''\n{jsonstring}\n'''"
                        ).format(
                            filename=templatename,
                            jsonstring=var,
                            )
                        )

        return (subvariables, subtemplates)

    def render_tex(self, output, context):
        '''Render a template into a .tex file

        Arguments:
        - output: a file object to write the result
        - context: a dict of all the data to populate the template
        '''

        output.write(self.template.render(context))
