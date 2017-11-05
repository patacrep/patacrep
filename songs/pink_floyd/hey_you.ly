\include "../_lilypond/header"
\paper{
  paper-height =2.5\cm
  paper-width= 10\cm
  line-width= 10\cm
}

TAB = \markup {
  \raise #1.5
  \sans
  \bold
  \huge
  \override #'(baseline-skip . 2.5)
  \left-align
  \center-column {
    T
    A
    B
  }
}

symbols = {
  \numericTimeSignature
  \time 4/4 
  \repeat volta 2 {
  <fis'\2>16 b\4 e'\3 g'\2 e'\3  b\4 g'\2 e'\3
  <fis'\2>16 b\4 e'\3 g'\2 e'\3  b\4 g'\2 e'\3
  e'\2 a\4 d'\3 a'\1 f'\2 d'\3 a'\1 d'\3
   e'\2 a\4 d'\3 a'\1 f'\2 d'\3 a'\1 d'\3
 }
}
\score {
  <<
   
    \new Staff 
    
    { 
       \override Staff.StringNumber #'transparent = 
##t 
      \clef "G_8" \symbols }
    %\chords { c2 | f2| g1 | c2 | f2| g1 }
   \new TabStaff   {
     \override Staff.Clef #'stencil = #(lambda (grob)
    (grob-interpret-markup grob TAB))
     \symbols }
  >>
}
