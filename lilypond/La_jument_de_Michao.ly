\include "header"
\paper{paper-height = 13.7\cm}

\new \songbookstaff
{
  \key a \minor
  \relative c''
  {
    \time 2/4
    a8. d16 c8 b
    \repeat volta 2
    {    
      a8. b16 a8 g 
      a8. d16 c8 b a8 a16 b a8 g 
    }
    \alternative
    { 
      {a8. d16 c8 b } {a4 a8 a8}
    }
    
    \repeat volta 2
    {    
      a8 a16 b c8 b16 a g4
      c8 b16 c d8 c16 b a8 g
    }
    
    \alternative
    { 
      {a4 a8 a8} {a8. d16 c8 b}
    }
    
    a8. b16 a8 g 
    a8. g16 a8 b c8. b16 a8 g a4 e8 a16 a
    
    \repeat volta 2 
    {
      a8 a16 b c8 b16 a g4
      c8 b16 c d8 c16 b a8 g
    }
    \alternative
    { 
      {a4 e8 a} {a8 a16 a16 d8 c8}
    }
      
    \repeat volta 2
    {
      a8 a16 a d8 c 
      b8. b16 a8 b c8. b16 a8 g
    }
    \alternative
    { 
      {a8. a16 d8 c8} {a4 e'4}
    }
    
    \repeat volta 2
    {
      e4 d8 f e4 
      e4 d4 c8 b
    }
    \alternative
    { 
      {e4 e4} {a,4 c4}
    }

    \repeat volta 2
    {
      e4 c8 a b4
      c4 d4 c8 b
    }
    \alternative
    { 
      {e4 c4} {a2}
    }

    a'2 f2 c4 d 
    
    \repeat volta 2
    {
      e4 c e4 d8 c b4 e4
    }
    \alternative
    { 
      {f4 d8 c} {d4 b8 c}
    }
    
    a2 c2 d2 f4 e c2
    c2 d2 f4 g4 e2 
  }
}

