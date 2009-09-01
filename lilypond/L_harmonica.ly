\version "2.12.1"

\paper
{
  make-footer=##f
  make-header=##f

  left-margin = 0\cm
  top-margin = 0\cm
  bottom-margin = 0\cm

  indent = 0\cm
  between-system-padding = 1\mm

  paper-width = 7.5\cm
  line-width = 7\cm
  paper-height = 5\cm
}

{
#(set-global-staff-size 12)
  \key a \minor
	\time 2/4
  \partial 4 e''8. d''16 	
	\relative c''{
		c8 a a g e a a c b g16 a b8 g a4.
    e'16 d c8 a a g e a a e' e8. d16 c8 b a4.
    g8 c8. c16 c8 e d8. d16 d8 e c c a c b4.
    e16 d c8 a a g e a a e' e8. d16 c8 b a2 
	}
}

