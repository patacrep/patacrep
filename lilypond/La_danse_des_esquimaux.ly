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
  paper-height = 3.1\cm
}

{
#(set-global-staff-size 12)
  \key e \major
	\time 2/4
	\relative c''{
  \repeat volta 2 {e8 e16 fis gis8 e a fis gis e dis fis e dis cis2}
  \repeat volta 2 {a'8 \times 2/3{a16 gis fis} f8 gis fis cis fis gis fis8 fis4 d8 cis2}
	}
}

