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
  \key d \minor
	\time 2/4
	\relative c''{
  d8 a' d, a e' f c' a, e' a, a a~ a2
  c8 g' c, g d' e b' d, a' d, d d~ d2
	}
}

