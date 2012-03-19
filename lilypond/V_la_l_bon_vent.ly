\include "header"
\paper{paper-height = 2.5\cm}

\new \songbookstaff
{
  \relative c'
  {
    \key a \minor
    \time 2/4
    \repeat volta 2
    {
      e8 a a4 e8 a16 a a4
      e8 a a8 a16 b 
    }
    \alternative
    {
     {c8 c b8 b } {c8 b a4} 
    }
    r8 e8 a c b a g b a e a c b a g b a
    e a c b a a g e2
  }
}
