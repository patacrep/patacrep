# -*- coding: utf-8 -*-
"""Abstract Syntax Tree for ChordPro code."""

class AST:
    """Base class for the tree."""
    # pylint: disable=no-init
    metadata = None

    @classmethod
    def init_metadata(cls):
        """Clear metadata

        As this attribute is a class attribute, it as to be reset at each new
        parsing.
        """
        cls.metadata = {
                '@languages': set(),
                }

class Expression(AST):
    """ChordPro expression"""

    def __init__(self, value):
        super().__init__()
        self.content = [value]

    def prepend(self, value):
        """Add a value at the beginning of the content list."""
        if value is not None:
            self.content.insert(0, value)
        return self

    def __str__(self):
        return "".join([str(item) for item in self.content])

class SongPart(AST):
    """ChordPro start_of/end_of command

    {start_of_chorus}, {end_of_tab}, {eov} ...
    """

    class Type:
        CHORUS = ("chorus",
                  "start_of_chorus", "end_of_chorus",
                  "soc", "eoc")
        VERSE = ("verse",
                 "start_of_verse", "end_of_verse",
                 "sov", "eov")
        BRIDGE = ("bridge",
                  "start_of_bridge", "end_of_bridge",
                  "sob", "eob")
        TAB = ("tab",
               "start_of_tab", "end_of_tab",
               "sot", "eot")

    def __init__(self, name):
        if "_" in name:
            self.init_long_form(name)
        else:
            self.init_short_form(name)

    def __str__(self):
        return self.name

    def init_short_form(self, name):
        self.type = ""

    def init_long_form(self, name):
        self.type = ""


