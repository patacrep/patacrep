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
	\relative c''{
		\repeat volta 2 {a8. b16 c8 d c b a4 a8. b16 a8 g a g f4
										 e8. f16 g8 a g f e4 e8. f16 e8 d e d c4}
	}
}
