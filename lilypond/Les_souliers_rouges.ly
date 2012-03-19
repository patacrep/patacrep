\include "header"
\paper{paper-height = 3.6\cm}

\new \songbookstaff
{
  \key g \major
  \time 2/4
  \relative c''
  {
    r8 g'16 fis e d b a g2
    r8 g'16 fis e d b a g'2
    
    \new Voice 
    {
      \set countPercentRepeats = ##t
      \repeat "percent" 3 { a,16 b b b a b b b }
    }
   
    \repeat volta 2 
    {
      g8 g16 g g8 e d8 g16 g a8 a16 a b8
      g16 g g8 e d8 g16 g a8 a16 a
    }
    g2
  }
}

