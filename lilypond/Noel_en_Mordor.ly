\include "header"
\paper{paper-height = 2.4\cm}

\new \songbookstaff
{
  \key c \minor
  \time 2/4
  \partial 4 g'8 g'
  \relative c''
  {
    c bes c d ees4 
    d8 ees f4 ees8 d ees4
    g,8 g c bes c d ees 4
    d8 ees f f ees d c2
    \repeat volta 4
    {
      g4 g8 g f4. g8 aes g f ees d2
    }
  }
}


