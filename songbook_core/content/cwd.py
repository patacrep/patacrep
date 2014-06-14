#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Change base directory before importing songs."""

import os

from songbook_core.content import process_content

#pylint: disable=unused-argument
def parse(keyword, config, argument, contentlist):
    """Return a list songs included in contentlist, whith a different base path.

    Arguments:
    - keyword: unused;
    - config: the current songbook configuration dictionary;
    - argument: a directory;
    - contentlist: songbook content, that is parsed by
      songbook_core.content.process_content().

    This function adds 'argument' to the directories where songs are searched
    for, and then processes the content.

    The 'argument' is added:
    - first as a relative path to the current directory;
    - then as a relative path to every path already present in
      config['songdir'].
    """
    config['_songdir'] = (
            [os.path.relpath(argument)] +
            [os.path.join(path, argument) for path in config['_songdir']] +
            config['_songdir']
            )
    return process_content(contentlist, config)

CONTENT_PLUGINS = {'cwd': parse}
