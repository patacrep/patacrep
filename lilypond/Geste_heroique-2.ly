\include "header"
\paper{paper-height = 2.4\cm}

\new \songbookstaff
{
  \relative c''
  {
    \time 2/4
    \key c \major
    \repeat volta 2
    {    
      e8 f g8 e d4 e8 g c,4 d8 f e d16 c b4 
      c8. d16 c d c b a8 b c e b c b4 
    }
    \alternative
    {
      {a8. b16 cis4}
      {a2\trill}
    }
  }
}

