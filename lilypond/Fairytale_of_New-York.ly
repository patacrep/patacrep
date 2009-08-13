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
  paper-height = 3.8\cm
}

{
	#(set-global-staff-size 14)
	\key d \major
	\time 2/4
	\partial 8 a'8
	\relative c''{
		b8 g cis e a, d, g fis e8. d16 d4 
	}
	
	\time 6/8
	a'8.^\markup {
	  (
	  \smaller \general-align #Y #DOWN \note #"4" #1
	  =
	  \smaller \general-align #Y #DOWN \note #"4." #1
	  ) }

	\relative c''{
	b16 a8 fis d fis a8. b16 a8 e8. fis16 e8 
	fis e d b a b a b cis d4.
		
	}
}

