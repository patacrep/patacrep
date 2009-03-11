# Copyright (c) 2008 Alexandre Dupas <alexandre.dupas@gmail.com>
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2, or (at your option) any later
# version.
# 
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#

SRC := $(wildcard *.tex)

SOURCES := $(shell egrep -l '^[^%]*\\begin\{document\}' *.tex)

CIBLE = $(SOURCES:%.tex=%)

PDF = $(CIBLE:%=%.pdf)
PSF = $(CIBLE:%=%.ps.gz)

SONGS = songs.sbd
SONGS_SRC = $(shell ls songs/*/*.sg)

MAKE_INDEX=./make-index

ifeq ($(shell which ikiwiki),)
IKIWIKI=echo "** ikiwiki not found" >&2 ; echo ikiwiki
else
IKIWIKI=ikiwiki
endif

# Get dependencies (that can also have dependencies)
define get_dependencies
	deps=`perl -ne '($$_)=/^[^%]*\\\(?:include|input)\{(.*?)\}/;@_=split /,/; foreach $$t (@_) { print "$$t "}' $<`
endef

# Get inclusion only files (that can not have dependencies)
define get_inclusions
	incl=`perl -ne '($$_)=/^[^%]*\\\(?:newauthorindex|newindex)\{.*\}\{(.*?)\}/;@_=split /,/; foreach $$t (@_) { print "$$t.sbx "}' $<`
endef

define get_prereq
	prep=`perl -ne '($$_)=/^[^%]*\\\(?:newauthorindex|newindex)\{.*\}\{(.*?)\}/;@_=split /,/; foreach $$t (@_) { print "$$t.sxd "}' $<`
endef

############################################################
### Cibles

default: pdf

ps: LATEX = latex
ps: $(PSF)
	gv $<

pdf: LATEX = pdflatex
pdf: $(PDF)
	xpdf $<

clean: cleandoc
	@rm -f $(SRC:%.tex=%.d)
	@rm -f $(CIBLE:%=%.aux) 
	@rm -f $(CIBLE:%=%.toc)
	@rm -f $(CIBLE:%=%.out) $(CIBLE:%=%.log) $(CIBLE:%=%.nav) $(CIBLE:%=%.snm)
	@rm -f $(CIBLE:%=%.dvi)
	@rm -f $(SONGS)
	@rm -f *.sbx *.sxd

cleanall: clean
	@rm -f $(PDF) $(PSF)

depend:

documentation:
	$(IKIWIKI) doc html -v --wikiname "Songbook Documentation" --plugin=goodstuff --set usedirs=0

cleandoc:
	@rm -rf "doc/.ikiwiki" html

############################################################

$(PSF): LATEX = latex
$(PSF): %.ps.gz: %.ps
	gzip -f $<

%.ps: %.dvi
	dvips -o $@ $<

%.dvi: %.tex %.aux
	$(LATEX) $<

$(PDF): LATEX = pdflatex
$(PDF): %.pdf: %.tex %.aux
	$(LATEX) $< 

%.aux: %.tex
	$(LATEX) $< 

%.sbx: %.sxd
	$(MAKE_INDEX) $< > $@

%.d: %.tex
	@$(get_dependencies) ; echo $< $@: $$deps > $@
	@$(get_inclusions) ; echo $(patsubst %.tex,%.pdf,$<) : $$incl >> $@ ; 
	@$(get_prereq) ; echo $$prep : $(patsubst %.tex,%.aux,$<) >> $@

include $(SOURCES:%.tex=%.d)

# songbook related rules
# that is not all but no other rules are easy to move around
%.aux: $(SONGS)

$(SONGS): $(SONGS_SRC)
	@cat $(SONGS_SRC) > $@


