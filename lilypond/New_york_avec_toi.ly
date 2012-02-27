\include "header"
\paper{
  paper-height = 1.1\cm
  paper-width= 5.2\cm
}

symbols = {
  \numericTimeSignature
  \time 4/4
  \repeat volta 2 {
  <a, e>8  <a, e> c cis <e a> <e a> <fis a> <e a>
  <fis, cis> <fis, cis> <fis, cis> <fis, cis> r2
}
}

\score {
  <<
    %\new Staff { \clef "G_8" \symbols }
    \new TabStaff   { \symbols }
  >>
}