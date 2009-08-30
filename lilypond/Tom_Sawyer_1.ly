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
  paper-height = 1.6\cm
}

{
#(set-global-staff-size 12)
  \key c \major
	\time 2/4
	\relative c''{
  e,4 c g'2 a4 c8. d16 e8 c4 g8 a4 c8. d16 e8 c d4 c2
	}
}

