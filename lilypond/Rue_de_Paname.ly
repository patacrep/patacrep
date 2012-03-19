\include "header"
\paper{paper-height = 3.6\cm}

\new \songbookstaff
{
  \key bes \major
  \time 6/8
  \relative c''
  {
    bes4 bes8 bes a bes c4. d4 c8 bes4. d4 bes8 << {c2.}\\{r4. f,8 g a} >>
    bes4 bes8 bes a bes c4. d4 c8 d4 d8 bes4 d8 c4. a4.
    \repeat volta 2 {bes4 g8 g a bes a2.}
    bes4 g8 g a bes a4. a4 bes8 c4. d4 bes8 c2.
  }
}
