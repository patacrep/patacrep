\include "header"
\paper
{
  paper-width = 15\cm
  line-width = 14.5\cm
  paper-height = 1.4\cm
}

\new \songbookstaff
{
  \key c \minor
  \time 2/4
  \partial 8 g'8
  \relative c''
  {
    \repeat volta 2 
    {    
      c8\trill bes c d ees4. d16 ees f8 ees d\trill c
    }
    \alternative 
    { 
     {ees4 d8 g,8} {ees'8 f ees d\trill } 
    }
    c4. c8 bes4 ees8 d c4 c8 bes16 a16 g8 a bes\trill g 
    c4. d8 bes bes ees8 d c c\trill bes4 c2
  }
}
