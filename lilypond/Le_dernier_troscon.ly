\include "header"
\paper{
  paper-height = 2 \cm
  paper-width= 6.7\cm
  line-width= 8\cm
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
  \repeat volta 4 {
  <d\5>4 f\5 e\5 g\4
  f\4 a\4 g\4 <f\4>8 e\4
  d4 f\4 e\4 g\4 
  f\4 e\4 d c\5 
}
}

\score {
  <<
   
    \new Staff 
    
    { 
       \override Staff.StringNumber #'transparent = 
##t 
      \clef "G_8" \symbols }
    %\chords { d2 c | f c | d c | f c }
   \new TabStaff   {
     \override Staff.Clef #'stencil = #(lambda (grob)
    (grob-interpret-markup grob TAB))
     \symbols }
  >>
}
