\include "header"
\paper{
  paper-height = 1.5 \cm
  paper-width= 5.2\cm
  line-width= 5\cm
}

TAB = \markup {
  \raise #1.5
  \sans
  \bold
  \huge
  \override #'(baseline-skip . 2.5)
  \left-align
  \center-column {
    T
    A
    B
  }
}

symbols = {
  \numericTimeSignature
  \time 4/4 
  \repeat volta 2 { 


    e'8 e' e' d' d' d' d' d' 
    c' c' c' a a a a a
    }
  

}

\score {
  <<
    \chords { c1| a1:m  }
    \new Staff 
    
    { 
       
       \override Staff.StringNumber #'transparent = 
##t 
     
      \clef "G_8" \symbols }
      
    %  \new TabStaff   {
    %    \override Staff.Clef #'stencil = #(lambda (grob)
    % (grob-interpret-markup grob TAB))
    % \symbols }
  >>
}
