#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Authors string management."""

import re

DEFAULT_AUTHWORDS = {
        "after": ["by"],
        "ignore": ["unknown"],
        "sep": ["and"],
        }

def compile_authwords(authwords):
    """Convert strings of authwords to compiled regular expressions.

    This regexp will later be used to match these words in authors strings.
    """
    # Fill missing values
    for (key, value) in DEFAULT_AUTHWORDS.items():
        if key not in authwords:
            authwords[key] = value

    # Compilation
    authwords['after'] = [
            re.compile(r"^.*%s\b(.*)" % word)
            for word in authwords['after']
            ]
    authwords['sep'] = [
            re.compile(r"^(.*)%s (.*)$" % word)
            for word in ([" %s" % word for word in authwords['sep']] + [','])
            ]

    return authwords


def split_author_names(string):
    r"""Split author between first and last name.

    The last space separates first and last name, but spaces following a
    backslash or a command are not separators.
    Examples:
    - Edgar Allan Poe => Poe, Edgar Allan
    - Edgar Allan \emph {Poe} => \emph {Poe}, Edgar Allan
    - The Rolling\ Stones => Rolling\ Stones, The
    - The {Rolling Stones} => {Rolling Stones}, The
    """
    ignore_space = False
    last_space = index = 0
    brace_count = 0
    for char in string:
        index += 1
        if brace_count == 0:
            if char == "\\":
                ignore_space = True
            elif not char.isalnum() and ignore_space:
                ignore_space = False
            elif char == " ":
                last_space = index
        if char == "}":
            brace_count += 1
        if char == "{":
            brace_count -= 1
    return string[:last_space], string[last_space:]


def split_sep_author(string, sep):
    """Split authors string according to separators.

    Arguments:
    - string: string containing authors names ;
    - sep: regexp matching a separator.

    >>> split_sep_author("Tintin and Milou", '^(.*) and (.*)$')
    ["Tintin", "Milou"]
    """
    authors = []
    match = sep.match(string)
    while match:
        authors.append(match.group(2))
        string = match.group(1)
        match = sep.match(string)
    authors.append(string)
    return authors

################################################################################
### Process authors tools.
################################################################################

def processauthors_removeparen(authors_string):
    """Remove parentheses

    See docstring of processauthors() for more information.
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

def processauthors_split_string(authors_string, sep):
    """Split strings

    See docstring of processauthors() for more information.
    """
    authors_list = [authors_string]
    for sepword in sep:
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
            if author.find(str(ignoreword)) != -1:
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

def processauthors_invert_names(authors_list):
    """Move first names after last names

    See docstring of processauthors() for more information.
    """
    dest = []
    for author in authors_list:
        first, last = split_author_names(author)
        if first:
            dest.append("%(last)s, %(first)s" % {
                'first': first.lstrip(),
                'last': last.lstrip(),
                })
        else:
            dest.append(last.lstrip())
    return dest

def processauthors(authors_string, after=None, ignore=None, sep=None):
    r"""Return a list of authors

    For example, we are processing:
    # processauthors(
    #   "Lyrics by William Blake (from Milton, 1808),
                    music by Hubert Parry (1916),
                    and sung by The Royal\ Choir~of~Nowhere
                    (just here to show you how processing is done)",
    #   after = ["by"],
    #   ignore = ["anonymous"],
    #   sep = [re.compile('^(.*) and (.*)$')],
    #   )


    The "authors_string" string is processed as:

    1) First, parenthesis (and its content) are removed.
    # "Lyrics by William Blake, music by Hubert Parry,
                and sung by The Royal\ Choir~of~Nowhere"

    2) String is split, separators being comma and words from "sep".
    # ["Lyrics by William Blake", "music by Hubert Parry",
                "sung by The Royal\ Choir~of~Nowhere"]

    3) Everything before words in "after" is removed.
    # ["William Blake", "Hubert Parry", "The Royal\ Choir~of~Nowhere"]

    4) Strings containing words of "ignore" are dropped.
    # ["William Blake", "Hubert Parry", The Royal\ Choir~of~Nowhere"]

    5) First names are moved after last names
    # ["Blake, William", "Parry, Hubert", Royal\ Choir~of~Nowhere, The"]
    """

    if not sep:
        sep = []
    if not after:
        after = []
    if not ignore:
        ignore = []

    return processauthors_invert_names(
            processauthors_clean_authors(
                processauthors_ignore_authors(
                    processauthors_remove_after(
                        processauthors_split_string(
                            processauthors_removeparen(
                                authors_string
                                ),
                            sep),
                        after),
                    ignore)
                )
            )

