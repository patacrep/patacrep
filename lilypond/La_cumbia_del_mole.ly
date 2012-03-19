\include "header"
\paper{paper-height = 2.5\cm}

\new \songbookstaff
{
  \key e \minor
  \time 2/2
  \relative c'''
  {
    \repeat volta 2 
    {
      g2 fis8 e4 dis8 e4. b8~ b4 e4 
    }
    \alternative
    {
      {	dis4. c4 b4 a8 b1 }
      
      {	dis4. e4 fis4 dis8 e4. b4 g4 fis8 e1 }
    }
  }
}

