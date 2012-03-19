\include "header"
\paper{paper-height = 6.1\cm}

\new \songbookstaff
{
  \key e \minor
  \time 2/4
  \relative c'
  {
    r4 r8 e8
    \repeat volta 2
    {
      b'8 b a b g4. g8 fis fis g fis e4 
      dis8 e e4 dis8 e e4 dis8 e e4 dis8 e e4. e8 
    }

    a8 a a fis g4. g8 fis fis g a b4. b8 
    c c c a b4. g8 fis fis g fis e4
    dis8 e e4 dis8 e e4 dis8 e e4 dis8 e e4. e8 
    
    \repeat volta 2
    {
      c'4 a b g a8 a g a b2
      c4 a b g a8 a g fis e2
    }
  }
}

