\include "header"
\paper{
  paper-height = 0.9\cm
  line-width   = 2.7\cm
  paper-width  = 3.0\cm
}

<<
  \new RhythmicStaff {
    \new Voice = "myRhythm" {
      \numericTimeSignature
      \time 4/4
      \autoBeamOff
      a8[ a]
      \override NoteHead #'style = #'cross a[ \revert NoteHead #'style a]
      \override NoteHead #'style = #'cross a[ \revert NoteHead #'style a]
      \override NoteHead #'style = #'cross a[ \revert NoteHead #'style a]
    }
  }
>>