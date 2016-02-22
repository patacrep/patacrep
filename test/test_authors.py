"""Tests of author parsing."""

# pylint: disable=too-few-public-methods

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
    ("The mamas and the papas", ("mamas and the papas", "The")), # Unbreakable spaces
    (r"\LaTeX command", ("command", r"\LaTeX")), # LaTeX commands are ignored
    (r"\emph{Some braces}", ("braces}", r"\emph{Some")), # LaTeX commands are ignored
    (r"The Rolling\ Stones", ("Rolling~Stones", 'The')), # Escaped spaces are converted
    ]

PROCESS_AUTHORS_DATA = [
    (
        (
            "Lyrics by William Blake (from Milton, 1808), music by Hubert "
            "Parry (1916), and sung by The Royal~Choir~of~FooBar (just here to "
            "show you how processing is done)"
            ),
        [
            ("Blake", "William"),
            ("Parry", "Hubert"),
            ("Royal~Choir~of~FooBar", "The"),
        ]
    ),
    (
        "Anonyme (1967)",
        [],
    ),
    (
        "Lucky Luke et Jolly Jumper",
        [
            ("Luke", "Lucky"),
            ("Jumper", "Jolly"),
        ],
    ),
]

AUTHWORDS = authors.compile_authwords({
    "after": ["by"],
    "ignore": ["anonymous", "Anonyme", "anonyme"],
    "separators": ['and', 'et'],
    })

class TestAutors(unittest.TestCase):
    """Test of author parsing."""

    def test_split_author_names(self):
        """Test of :func:`patacrep.authors.split_author_names` function."""
        for argument, expected in SPLIT_AUTHORS_DATA:
            with self.subTest(argument=argument, expected=expected):
                self.assertEqual(authors.split_author_names(argument), expected)

    def test_processauthors(self):
        """Test of :func:`patacrep.authors.processauthors` function."""
        for argument, expected in PROCESS_AUTHORS_DATA:
            with self.subTest(argument=argument, expected=expected):
                self.assertEqual(
                    set(
                        authors.processauthors(argument, **AUTHWORDS)
                    ),
                    set(expected)
                    )
