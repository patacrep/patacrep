\include "header"
\paper{paper-height = 2.4\cm}

\new \songbookstaff
{
  \key e \minor
  \time 4/4
  \relative c'
  {
    \repeat volta 2
    {r8 e g a b4 d b g' b, d8 b8~ b8 d4 b8 a4 b8 a8~ a1}
    \repeat volta 2
    {r8 a4 b8 c2~ c8 b4 a8 b2~ b8 a4 g8 a4 b8 a8~ a1}
  }
}

