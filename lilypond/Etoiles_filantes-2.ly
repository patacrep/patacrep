\include "header"
\paper{paper-height = 2.3\cm}

\new \songbookstaff
{
  \relative c''
  {
    \repeat volta 2 
    {
      a4 a8. b16 c8 d e d b4 b8. b16 b8 c b a 
      g4 g8. g16 g8 a b a 
    }
    
    \alternative
    { 
      {a4. a8 g' f4 e8} {a,1} 
    }
  }
}

