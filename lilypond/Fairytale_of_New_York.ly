\include "header"
\paper{paper-height = 2.8\cm}

\new \songbookstaff
{
  \key d \major
  \time 2/4
  \partial 8 a'8
  \relative c''
  {
    b8 g cis e a, d, g fis e8. d16 d4 
  }

  \time 6/8
  a'8.^\markup {
    (
    \smaller \general-align #Y #DOWN \note #"4" #1
    =
    \smaller \general-align #Y #DOWN \note #"4." #1
    ) }

  \relative c''
  {
    b16 a8 fis d fis a8. b16 a8 e8. fis16 e8 
    fis e d b a b a b cis d4.
  }
}
