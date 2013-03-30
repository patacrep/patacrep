# Copyright (c) 2008-2010 Alexandre Dupas <alexandre.dupas@gmail.com>
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

BOOKS_DIR=books/
SONGBOOKS := $(wildcard $(BOOKS_DIR)/*.sb)
TARGETS = $(SONGBOOKS:$(BOOKS_DIR)/%.sb=%)
LIBRARY=./

PDF = $(TARGETS:%=%.pdf)

#CHORDS = chords.tex
#CHORDS_SRC = $(shell ls $(LIBRARY)/songs/*/*.sg)

DATE = $(shell date +%d)-$(shell date +%m)-$(shell date +%Y)

PRINT=printf "%s\n"
PRINTTAB=printf "\t%s\n"

MAKE_SONGBOOK=./songbook.py
MAKE_INDEX=./songbook-makeindex.py
MAKE_CHORDS=./utils/songbook-gtab.py

ifeq ($(shell which lilypond),)
  LILYPOND=$(ECHO) "** lilypond not found" >&2 ; $(ECHO) lilypond
  LILYFILE=''
else
  LILYPOND=lilypond
  LILY_SRC:=$(wildcard $(LIBRARY)/lilypond/*.ly)
  LILYFILE=$(LILY_SRC:%.ly=%.pdf)
endif

LATEX=pdflatex $(LATEX_OPTIONS)
############################################################
### Targets

default: songbook.pdf

all: $(PDF)

pdf: $(PDF)
	xpdf $<

lilypond: $(LILYFILE)

clean:
	@rm -f $(TARGETS:%=%.d)   $(TARGETS:%=%.tex) $(TARGETS:%=%.aux) \
	       $(TARGETS:%=%.toc) $(TARGETS:%=%.out) $(TARGETS:%=%.log) \
	       $(TARGETS:%=%.nav) $(TARGETS:%=%.snm)
	@rm -f *.sbx *.sxd *.sxc
	@rm -f *.pyc

cleanall: clean
	@rm -f $(PDF)
	@rm -f $(LILYFILE)

depend:

############################################################


$(PDF): %.pdf: %.tex %.aux

%.aux: %.tex
	$(LATEX) $< 

%.sbx: %.sxd
	$(MAKE_INDEX) $< > $@

%.tex: $(BOOKS_DIR)/%.sb
	$(MAKE_SONGBOOK) --library=$(LIBRARY) -s $< -o $@

%.d: $(BOOKS_DIR)/%.sb
	$(MAKE_SONGBOOK) --library=$(LIBRARY) -s $< -d -o $@

%.pdf: %.ly
	@$(LILYPOND) --format=pdf -e '(define-public songbookstaff "$(SONGBOOKSTAFF)")' --output=$(@:%.pdf=%) $<

#$(CHORDS): $(CHORDS_SRC)
#	$(MAKE_CHORDS) -o $@

archive: cleanall
	tar -czvf songbook.tar.gz \
	--exclude-vcs \
	--exclude=$(BOOKS_DIR)/default.sb \
	--exclude=perso/* --exclude=perso \
	--exclude=build/* --exclude=build \
	--exclude=data/* --exclude=data \
	--exclude=*tar.gz \
	--transform 's/songbook/songbook-$(DATE)/1' \
	../songbook

ifeq (.pdf,$(suffix $(MAKECMDGOALS)))
include $(MAKECMDGOALS:%.pdf=%.d)
else ifneq ($(MAKECMDGOALS),clean)
  ifneq ($(MAKECMDGOALS),cleanall)
  include $(TARGETS:%=%.d)
  endif
endif
