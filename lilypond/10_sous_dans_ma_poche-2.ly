\include "header"
\paper{paper-height = 4\cm}

\new \songbookstaff
{
  \relative c'
  {
    \key a \minor
    \time 2/4
    \partial 8 e8

    \repeat volta 2
    {  
      a8\trill a16 a g8 a16 b c8 c b16\trill a b g
      a8 a16 b g8 a16 b c16 a b g a4
    }

    \repeat volta 2
    {
      c8 c b8.\trill a16 b16 a g fis e4
      a8 a16 b g8 a16 b 
    }
    
    \alternative
    {
      {c8 c b16\trill a b8}
      {c16 a b g a4\trill}
    }
  }
}
