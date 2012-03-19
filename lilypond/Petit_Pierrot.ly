\include "header"
\paper{
  paper-height = 2.6\cm
}

\new \songbookstaff
{
  \relative c''
  {
    \key a \minor
    \time 6/8
    
    \repeat volta 2
    {
      b4. b8 d b c4. c8 d c b4. b8 c b
    }
    \alternative
    {
      {a4 a16 b c8 b a} {a2.} 
    }

    \repeat volta 2
    {
      <<
	{e'4.~ e8 f e f4.~ f8 e d f4. e4 d8 e2.  }
	\\
	{c4.~ c8 d c d4.~ d8 c b d4. c4 b8 a4 a16 b c8 b a}
      >>
    }
    
%    e f e f e d e d e c
    
    
  }
}
