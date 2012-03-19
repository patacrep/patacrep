\include "header"
\paper{
  paper-height = 1.1\cm
  line-width   = 14.5\cm
  paper-width  = 15\cm
}

\new \songbookstaff
{
  \relative c''
  {
    \key a \minor
    \time 2/4
    \repeat volta 2
    {
      a8 c a c e d c b 
      b g b d g f e d 
      c b a b c d c b
      c d e d b d c b 
      a2
    }
  }
}
