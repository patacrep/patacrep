\include "header"
\paper{paper-height = 2.4\cm}




{
  \key d \major \time 4/4
 \relative c'
'  
	{
 \repeat volta 4 {g8 fis e fis g fis g a b1
		fis8 e d e fis2}
	  \alternative{
            {e8 fis g fis e4}
            {e8 fis e d cis b}
            {e8 fis g fis e4}
            {e8 fis e d cis b}
            }
	}
}
