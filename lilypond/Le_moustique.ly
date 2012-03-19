\include "header"
\paper{paper-height = 2.4\cm}

\new \songbookstaff
{
  \relative c''
  {
    \key f \major
    \time 2/4
    \partial 8 c8
    \repeat volta 2 
    {
      f4 d e c8 d8\(d8\) d4 a8 bes4. c8 e8 e c4 d a8 c8\(c8\) bes4 g8  
    }
    \alternative
    {
      { f4. c'8 }
      { f,2 }
    }
  }
}
