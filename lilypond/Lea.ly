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
  paper-height = 3.2\cm
}

{
#(set-global-staff-size 12)
  \key a \minor
	\time 2/4
	\relative c''{
  e8. f16 g8 a g f e4 e16 f e d e8 c b c a4
  e'8. f16 g8 a g16 a g f e4 e16 f e d e8 c << {e2} \\ {b2} >>
	}
}

