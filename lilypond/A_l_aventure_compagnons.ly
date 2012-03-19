\include "header"
\paper{paper-height = 5.6\cm}

\new \songbookstaff
{
  \key ees \major
  \time 2/4
  \relative c''
  {
    << {g'2 f8. g16 aes4~ aes4 g8. f16 ees8. d16} \\ {bes'2 aes8. g16 f4~ f4 ees8. d16 c8. bes16} >>
    << {c4}\\{aes4} >> bes2
    c8. bes16 c8. d16 ees8. g16 f8. d16 ees4 << {g4~ g4}\\{bes4~ bes} >> ees,8. g16
    \repeat volta 4 { bes8. g16 ees8. g16 bes8. g16 ees8. g16 }
    \alternative { {bes8. g16 \times 2/3 { bes,8 c d } \times 2/3 { ees f g } ees8. g16} { bes4 << {g4~ g2}\\{bes4~ bes2} >> } }
  }
}
