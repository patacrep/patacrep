\include "header"
\paper{paper-height = 5.0\cm}


musique = 
{
  \parallelMusic #'(voiceA voiceB voiceC voiceD) 
  {
      \repeat volta 2 {a'2  a'4  g' a'  b' c''2  c''4  e''   d''  c''  c''  b' c''2 } |
      \repeat volta 2 {e'2  e'4  d' e'  g' g'2   g'4   g'    fis' g'   a'   g' g'2  } |
      \repeat volta 2 {c'2  c'4  b  c'  d' e'2   e'4   c'    a    e'   d'   d' e'2  } |
      \repeat volta 2 {a2   a4   e  a   g  c2    c4    c     d    e    f    g  c2   } |
    
      \repeat volta 2 {c''2  b'4 b' a'  a'   gis'2 gis' fis'8 gis' a'4  a' gis' a'2   } |
      \repeat volta 2 {g'2   g'4 g' e'  f'   e'2   e'   d'4        e'4  e' e'   cis'2 } |
      \repeat volta 2 {e'2   d'4 e' c'  d'   b2    c'   a4         c'4  b  b    a2    } |
      \repeat volta 2 {c'2   g4  e  a   d    e2    c    d4         a,4  e  e    a,2   } |
    }
}
\score 
{
  \new PianoStaff 
  << 
    \musique
    \new Staff
    {
      \key a \minor
      << \voiceA \\ \voiceB >>
    }
    \new Staff 
    {
      \key a \minor
      \clef bass
      << \voiceC \\ \voiceD >>
    }
  >>
}

