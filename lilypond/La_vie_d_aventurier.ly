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
  \key a \minor
  \partial 8 e'8	
  \relative c''{
    a4. b8 c8 d4 c8 b8 a4 g8 a4. e8     %\break
    a4. c16 b c8 d4 e8 d2~ d4. d8       %\break
    e4. d16 e d8 c4 b8 c8 b4 g8 a4. e8  %\break
    a4. b16 a g8 e4 g8 a1	
  }
}
