\include "header"
\paper
{
  paper-width = 15.5\cm
  line-width = 15\cm
  paper-height = 1.5\cm
}

\new \songbookstaff
{
  \key a \minor
  \time 2/4
  \partial 8 a'8
  \relative c''
  {
    b8 a4 g8 f4.\trill g8 
    <<
      {a8 g4 f8 e2}
      \\
      {f4 f' e2}
    >>
    r4 c16 b a e 
    c4. a8 g8 g'8~ g4~ g8 b4 a16 g 
    | f16 a c f a8 c8~ c8 d4 c8 | b4.\trill a8 | gis2 |
    r4 c,4 | d4. c8 | b16 a g4 a8 | e2 | 
  }
}

