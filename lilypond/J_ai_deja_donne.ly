\include "header"
\paper {
   paper-width = 8.5\cm
   line-width = 8\cm
   paper-height = 2.5\cm
}

\score
{  <<
 
  \relative c''
  { \key g \major
    \repeat volta 2 {g16 fis e4 d8 e4. fis16 g b c a4 g8 fis8. g16 a4}
    b4 e,8. b'16 c4 e,8. b'16 a4. g8 a16 b16 a4.~ a2
    r8 a16 g fis8 g a2 r8 a16 g fis8 e dis1
  }
  >>
}