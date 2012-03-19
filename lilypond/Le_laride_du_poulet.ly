\include "header"
\paper{paper-height = 2.4\cm}

\new \songbookstaff
{
  \key a \minor
  \time 2/4
  \relative c''
  {
    \partial 8 a8
    \repeat volta 2
    {
      a8 b c8. c16 b8 b a g a b c8. c16 b8 b a a
    }
    \repeat volta 2
    {
     a8 a e'8. d16 c8 d b a a a e'8. d16 c8 d b a
    }
  }
}

