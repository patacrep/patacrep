\include "header"
\paper{paper-height = 1.4\cm}

\new \songbookstaff
{
  \key d \minor
  \time 4/4
  \relative c''
  {
    \repeat volta 2
    {
      d2~ d8 e4 f8 a1 
    }
    \alternative
    {
      {g2. f4 e2. f8 e} {g2. bes4 a1}
    }
  }
}
