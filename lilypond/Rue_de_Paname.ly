\include "header"
\paper{paper-height = 3.6\cm}

{
  \time 6/8
  \relative c''
  {
    c4 c8 c b c d4. e4 d8 c4 c8 c b c << {d2.}\\{r4 g,8 g a b} >>
    c4 c8 c b c d4. e4 d8 e4 g8 g f e d2. 
    \repeat volta 2 {c4 a8 a b c b2.} 
    c4 a8 a b c b4. b4 c8 d4. e4 c8 d2.
  }
}
