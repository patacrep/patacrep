#!/usr/bin/env python
# -*- coding: utf-8 -*-

FILENAME = "naheulbeuk.tex"

import plasTeX
from plasTeX.TeX import TeX

doc = TeX(file = FILENAME).parse()

language_list = set()
for node in doc.allChildNodes:
    if node.nodeName == "selectlanguage":
        language_list.add(node.argSource)

print language_list
