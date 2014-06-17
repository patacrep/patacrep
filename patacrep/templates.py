#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Template for .tex generation settings and utilities"""

from jinja2 import Environment, FileSystemLoader, ChoiceLoader, \
        TemplateNotFound, nodes
from jinja2.ext import Extension
from jinja2.meta import find_referenced_templates as find_templates
import codecs
import os
import re
import json

from patacrep import errors

_LATEX_SUBS = (
    (re.compile(r'\\'), r'\\textbackslash'),
    (re.compile(r'([{}_#%&$])'), r'\\\1'),
    (re.compile(r'~'), r'\~{}'),
    (re.compile(r'\^'), r'\^{}'),
    (re.compile(r'"'), r"''"),
    (re.compile(r'\.\.\.+'), r'\\ldots'),
)

_VARIABLE_REGEXP = re.compile(r"""
    \(\*\ *variables\ *\*\)    # Match (* variables *)
    (                          # Match and capture the following:
    (?:                        # Start of non-capturing group, used to match a single character
    (?!                        # only if it's impossible to match the following:
    \(\*\ *                    # - a literal (*
    (?:                        # Inner non-capturing group, used for the following alternation:
    variables                  # - Either match the word variables
    |                          # or
    endvariables               # - the word endvariables
    )                          # End of inner non-capturing group
    \ *\*\)                    # - a literal *)
    )                          # End of negative lookahead assertion
    .                          # Match any single character
    )*                         # Repeat as often as possible
    )                          # End of capturing group 1
    \(\*\ *endvariables\ *\*\) # until (* endvariables *) is matched.""",
    re.VERBOSE|re.DOTALL)


class VariablesExtension(Extension):
    """Extension to jinja2 to silently ignore variable block.
    Instead, they are parsed by this module.
    """
    tags = set(['variables'])

    def parse(self, parser):
        parser.stream.next()
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


class TexRenderer(object):
    """Render a template to a LaTeX file."""

    def __init__(self, template, datadirs, lang):
        '''Start a new jinja2 environment for .tex creation.

        Arguments:
        - template: name of the template to use.
        - datadirs: list of locations of the data directory
          (which may contain file <datadir>/templates/<template>).
        - lang: main language of songbook.
        '''
        self.lang = lang
        # Load templates in filesystem ...
        loaders = [FileSystemLoader(os.path.join(datadir, 'templates'))
                      for datadir in datadirs]
        self.texenv = Environment(
                loader=ChoiceLoader(loaders),
                extensions=[VariablesExtension],
                )
        self.texenv.block_start_string = '(*'
        self.texenv.block_end_string = '*)'
        self.texenv.variable_start_string = '(('
        self.texenv.variable_end_string = '))'
        self.texenv.comment_start_string = '(% comment %)'
        self.texenv.comment_end_string = '(% endcomment %)'
        self.texenv.line_comment_prefix = '%!'
        self.texenv.filters['escape_tex'] = _escape_tex
        self.texenv.trim_blocks = True
        self.texenv.lstrip_blocks = True

        try:
            self.template = self.texenv.get_template(template)
        except TemplateNotFound as exception:
            raise errors.TemplateError(
                    exception,
                    """Template "{template}" not found.""".format(
                        template=exception.name
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
        elif len(default > 0):
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
        templatename = self.texenv.get_template(template).filename
        with codecs.open(
                templatename,
                'r',
                'utf-8'
                ) as template_file:
            content = template_file.read()
            subtemplates = list(find_templates(self.texenv.parse(content)))
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
