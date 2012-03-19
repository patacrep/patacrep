\include "header"
\paper{
  paper-height = 1.4\cm
  paper-width= 4.0\cm
  line-width= 3.7\cm
}

symbols = {
  \numericTimeSignature
  \time 4/4 
  \autoBeamOff
  \partial 4. e,8    
  g,[ gis,] | 
  \autoBeamOn a,4 
  \autoBeamOff
  \repeat percent 3 {  <a,e a c' e'>8[ <a,e a c' e'>]}
}

\score {
  <<
    \new Staff { \clef "G_8" \symbols }
    % \new TabStaff   { \symbols }
  >>
}
