# -*- coding: utf-8 -*-

"""Quick management of random LaTeX commands."""

from plasTeX import Command

# pylint: disable=invalid-name,too-many-public-methods
class songcolumns(Command):
    r"""Manage `\songcolumns` command"""
    args = '{num:int}'

# pylint: disable=invalid-name,too-many-public-methods
class gtab(Command):
    r"""Manage `\gta` command"""
    args = '{chord:str}{diagram:str}'
