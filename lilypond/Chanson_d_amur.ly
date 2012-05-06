\include "header"
\paper{paper-height = 2.4\cm}




{
  \key g \minor \time 4/4
 \relative c'
  
	{
 \repeat volta 2 {c8 d ees g f a c a 
	  bes d bes g bes4 g8 d
	  c d ees g f a c a}
	  \alternative {
	  {bes d4. bes8 d4 bes8}
	  {bes1}}
	}

}
