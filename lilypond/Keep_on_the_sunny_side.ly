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
  \key bes \major
	\time 2/4
	\relative c'{
  r8 f g a bes4 d8. bes16 c8 bes a g f2~
  f4 bes8 d f4 f8. g16 f8 d bes d c2~
  c4 c8 d ees4 d8 c f8. g16 f8 ees d8. d16 d8 c bes4 
  bes8 d c8. c16 d8 c a f g a bes2
	}
}

