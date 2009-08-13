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
	\relative c'{
		\repeat volta 2 {e'8 d e a, e' d e a, d c d g, d' c d g,}
	}
}
