\include "header"
\paper{paper-height = 5.0\cm}

\new \songbookstaff
{
  \key d \minor
  \time 2/4
  \relative c'{
    \repeat volta 2
    {
      d8.\trill e16 f8 d g16 f e8 f4
      d8.\trill e16 f8 d e16 f e d c4
      d8.\trill e16 f8 d g16 f e8 f4
      d8.\trill e16 f8 bes a16 g f e d4
    }
    
    \repeat volta 2
    {
      d'8. bes16\trill a8 bes g16 a bes g a4
      d8. bes16\trill a8 bes c16 d c bes a4
      d8. bes16\trill a8 bes g16 a bes g a4
      d,8.\trill e16 f8 bes a16 g f e d4
    }
  }
}

