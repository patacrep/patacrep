\include "../_lilypond/header"
\paper{
  paper-height = 1\cm
  paper-width  = 6\cm
}

<<
  \new RhythmicStaff {
    \new Voice = "myRhythm" {
      \numericTimeSignature
      \time 4/4
      a4^"verse" a8-> a  a8 a a-> a
       a4^"chorus" a->  a8 a a-> a
      
    }
  }
>>
