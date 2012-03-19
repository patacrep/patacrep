\include "header"
\paper{paper-height = 5.2\cm}

\new \songbookstaff
{
  \relative c'''
  {
    \key c \major
    \time 2/4
    \partial 8 g8
				%harmonica
    c4. g8 a8 g4 e8 f2~ f4 g8 f8 e2 f8 e4 c8 d2~ d8
    d16 e16 f8 d8 e8 d4 c8 f8 e4 c8 d2~ d8 
    d16 e16 f8 d8 e8 d4 c8 f8 e4 c8 g'2
    
				%guitare
    \repeat volta 2
    {
      g8 f4 e8 c8 d4 e8 d4~ d8 d16 e16 f8 e4 d8
    }
    e8 d4 c8 f8 e4 c8 d4~ d8 d16 e16 f8 e4 d8 e8 d4 c8 f8 e4 c8 g'2

  }


}

