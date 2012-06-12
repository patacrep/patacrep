\include "header"
\paper{
  paper-height = 1.1\cm
  paper-width  = 5.2\cm
}

<<
   \chords { d1:m | f2 g2 }
  \new RhythmicStaff {
    \new Voice = "myRhythm" {
      \numericTimeSignature
      \time 4/4
      a4 a8 a~ a a a a 
      a4 a a a     
    }
  }
>>