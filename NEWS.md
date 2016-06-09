# patacrep 5.0.0

* Songbook file
  * Default extension is now `.yaml`
  * Book options are now specified using the yaml markup
    * `cd` behavior changed [#207](https://github.com/patacrep/patacrep/pull/207)
    * `addsongdir` and `setcounter` created
    * `sorted` renamed to `sort`
  * The song counter is no more reset on `songsection` [#208](https://github.com/patacrep/patacrep/pull/208)
  * The names of notes can be explicitely defined (was limited to `solfedge` or `alphascale`) [#217](https://github.com/patacrep/patacrep/pull/217)

* Song files
  * New song format supported: Chordpro
  * Supported extensions [#174](http://github.com/patacrep/patacrep/pull/174)
    * .csg: Chordpro (recommmended)
    * .tsg: LaTeX song
    * .sg: LaTeX song (unfavored)
    * .tis: LaTeX intersong
  * `start_echo` is now supported in chordpro songs [#205](https://github.com/patacrep/patacrep/pull/205)
  * LaTeX songs
    * `cov` renamed to `cover`
    * `vcov` is deprecated
  * Image directive now accepts options to define its size [#218](https://github.com/patacrep/patacrep/pull/218)
  * Better handling of special characters [#213](https://github.com/patacrep/patacrep/pull/213)

* Add a compilation option `--error` [#195](https://github.com/patacrep/patacrep/pull/195)

* Template files also uses `yaml` markup

* Creation of a patatools utility [#189](https://github.com/patacrep/patacrep/pull/189)

* Datadir reorganisation [#211](https://github.com/patacrep/patacrep/pull/211)
  * songbook templates are now located in `songbook` subfolder of the `templates`
  * the LaTeX styles (previously in `/latex`) are now in `/templates/styles`

* Various fixes and improvements


# patacrep 4.0.0

* Project management
  * Change name [#39](http://github.com/patacrep/patacrep/issues/39)
  * Renew of the developement team
  * Separation of engine and data
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
  * Better error handling
  * Better code documentation (in comments)
  * Cache song AST, which gives an improvement of 45s for the compilation of all patadata [#51](http://github.com/patacrep/patacrep/issues/51)
  * Lot of small improvements

* Installation
  * All from PyPi ! Can now use pip to install/update/remove patacrep

* Features
  * Change the template engine [#9](http://github.com/patacrep/patacrep/issues/9)
  * Ability to add user variables [#18](http://github.com/patacrep/patacrep/issues/18)
  * Change the song inclusion syntax [#47](http://github.com/patacrep/patacrep/issues/47)
    * Now possible to include content that is not song (raw tex file, for instance)
    * Can write plugins to include custom type of content
  * Songbook customization made easy with patadata templates (font, paper, colors, column, ...) [#41](http://github.com/patacrep/patacrep/issues/41)
  * Can change columns number [#41](http://github.com/patacrep/patacrep/issues/41)
  * Lilypond
    * On the fly lylipond files compilation
    * Adapt partition size to the paper size [#19](http://github.com/patacrep/patacrep/issues/19)
  * Can choose song ordering [#36](http://github.com/patacrep/patacrep/issues/36)
  * Easier song repertories management [#43](http://github.com/patacrep/patacrep/issues/43) and  [#45](http://github.com/patacrep/patacrep/issues/45)
    * Can have more than one data folder
  * Better index customization
  * Better file encoding management [#62](http://github.com/patacrep/patacrep/issues/62).


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
