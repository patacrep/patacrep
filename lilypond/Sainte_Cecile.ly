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
  paper-height = 5.2\cm
}

{
#(set-global-staff-size 12)
  \key d \minor
	\time 2/4
	\relative c'{
  \repeat volta 2{
  d8.\trill e16 f8 d g16 f e8 f4
  d8.\trill e16 f8 d e16 f e d c4
  d8.\trill e16 f8 d g16 f e8 f4
  d8.\trill e16 f8 bes a16 g f e d4
  }

\repeat volta 2{
  d'8. bes16\trill a8 bes g16 a bes g a4
  d8. bes16\trill a8 bes c16 d c bes a4
  d8. bes16\trill a8 bes g16 a bes g a4
  d,8.\trill e16 f8 bes a16 g f e d4
  }
	}
}

