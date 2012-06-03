\include "header"
\paper{paper-height = 3.6\cm}




{
  \key f \major \time 4/4
 \relative c' 
	{
 \repeat volta 2 {f8 g a8. g16 f8 e f d f g a8. g16 f8 e f4}
	  \alternative {
{g8 a bes8. g16 g8 bes a f f f e g f e d4}  {a'8 d c8. bes16 f8 g a a f f a g f g e4}}
	}

}
