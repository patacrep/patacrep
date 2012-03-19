\include "header"
\paper{paper-height = 4.0\cm}

\new \songbookstaff
{
  \key e \minor
  \time 4/4
  \tempo 2 = 60
  \relative c''
  {
    e4 b8 e e4 \times 2/3{g8 fis e} d4 e4 <<{e2}\\{b2}>>
    g8 a b a g fis e d e fis g a b4   c8 b 
    e4 b8 e e4 \times 2/3{g8 fis e} d4 e4 <<{e2}\\{b2}>>
    g8 a b a g fis g a b b \times 2/3{a' g fis} e2
  }
}


