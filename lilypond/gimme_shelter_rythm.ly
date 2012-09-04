\include "header"
\paper{
  paper-height = 0.6\cm
  paper-width  = 4.5\cm
}

<<
  \new RhythmicStaff {
    \new Voice = "myRhythm" {
      \numericTimeSignature
      \time 4/4
      a4^"" a a8 a a a~ a a a a a a a a
      
      
    }
  }
>>