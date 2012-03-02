\include "header"
\paper{
  paper-height = 2.4\cm
  paper-width  = 7.1\cm
}

<<
  \new RhythmicStaff {
    \new Voice = "myRhythm" {
      \numericTimeSignature
      \time 4/4
      a8^"Rythm verse" a~ a16 a a a a8 a~ a16 a a a
      a8^"Rythm chorus" a16 a \override NoteHead #'style = #'cross a8. \revert NoteHead #'style a16  a8 a16 a \override NoteHead #'style = #'cross a8. \revert NoteHead #'style a16
      a4.^"Rythm bridge" a8~ a2
      
    }
  }
>>