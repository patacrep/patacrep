\include "header"
\paper{paper-height = 5.7\cm}


musique = 
{
  \parallelMusic #'(voiceA voiceB voiceC voiceD) 
  {
      \repeat volta 2 {g'2  g'4  f' g'  a' bes'2 bes'4 d''   c'' bes' bes' a' bes'2} |
      \repeat volta 2 {d'2  d'4  c' d'  f' f'2   f'4   f'    e'  f'   g'   f' f'2  } |
      \repeat volta 2 {bes2 bes4 a  bes c' d'2   d'4   bes   g   d'   c'   c' d'2  } |
      \repeat volta 2 {g2   g4   d  g   f  bes,2 bes,4 bes,  c   d    ees  f  bes,2} |
    
      \repeat volta 2 {bes'2 a'4 a' g'  g'   fis'2 fis' e'8 fis' g'4  g' fis' g'2} |
      \repeat volta 2 {f'2   f'4 f' d'  ees' d'2   d'   c'4      d'4  d' d'   b2 } |
      \repeat volta 2 {d'2   c'4 d' bes c'   a2    bes  g4       bes4 a  a    g2 } |
      \repeat volta 2 {bes2  f4  d  g   c    d2    bes, c4       g,4  d  d    g,2} |
    }
}
\score 
{
  \new PianoStaff 
  << 
    \musique
    \new Staff
    <<
      \key g \minor
      \voiceA \\
      \voiceB
    >>
    \new Staff 
    {
      \key g \minor
      \clef bass
      <<
	\voiceC \\
	\voiceD
      >>
    }
  >>
}

