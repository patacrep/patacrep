#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Template for .tex generation settings and utilities"""

from jinja2 import Environment, FileSystemLoader, ChoiceLoader, PackageLoader
import os
import re

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
        self.template = template

        self.texenv = Environment(
                loader=ChoiceLoader([
                    FileSystemLoader(
                        os.path.join(datadir, 'templates')
                        ),
                    PackageLoader(
                        'songbook_core', os.path.join('data', 'templates')
                        ),
                    ])
                )
        self.texenv.block_start_string = '(*'
        self.texenv.block_end_string = '*)'
        self.texenv.variable_start_string = '(('
        self.texenv.variable_end_string = '))'
        self.texenv.comment_start_string = '(% comment %)'
        self.texenv.comment_end_string = '(% endcomment %)'
        self.texenv.filters['escape_tex'] = _escape_tex
        self.texenv.trim_blocks = True
        self.texenv.lstrip_blocks = True

    def file_template(self):
        """Return the filename of the selected template."""
        return self.texenv.get_template(self.template).filename

    def render_tex(self, output, context):
        '''Render a template into a .tex file

        Arguments:
        - output: a file object to write the result
        - context: all the data to populate the template
        '''

        #pylint: disable=star-args
        output.write(
                self.texenv.get_template(self.template).render(**context)
                )
