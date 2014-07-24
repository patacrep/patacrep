# -*- coding: utf-8 -*-

r"""PlasTeX module to deal with chords commands of the songs LaTeX package

Chords are set using commands like \[C]. This package parses those commands.
"""

import logging

import plasTeX
from plasTeX import Command, Environment, Macro
from plasTeX.Base.LaTeX.Math import BeginDisplayMath

LOGGER = logging.getLogger(__name__)

# Count the number of levels of 'verse' environment: IN_VERSE==1 means that we
# are in a 'verse' environment; IN_VERSE==2 means that we are in two included
# 'verse' environment, and so on.
IN_VERSE = 0

def wrap_displaymath(cls):
    """Decorator to store the depth of 'verse' environment

    In the invoke() method classes, global variable IN_VERSE indicates the
    number of 'verse' (or 'chorus' or 'verse*') environment we are in.
    """

    # pylint: disable=no-init,too-few-public-methods
    class WrappedClass(cls):
        """Wrapper to LaTeX environment updating IN_VERSE"""
        blockType = True
        # pylint: disable=super-on-old-class,global-statement,no-member
        def invoke(self, tex):
            """Wrapper to invoke() to update global variable IN_VERSE."""
            global IN_VERSE
            if self.macroMode == Macro.MODE_BEGIN:
                self.ownerDocument.context.push()
                self.ownerDocument.context.catcode("\n", 13)
                IN_VERSE += 1
            else:
                self.ownerDocument.context.pop()
                IN_VERSE -= 1
            super(WrappedClass, self).invoke(tex)
    return WrappedClass

# pylint: disable=too-many-public-methods
@wrap_displaymath
class Verse(Environment):
    """LaTeX 'verse' environment"""
    macroName = 'verse'

# pylint: disable=too-many-public-methods
@wrap_displaymath
class VerseStar(Environment):
    """LaTeX 'verse*' environment"""
    macroName = 'verse*'

# pylint: disable=too-many-public-methods
@wrap_displaymath
class Chorus(Environment):
    """LaTeX 'chorus' environment"""
    macroName = 'chorus'

def match_space(token):
    """Return True if token is a space or newline character."""
    return (
            isinstance(token, plasTeX.Tokenizer.Space)
            or token.nodeName == 'active::\n'
            )

def match_closing_square_bracket(token):
    """Return True if token is character ']'."""
    return token.nodeType == token.TEXT_NODE and token.nodeValue == ']'

def match_egroup(token):
    """Return True if token is of type `egroup` (end of group)."""
    return isinstance(token, plasTeX.Base.Text.egroup) #pylint: disable=no-member

def match_space_or_chord(token):
    """Return True if token is a space or a chord."""
    return match_space(token) or isinstance(token, Chord)

def parse_until(tex, end=lambda x: False):
    """Parse `tex` until condition `end`, or `egroup` is met.

    Arguments:
    - tex: object to parse
    - end: function taking a token in argument, and returning a boolean.
      Parsing stops when this function returns True, or an `egroup` is met.

    Return: a tuple of two items (the list of parsed tokens, last token). This
    is done so that caller can decide whether they want to discard it or not.
    Last token can be None if everything has been parsed without the end
    condition being met.
    """
    parsed = []
    last = None
    for token in tex:
        if end(token) or match_egroup(token):
            last = token
            break
        elif isinstance(token, plasTeX.Base.Text.bgroup): #pylint: disable=no-member
            # pylint: disable=expression-not-assigned
            [token.appendChild(item) for item in parse_until(tex, match_egroup)]
        parsed.append(token)
    return (parsed, last)


class Chord(Command):
    """Beginning of a chord notation"""
    macroName = 'chord'
    macroMode = Command.MODE_NONE

class BeginChordOrDisplayMath(BeginDisplayMath):
    r"""Wrapper to BeginDisplayMath

    In a 'verse' (or 'verse*' or 'chorus') environment, the '\[' macro
    displays a chord. Otherwise, it corresponds to the usual LaTeX math mode.
    This class calls the right method, depending on the inclusion of this
    macro in a verse environment.
    """
    macroName = '['

    def invoke(self, tex):
        """Process this macro"""
        if IN_VERSE:
            chord = Chord()

            self.ownerDocument.context.push() #pylint: disable=no-member
            self.ownerDocument.context.catcode("&", 13) #pylint: disable=no-member
            chord.setAttribute(
                    'name',
                    parse_until(tex, match_closing_square_bracket)[0],
                    )
            self.ownerDocument.context.pop() #pylint: disable=no-member

            token = next(iter(tex), None)
            if token is None:
                return [chord]
            elif match_space(token):
                chord.appendChild(token)
                return [chord]
            elif (
                    isinstance(token, Verse)
                    or isinstance(token, VerseStar)
                    or isinstance(token, Chorus)
                    ):
                LOGGER.warning((
                    "{} L{}: '\\end{{verse}}' (or 'verse*' or 'chorus') not "
                    "allowed directly after '\\['."
                    ).format(tex.filename, tex.lineNumber)
                    )
                return [chord]
            elif isinstance(token, Chord):
                token.attributes['name'] = (
                        chord.attributes['name']
                        + token.attributes['name']
                        )
                chord = token
                return [chord]
            elif isinstance(token, plasTeX.Base.Text.bgroup): #pylint: disable=no-member
                # pylint: disable=expression-not-assigned
                [chord.appendChild(item) for item in parse_until(tex)[0]]
                return [chord]
            else:
                chord.appendChild(token)
                (parsed, last) = parse_until(tex, match_space_or_chord)
                # pylint: disable=expression-not-assigned
                [chord.appendChild(item) for item in parsed]
                if isinstance(last, Chord):
                    return [chord, last]
                else:
                    chord.appendChild(last)
                    return [chord]
        else:
            return super(BeginChordOrDisplayMath, self).invoke(tex)

