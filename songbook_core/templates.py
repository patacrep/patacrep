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


def _init_tex_env(datadir=''):
    '''Start a new jinja2 environment for .tex creation'''
    loader = ChoiceLoader([
                    PackageLoader('songbook_core', 'data/templates'),
                    FileSystemLoader(os.path.join(datadir, 'templates')),
                           ])
    texenv = Environment(loader=loader)
    texenv.block_start_string = '(*'
    texenv.block_end_string = '*)'
    texenv.variable_start_string = '(('
    texenv.variable_end_string = '))'
    texenv.comment_start_string = '(% comment %)'
    texenv.comment_end_string = '(% endcomment %)'
    texenv.filters['escape_tex'] = _escape_tex
    texenv.trim_blocks = True
    texenv.lstrip_blocks = True
    return texenv


def render_tex(output, context, datadir=''):
    '''Render a template into a .tex file

    Arguments:
    - output: a file object to write the result
    - context: all the data to populate the template
    - datadir: location of the user-defined templates
    '''
    env = _init_tex_env(datadir=datadir)
    template = env.get_template(context['template'])

    content = template.render(**context)
    output.write(content)
    return None # TODO: gestion des erreurs
