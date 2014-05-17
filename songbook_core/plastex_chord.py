# -*- coding: utf-8 -*-

r"""PlasTeX module to deal with chords commands of the songs LaTeX package

Chords are set using commands like \[C]. This package parses those commands.
"""

from plasTeX import Command, Environment, Macro
from plasTeX.Base.LaTeX.Math import BeginDisplayMath

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
    class DisplayMath(cls):
        """Wrapper to LaTeX environment updating IN_VERSE"""
        blockType = True
        # pylint: disable=super-on-old-class,global-statement,no-member
        def invoke(self, tex):
            """Wrapper to invoke() to update global variable IN_VERSE."""
            global IN_VERSE
            if self.macroMode == Macro.MODE_BEGIN:
                IN_VERSE += 1
            else:
                IN_VERSE -= 1
            super(DisplayMath, self).invoke(tex)
    return DisplayMath

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



class BeginChord(Command):
    """Beginning of a chord notation"""
    macroName = 'chord'
    macroMode = Command.MODE_BEGIN

    @property
    def source(self):
        """Return chord LaTeX code."""
        return r'\[{}]'.format(''.join([str(item) for item in self.childNodes]))

class EndChord(Command):
    """End of a chord notation"""
    macroMode = Command.MODE_END

class BeginChordOrDisplayMath(BeginDisplayMath):
    r"""Wrapper to BeginDisplayMath

    In a 'verse' (or 'verse*' or 'chorus') environment, the '\[' macro
    displays a chord. Otherwise, it corresponds to the usual LaTeX math mode.
    This class calls the right method, depending on the inclusion of this
    macro in a verse environment.
    """
    macroName = '['

    def digest(self, tokens):
        """Consume the tokens corresponding to the arguments of this macro"""
        if IN_VERSE:
            for item in tokens:
                if item.nodeType == item.TEXT_NODE and item.nodeValue == ']':
                    break
                self.appendChild(item)
        else:
            return super(BeginChordOrDisplayMath, self).digest(tokens)

    def invoke(self, tex):
        """Process this macro"""
        if IN_VERSE:
            begin = BeginChord()
            self.ownerDocument.context.push(begin) # pylint: disable=no-member
            self.parse(tex)

            for token in tex:
                if token.nodeType == token.TEXT_NODE and token.nodeValue == ']':
                    break
                else:
                    begin.appendChild(token)

            end = EndChord()
            self.ownerDocument.context.push(end) # pylint: disable=no-member

            return [begin]
        else:
            return super(BeginChordOrDisplayMath, self).invoke(tex)
