#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from songbook_core.content import process_content

def parse(keyword, config, argument, contentlist):
    config['_songdir'] = (
            [os.path.relpath(argument)] +
            [os.path.join(path, argument) for path in config['_songdir']] +
            config['_songdir']
            )
    return process_content(contentlist, config)

CONTENT_PLUGINS = {'cwd': parse}
