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
  paper-height = 4.8\cm
}

{
#(set-global-staff-size 12)
	\relative c''{
		\time 6/8
		c4 c8 c b c d4. e4 d8 c4 c8 c b c << {d2.}\\{r4 g,8 g a b} >>
		c4 c8 c b c d4. e4 d8 e4 g8 g f e d2. 
		\repeat volta 2 {c4 a8 a b c b2.} 
		c4 a8 a b c b4. b4 c8 d4. e4 c8 d2.
	}
}

