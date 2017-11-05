\include "../_lilypond/header"
\paper{paper-height = 3.6\cm}

{
  \key a \minor
  \time 2/4
  \relative c''
  {
    r8 a16 b c8 a c a b g e 
    c16 d e8 c d d e e a
    a16 b c a e'8~ e c b g e
    c16 d e c e c d8 d e e a2
  }
}
