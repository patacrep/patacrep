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
  paper-height = 3.3\cm
}

{
  #(set-global-staff-size 12)
  \relative c'{
    \time 2/4
    a'4~ a8 a16 b %\break
    \repeat volta 2 {d8 c16 b~ b8 a16 b d8 c16 b~ b4 e,8 a16\trill g a8 b16 g \break d'8. c16 b8\trill a16 b }
    \alternative { {c8 b\trill a8 b16 c} {c16 a b g a4\trill} }
  }
}
