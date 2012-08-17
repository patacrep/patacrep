\include "header"
\paper{
  paper-height = 3 \cm
  paper-width= 13.4\cm
  line-width= 13.2\cm
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
    <c\5>8 <e\4 g c'> g, <d\4 g b\2>
    <c\5>8 <e\4 g c'> g, <d\4 g b\2> }
  \alternative {
    { a,4 g,16 a, \bendAfter#1 c8 a,8 <e a c'>4. }
    { a,4 c16 a, \bendAfter#1 g,8 a,8 <e a c'>4. }
}
\repeat volta 2 {
    a,16^"riff" e a e  c8 a, c16 e a e c16 e a e }
}

\score {
  <<
   
    \new Staff 
    
    { 
       \override Staff.StringNumber #'transparent = 
##t 
      \clef "G_8" \symbols }
    \chords { c4 g c g | a1:m | a1:m | a2:m c4 g4 }
   \new TabStaff   {
     \override Staff.Clef #'stencil = #(lambda (grob)
    (grob-interpret-markup grob TAB))
     \symbols }
  >>
}
