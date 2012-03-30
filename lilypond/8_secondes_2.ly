\include "header"
\paper {
   paper-width = 8.5\cm
   line-width = 8\cm
   paper-height = 1.3\cm
}

\score
{  <<

   \relative c''
  { \key a \major
   b8 b b cis d4 cis8 b b a b e a a a4
   a8\accent a\accent a\accent a\accent a\accent a\accent b\accent a\accent cis4\accent b\accent a\accent gis\accent
  }
  >>
}