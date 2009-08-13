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
  \relative c''{
    \time 6/8
    \partial 8 e8
    b4 e8 c4 e8 e16 d c8 b c a e' %\break
    b4 e8 c4 e8 e16 d c8 b a4.
	}
}
