# patacrep 4.0.0

* Project gestion
  * Name change [#39](http://github.com/patacrep/patacrep/issues/39
  * Renew of the developement team
  * Separation engine/data
    * The engine is the [current poject](http://github.com/patacrep/patacrep)
    * Data have their [own project](http://github.com/patacrep/patadata)
    * And so does [various tools](http://github.com/patacrep/pataextra)

* Internal changes
  * Complete migration to Python
    * No more Makefiles
    * Creation of a `songbook` command
    * patacrep uses Python3 [#65](http://github.com/patacrep/patacrep/issues/65)
  * Massive code refactoring and simplification
  * [PEP8](http://legacy.python.org/dev/peps/pep-0008/) conformity
  * Better LaTeX Packages
  * Better langages handling
  * Better errors handling
  * Better code documentation (in comments)
  * Caching song AST, which gave an improvement of 45s for the compilation of all patadata [#51](http://github.com/patacrep/patacrep/issues/51)
  * Lot of small improvements

* Installation
  * All from PyPi ! You can now use pip to install/update/remove patacrep

* Fonctionnalities
  * Change the template engine [#9](http://github.com/patacrep/patacrep/issues/9)
  * Ability to add user variables [#18](http://github.com/patacrep/patacrep/issues/18)
  * Change the song inclusion syntaxe [#47](http://github.com/patacrep/patacrep/issues/47)
    * It is now possible to include other things than songs
    * You can write a plugins to include your own type of content
  * Personalisaitons of the songbook is easier with patadata templates (font, paper, colors, column, ...) [#41](http://github.com/patacrep/patacrep/issues/41)
  * You can change the number of columns [#41](http://github.com/patacrep/patacrep/issues/41)
  * Lilypond
    * On the fly lylipond files compilation
    * Adapt partition size to the paper size [#19](http://github.com/patacrep/patacrep/issues/19)
  * You can choos how to sort the songs [#36](http://github.com/patacrep/patacrep/issues/36)
  * Easier song repertories management [#43](http://github.com/patacrep/patacrep/issues/43) and  [#45](http://github.com/patacrep/patacrep/issues/45)
    * You can have more than one data folder
  * Better index customisation
  * Better gestion of files encoding [#62](http://github.com/patacrep/patacrep/issues/62).


# songbook 3.7.2

  (Louis) Undocumented bug corrections and improvements.

# songbook 3.4.7 to 3.7.1

  Mainly new songs in the data (which was included in songbook at this
  time), and a few undocumented bug corrections and improvements.

# songbook (v0.8)

  Undocumented.

# songbook (v0.7)

  (lohrun) New songbook format (not compatible with older version).
    Changes have been made to the compilation toolchain that prevent
    compilation of old format songbook.
  (lohrun) Use LaTeX Songs package v2.10.

 -- Alexandre Dupas <alexandre.dupas@gmail.com> Sat, 17 Jul 2010 15:24:14 +0200

# songbook (v0.6)

  (crep, lohrun) Corrections of mistakes and typos.
  (lohrun) Use plain songs package v2.9
  (lohrun) Replace makeindex script with a new python version
  (lohrun) Add script to produce the list of chords used in songs
  (crep, lohrun) Correct chords and gtabs used in songs
  (lohrun) Modification of the default geometry
  (lohrun) Remove capos from the lyricbook

 -- Alexandre Dupas <alexandre.dupas@gmail.com> Fri, 11 Dec 2009 15:35:03 +0100

# songbook (0.5)

  (crep, lohrun) Corrections of mistakes and typos.
  (lohrun) Add a proper volume mechanism
  (lohrun) Add volume-1 source containing about 165 songs
  (crep) Add naheulbeuk special edition
  (lohrun) Upgraded songs.sty with bits from songs package v2.9
  (lohrun) Add tabs option
  (crep,lohrun) Add lilypond option

 -- Alexandre Dupas <alexandre.dupas@gmail.com> Tue, 18 Aug 2009 23:38:12 +0200

# songbook (0.4)

  (crep, lohrun) Corrections of mistakes and typos.
  (crep, lohrun) Add cover picture to each song
  (lohrun) Update to the Songs Package v2.8
  (lohrun) Update makefile to be POSIX compilant

 -- Alexandre Dupas <alexandre.dupas@gmail.com> Sun, 31 May 2009 01:39:16 +0200

# songbook (0.3)

  (crep) Corrections of a lot of mistakes.
  (crep) Include image support.
  (lohrun) Add make-html utility.

 -- Alexandre Dupas <alexandre.dupas@gmail.com> Sun, 15 Feb 2009 18:34:59 +0100

# songbook (0.2)

  Initial version.

 -- Alexandre Dupas <alexandre.dupas@gmail.com> Sat, 11 Oct 2008 20:00:00 +0100
