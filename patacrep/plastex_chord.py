# -*- coding: utf-8 -*-

r"""PlasTeX module to deal with chords commands of the songs LaTeX package

Chords are set using commands like \[C]. This package parses those commands.
"""

import logging

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



class Chord(Command):
    """Beginning of a chord notation"""
    macroName = 'chord'
    macroMode = Command.MODE_NONE

    def __init__(self, *args, **kwargs):
        super(Chord, self).__init__(*args, **kwargs)
        self.chord = ""

    @property
    def source(self):
        """Return chord LaTeX code."""
        return r'\[{}]'.format(self.chord)

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

            for token in tex:
                if token.nodeType == token.TEXT_NODE and token.nodeValue == ']':
                    break
                else:
                    if token.nodeName == '#text':
                        chord.chord += str(token)
                    elif token.nodeName == "active::&":
                        chord.chord += '&'
                    else:
                        LOGGER.warning((
                            "{}: Unexpected character '{}' in chord "
                            "argument. Continuing anyway.").format(
                                tex.filename,
                                token.source,
                                ))
                        break

            return [chord]
        else:
            return super(BeginChordOrDisplayMath, self).invoke(tex)
