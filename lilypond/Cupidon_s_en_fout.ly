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
  paper-height = 3.5\cm
}

{
#(set-global-staff-size 12)
  \key a \minor
	\time 2/4
  \relative c''{
   r8 a16 b c8 a c a b g e 
   c16 d e8 c d d e e a
   a16 b c a e'8~ e c b g e
   c16 d e c e c d8 d e e a2
	}
}

