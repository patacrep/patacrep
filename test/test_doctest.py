#!/usr/bin python

# Copyright 2015 Louis Paternault
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Tests"""

import doctest

import patacrep
from patacrep import files

def load_tests(__loader, tests, __pattern):
    """Load tests (doctests).
    """
    # Loading doctests
    tests.addTests(doctest.DocTestSuite(patacrep))
    for module in files.iter_modules(patacrep.__path__, "{}.".format(patacrep.__name__)):
        try:
            tests.addTests(doctest.DocTestSuite(module))
        except ValueError:
            # No docstring, or no doctests in the docstrings
            continue

    return tests
