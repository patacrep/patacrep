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
  paper-height = 3.3\cm
}

{
#(set-global-staff-size 12)
  \key c \major
	\time 2/4
	\relative c''{
  e4 c g'2 a4 a8. a16 g8 e4 c8 a'4 a8. a16 g8 f e c d2~ d4
  e8 f g4 g8. g16 f8 e d c a c4 a8 g4 c8 d e8 g4 g,8 e' e d d c2
	}
}

