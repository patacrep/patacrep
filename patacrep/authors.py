"""Authors string management."""

import logging
import re

LOGGER = logging.getLogger(__name__)

RE_AFTER = r"^.*\b{}\b(.*)$"
RE_SEPARATOR = r"^(.*)\b *{} *(\b.*)?$"

def compile_authwords(authwords):
    """Convert strings of authwords to compiled regular expressions.

    This regexp will later be used to match these words in authors strings.
    """
    return {
        'ignore': authwords.get('ignore', []),
        'after': [
            re.compile(RE_AFTER.format(word))
            for word in authwords.get('after', [])
            ],
        'separators': [
            re.compile(RE_SEPARATOR.format(word))
            for word in ([" %s" % word for word in authwords.get('separators', [])] + [',', ';'])
            ],
        }

def split_author_names(string):
    r"""Split author between first and last name.

    The last space separates first and last name.
    LaTeX commands are ignored, escaped spaces are converted to ~.

    >>> split_author_names("Edgar Allan Poe")
    ('Poe', 'Edgar Allan')
    >>> split_author_names("Edgar Allan \emph {Poe}")
    ('{Poe}', 'Edgar Allan \\emph')
    >>> split_author_names(r"The Rolling\ Stones")
    ('Rolling~Stones', 'The')
    >>> split_author_names("The {Rolling Stones}")
    ('Stones}', 'The {Rolling')
    >>> split_author_names("The Rolling Stones")
    ('Rolling\xa0Stones', 'The')
    >>> split_author_names("   John   Doe  ")
    ('Doe', 'John')
    """
    chunks = string.strip().replace("\\ ", "~")
    chunks = chunks.split(" ")
    return (chunks[-1].strip(), " ".join(chunks[:-1]).strip())


def split_sep_author(string, separators):
    """Split authors string according to separators.

    Arguments:
    - string: string containing authors names ;
    - separators: regexp matching a separator.

    >>> split_sep_author("Tintin and Milou", re.compile(RE_SEPARATOR.format("and")))
    ['Tintin', 'Milou']
    >>> split_sep_author("Tintin,", re.compile(RE_SEPARATOR.format(",")))
    ['Tintin']
    """
    authors = []
    match = separators.match(string)
    while match:
        if match.group(2) is not None:
            authors.append(match.group(2).strip())
        string = match.group(1)
        match = separators.match(string)
    authors.insert(0, string.strip())
    return authors

################################################################################
### Process authors tools.
################################################################################

def processauthors_removeparen(authors_string):
    """Remove parentheses

    See docstring of processauthors() for more information.

    >>> processauthors_removeparen("This (foo) string (bar) contains (baz) parenthesis")
    'This  string  contains  parenthesis'
    """
    opening = 0
    dest = ""
    for char in authors_string:
        if char == '(':
            opening += 1
        elif char == ')' and opening > 0:
            opening -= 1
        elif opening == 0:
            dest += char
    return dest

def processauthors_split_string(authors_string, separators):
    """Split strings

    See docstring of processauthors() for more information.

    >>> processauthors_split_string("Tintin and Milou", [re.compile(RE_SEPARATOR.format("and"))])
    ['Tintin', 'Milou']
    >>> processauthors_split_string("Tintin, Milou", [re.compile(RE_SEPARATOR.format(","))])
    ['Tintin', 'Milou']
    >>> processauthors_split_string(
    ...     "Tintin, and Milou",
    ...     [re.compile(RE_SEPARATOR.format(word)) for word in ['and', ',']]
    ... )
    ['Tintin', 'Milou']
    """
    authors_list = [authors_string]
    for sepword in separators:
        dest = []
        for author in authors_list:
            dest.extend(split_sep_author(author, sepword))
        authors_list = dest
    return authors_list

def processauthors_remove_after(authors_list, after):
    """Remove stuff before "after"

    See docstring of processauthors() for more information.
    """
    dest = []
    for author in authors_list:
        for afterword in after:
            match = afterword.match(author)
            if match:
                author = match.group(1)
                break
        dest.append(author)
    return dest

def processauthors_ignore_authors(authors_list, ignore):
    """Ignore ignored authors

    See docstring of processauthors() for more information.
    """
    dest = []
    for author in authors_list:
        ignored = False
        for ignoreword in ignore:
            if author.find(ignoreword) != -1:
                ignored = True
                break
        if not ignored:
            dest.append(author)
    return dest

def processauthors_clean_authors(authors_list):
    """Clean: remove empty authors and unnecessary spaces

    See docstring of processauthors() for more information.
    """
    return [
        author.lstrip()
        for author
        in authors_list
        if author.lstrip()
        ]

def processauthors(authors_string, after=None, ignore=None, separators=None):
    r"""Return an iterator of authors

    For example, in the following call:

    >>> set(processauthors(
    ...   (
    ...       "Lyrics by William Blake (from Milton, 1808), "
    ...       "music by Hubert Parry (1916), "
    ...       "and sung by The Royal~Choir~of~FooBar "
    ...       "(just here to show you how processing is done)"
    ...   ),
    ...   **compile_authwords({
    ...         'after': ["by"],
    ...         'ignore': ["anonymous"],
    ...         'separators': ["and", ","],
    ...         })
    ...   )) == {("Blake", "William"), ("Parry", "Hubert"), ("Royal~Choir~of~FooBar", "The")}
    True


    The "authors_string" is processed as:

    1) First, parenthesis (and its content) are removed.
    # "Lyrics by William Blake, music by Hubert Parry,
                and sung by The Royal~Choir~of~FooBar"

    2) String is split, separators being comma and words from "separators".
    # ["Lyrics by William Blake", "music by Hubert Parry",
                "sung by The Royal~Choir~of~FooBar"]

    3) Everything before words in "after" is removed.
    # ["William Blake", "Hubert Parry", "The Royal~Choir~of~FooBar"]

    4) Strings containing words of "ignore" are dropped.
    # ["William Blake", "Hubert Parry", The Royal~Choir~of~FooBar"]

    5) First and last names are splitted
    # [
    #   ("Blake", "William"),
    #   ("Parry", "Hubert"),
    #   ("Royal~Choir~of~FooBar", "The"),
    # ]
    """

    if not separators:
        separators = []
    if not after:
        after = []
    if not ignore:
        ignore = []

    for author in processauthors_clean_authors(
            processauthors_ignore_authors(
                processauthors_remove_after(
                    processauthors_split_string(
                        processauthors_removeparen(
                            authors_string
                            ),
                        separators),
                    after),
                ignore)
        ):
        yield split_author_names(author)

def process_listauthors(authors_list, after=None, ignore=None, separators=None):
    """Process a list of authors, and return the list of resulting authors."""
    authors = []
    for sublist in [
            processauthors(string, after, ignore, separators)
            for string in authors_list
        ]:
        authors.extend(sublist)
    return authors
