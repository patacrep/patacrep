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
  \key g \major
  \relative c'{
    \time 6/8
    b'8. a16 g fis e8 fis16 g a8 b a g a g16 fis e8 %\break
    b'8. a16 g fis e8 fis16 g a8 c b a b4.
  }
}

