\include "header"
\paper{paper-height = 2.5\cm}

\new \songbookstaff
{
  \relative c'
  {
    \time 2/4
    a'4~ a8 a16 b %\break
    \repeat volta 2 {d8 c16 b~ b8 a16 b d8 c16 b~ b4 e,8 a16\trill g a8 b16 g \break d'8. c16 b8\trill a16 b }
    \alternative { {c8 b\trill a8 b16 c} {c16 a b g a4\trill} }
  }
}
