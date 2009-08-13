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
		\repeat volta 2 {a4 a8. b16 c8 d e d b4 b8. b16 b8 c b a 
										 g4 g8. g16 g8 a b a }
		\alternative{ {a4. a8 g' f4 e8} {a,1} }
	}
}
