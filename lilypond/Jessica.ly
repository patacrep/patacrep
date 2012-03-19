\include "header"
\paper{paper-height = 1.2\cm}

\new \songbookstaff
{
  \key c \major
  \time 2/4
  \relative c''
  {
    \repeat volta 2
    {
      c2 d2 e8. f16 g8. f16~ f8. e16 d4
      c2 d2 e8. f16 g8. c16~ c8. g16 e8. d16 
      }
    c2
  }
}

