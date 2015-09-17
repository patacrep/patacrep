"""Tests of author parsing."""

# pylint: disable=too-few-public-methods

import re
import unittest

from patacrep import authors

SPLIT_AUTHORS_DATA = [
    ("Edgar Allan Poe", ("Poe", "Edgar Allan")),
    ("Richard M. Stallman", ("Stallman", "Richard M.")),
    ("Georges Brassens", ("Brassens", "Georges")),
    ("The Who", ("Who", "The")),
    ("Cher", ("Cher", "")),
    ("Red~Hot~Chili~Peppers", ("Red~Hot~Chili~Peppers", "")),
    ("The mamas~and~the~papas", ("mamas~and~the~papas", "The")),
    ("The mamas\ and\ the\ papas", ("mamas\ and\ the\ papas", "The")),
    ]

PROCESS_AUTHORS_DATA = [
        (
            "Lyrics by William Blake (from Milton, 1808), music by Hubert Parry (1916), and sung by The Royal\ Choir~of~FooBar (just here to show you how processing is done)",
            [
                ("Blake", "William"),
                ("Parry", "Hubert"),
                ("Royal\ Choir~of~FooBar", "The"),
                ]
            ),
        ]

class TestAutors(unittest.TestCase):
    """Test of author parsing."""

    def test_split_author_names(self):
        for argument, expected in SPLIT_AUTHORS_DATA:
            with self.subTest(argument=argument, expected=expected):
                self.assertEqual(authors.split_author_names(argument), expected)

    def test_processauthors(self):
        for argument, expected in PROCESS_AUTHORS_DATA:
            with self.subTest(argument=argument, expected=expected):
                self.assertEqual(
                    authors.processauthors(
                        argument,
                        **authors.compile_authwords({
                            "after": ["by"],
                            "ignore": ["anonymous"],
                            "sep": ['and'],
                            })
                    ),
                    expected
                    )
