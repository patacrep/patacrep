\include "header"
\paper{
  paper-height = 4\cm
  paper-width= 8\cm
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
  <dis\5 g\4 ais\3 dis'\2 g'\1>2
  <gis,\6 dis\5 gis\4 c'\3 dis'\2 gis'\1>2
  <ais,\6 d\5 f\4 ais\3 d'\2 ais'\1>2 
  d16\5 dis\5 f8\4 f16\4 g16\4 gis8\4
  
  <dis\5 g\4 ais\3 dis'\2 g'\1>2
  <gis,\6 dis\5 gis\4 c'\3 dis'\2 gis'\1>2
  <ais,\6 d\5 f\4 ais\3 d'\2 ais'\1>2 
   d8\5 dis\5 f\4 d8\5
  
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
