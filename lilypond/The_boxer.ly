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
  \key c \major
	\time 4/4
	\relative c'{
  e2 g c,4 d e2  d2~ d4. g8 g2~ g4. f8 e4 g c4. g8 e4 g a e g2 f2 f2 e8 e d c d2 c2
	}
}

