#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Template for .tex generation settings and utilities"""

from jinja2 import Environment, FileSystemLoader, ChoiceLoader, PackageLoader
from jinja2.meta import find_referenced_templates as find_templates
import os
import re
import json
import locale

_LATEX_SUBS = (
    (re.compile(r'\\'), r'\\textbackslash'),
    (re.compile(r'([{}_#%&$])'), r'\\\1'),
    (re.compile(r'~'), r'\~{}'),
    (re.compile(r'\^'), r'\^{}'),
    (re.compile(r'"'), r"''"),
    (re.compile(r'\.\.\.+'), r'\\ldots'),
)


def _escape_tex(value):
    '''Escape TeX special characters'''
    newval = value
    for pattern, replacement in _LATEX_SUBS:
        newval = pattern.sub(replacement, newval)
    return newval


class TexRenderer(object):
    """Render a template to a LaTeX file."""

    def __init__(self, template, datadir=''):
        '''Start a new jinja2 environment for .tex creation.

        Arguments:
        - datadir: location of the user-defined templates
        '''
        self.texenv = Environment(
                loader=ChoiceLoader([
                    FileSystemLoader(
                        os.path.join(datadir, 'templates')
                        ),
                    PackageLoader(
                        'songbook_core', os.path.join('data', 'templates')
                        ),
                    ]),
                )
        self.texenv.block_start_string = '(*'
        self.texenv.block_end_string = '*)'
        self.texenv.variable_start_string = '(('
        self.texenv.variable_end_string = '))'
        self.texenv.comment_start_string = '(% variables %)'
        self.texenv.comment_end_string = '(% endvariables %)'
        self.texenv.line_comment_prefix = '(%%)'
        self.texenv.filters['escape_tex'] = _escape_tex
        self.texenv.trim_blocks = True
        self.texenv.lstrip_blocks = True

        # TODO: catch the TemplateNotFound
        self.template = self.texenv.get_template(template)

        # Trick to get the language code
        self.lang = locale.getdefaultlocale()[0].split('-')[0].split('_')[0]

    def get_variables(self):
        '''Get and return a dictionary with the default values
         for all the variables
        '''
        data = self.parse_templates()
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

    def parse_templates(self):
        '''Recursively parse all the used templates to extract all the
        variables as a dictionary.
        '''
        templates = self.get_templates(self.template)
        templates |= set([self.template.name])
        variables = {}
        regex = re.compile(r'\(% variables %\)\n(?P<variables>.*)'
                            '\(% endvariables %\)', re.DOTALL)
        for template_name in templates:
            filename = self.texenv.get_template(template_name).filename
            print filename
            with open(filename, 'r') as template_file:
                content = template_file.read()
            match = re.search(regex, content)
            if match:
                content = match.group('variables')
                variables.update(json.loads(content))
        return variables

    def get_templates(self, template):
        '''Recursively get a set of all the templates used
        by a particular template.
        '''
        with open(template.filename, 'r') as template_file:
            content = template_file.readlines()
        new_templates = list(find_templates(self.texenv.parse(content)))
        all_templates = set(new_templates)
        if len(new_templates) > 0:
            for new_template_name in new_templates:
                new_template = self.texenv.get_template(new_template_name)
                # union of the sets
                all_templates |= self.get_templates(new_template)
        return all_templates

    def render_tex(self, output, context):
        '''Render a template into a .tex file

        Arguments:
        - output: a file object to write the result
        - context: a dict of all the data to populate the template
        '''

        output.write(self.template.render(context))
