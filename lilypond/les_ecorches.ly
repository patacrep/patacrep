\include "header"
\paper{
  paper-height = 2.5\cm
  paper-width= 7.2\cm
}

symbols = {
  \numericTimeSignature
  \time 12/8
  \repeat volta 4 {
  a,4  a,8 eis (e) e c (a,) a, g, (e,) e8
}
  \repeat volta 4 {
    g,4 g,8 eis (d) d c (b,) b, g,4 d8
  }
}

\score {
  <<
    \new Staff { \clef "G_8" \symbols }
    \new TabStaff   { \symbols }
  >>
}