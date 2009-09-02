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
  paper-height = 4.2\cm
}

{
#(set-global-staff-size 12)
  \key g \major
	\time 2/4
	\relative c''{
  r8 g'16 fis e d b a g2
  r8 g'16 fis e d b a g'2
  \new Voice {
     \set countPercentRepeats = ##t
       \repeat "percent" 3 { a,16 b b b a b b b }
     }
    \repeat volta 2 {g8 g16 g g8 e d8 g16 g a8 a16 a b8
    g16 g g8 e d8 g16 g a8 a16 a}
    g2
 }
}

