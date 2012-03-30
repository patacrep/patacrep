\include "header"
\paper {
   paper-width = 8.5\cm
   line-width = 8\cm
   paper-height = 3\cm
}

\score
{  <<
 
  \relative c'''
  { \key a \major
   cis8\accent b\accent a\accent gis\accent a\accent gis\accent fis\accent e\accent
   fis4 a cis,4. fis8 fis8 fis fis a gis8. fis16 e8 fis cis4 \times 2/3 {b8 cis b} a4_^ e_^
   b'8 b b cis d4 cis8 b b a b e a a a4
   a8\accent a\accent a\accent a\accent a\accent a\accent b\accent a\accent cis4\accent b\accent a\accent gis\accent
  }
  >>
}