\include "header"
\paper{
  paper-height = 3.1\cm
  paper-width= 7.1\cm
}

symbols = {
 
  d8 a d' fis' d' a d a d' fis' d' a
  g, g d' g' d' g g, g d' fis, g d'
  e, b, e e' b g e, b, e e' b g
  a, e a e' b g a, e a a, g, fis,
}
  
\score {
 
  <<
 
    %\new Staff { \clef "G_8" \symbols }
   \chords {d1. g e:m a }
   \new TabStaff   { 
      \numericTimeSignature
      \time 12/8    
      \symbols }
    
  >>
}

