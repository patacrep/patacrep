\include "header"
\paper{paper-height = 2.2\cm}

{
  \key e \major
  \time 2/4
  \relative c''
  {
    \repeat volta 2 
    {
      e8 e16 fis gis8 e a fis gis e dis fis e dis cis2
    }
    \repeat volta 2 
    {
      a'8 \times 2/3{a16 gis fis} f8 gis fis cis fis gis fis8 fis4 d8 cis2
    }
  }
}

