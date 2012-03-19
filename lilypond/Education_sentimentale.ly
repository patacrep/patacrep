\include "header"
\paper{paper-height = 2.5\cm}

\new \songbookstaff
{
  \key c \major
  \time 3/4
  \relative c''{
    e8 f e d c b a gis a b c a d e f e 
    <<
      {d4 r2. } \\
      {r8 g,8 f'  e d4 g,4}
    >>
    <<
      {e'8 f e d c b a g a b c a d c b4. c8 c2.} \\
      {g'8 a g f e d c b c d e c f e d4. c8 c2.}
    >>
  }
}

