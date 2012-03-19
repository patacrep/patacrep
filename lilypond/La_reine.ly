\include "header"
\paper{paper-height = 8.8\cm}


\new \songbookstaff
{
  \key e \minor
  \time 2/2
  \relative c''{
    b8 e4 b8 e4 b4 c b b b
    b8 e4 b8 e4 b c b\trill a2
    a2 fis'2 g4 fis\trill e e fis2 g4 fis\trill e1

    fis1 g e2 g4 fis8 e d1 
    e2. d8 c b2. g4 a4. b16 a g4 fis 

    e8 e16 e e8 g c b4 g8
    e8 e16 e e8 g fis'4 e  

    << 
      {fis1 | g | e2 g4 fis8 e | d1 | 
       e2. d8 c | b2. g4 | a4. b16 a g4 fis | 
       e8 e16 e e8 g c b4 g8} 
      \\
      {
	d'4. g8 g4 d' | c b2 a4 | g4 e g a |
	\times 2/3 {b8 [c b]} \times 2/3{ a8 [b a]} g4 g |
	a8 g a4 b c | b e e e | dis2 b2 | e1}
    >>
    
    e,,8 e16 e e8 g c b4 g8 
    e8 e16 e e8 g c b4 g8 
    e4 b e b
  }
}

