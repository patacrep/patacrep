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
  paper-height = 5.0\cm
}

{
#(set-global-staff-size 12)
  \key c \major
	\time 2/4
	\relative c''{
  c8 d e8 e16 e~ e8 f16 e d4
  b8 c d8 d16 d~ d8 e16 d c4
  a8 b c8 c16 c~ c8 d16 c b4
  gis8 a b8 b16 b~ b8 c16 b a4

  a8 a a8 a16 a~ a8 a16 a d4
  d8 d d8 d16 d~ d8 e16 f e4
  r8 e8 e4 d4 e4
	}
}

