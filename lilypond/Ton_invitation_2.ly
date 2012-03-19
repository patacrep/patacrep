\include "header"
\paper{paper-height = 3.8\cm}

\new \songbookstaff
{
  \relative c''
  {
    \time 4/4
    \key b \minor
    \repeat volta 2
    {
      g8 a4 ais8 b2 g8 b4 ais8 fis2
    }
    fis8\trill d4 cis8 b2
    d8 d4 e8 cis2
    d8 d4 cis8 b4. d16 d
    d8 e4 d8 cis4 d'8 d

    \repeat volta 2
    {
      cis8 d16 cis~ cis8 d16 cis b4 a b4. g8 fis2
    }
    \alternative
    {
      {fis8\trill a4 ais8 b2 g8 b4 g8 fis4 d'8 d8} {fis,1}
    }
  }
}

