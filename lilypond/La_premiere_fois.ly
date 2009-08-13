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
	\key ees \major
		\time 6/8
	\partial 4. c'8 d' ees' 
	\relative c''{
		g2.~ g8 bes bes bes aes g g4. ees~ ees8 ees d c d ees \break
		g2.~ g8 c c c bes aes g2.
	}
}

