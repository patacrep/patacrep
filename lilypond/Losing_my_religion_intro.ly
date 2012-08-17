\include "header"
\paper{
  paper-height = 5.5 \cm
  paper-width= 8\cm
  line-width= 7.5\cm
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
  r2 <d\4>8 <e\4> d a, |
  \repeat volta 2 {
    
    \improvisationOn
    <f>4~ <f>8 <f> <f> <f>~ <f> <f>~
    <f> <f> <f> <f>
    \improvisationOff
    <d\4>8 <e\4> d a,
    }
  \alternative {
    {   \improvisationOn
    <a>4~ <a>8 <a> <a> <a>~ <a> <a>~
    <a> <a> <a> <a>
    \improvisationOff
    <d\4>8 <e\4> d a, }
    { \improvisationOn
    <a>4 <a>8 <a>~ <a> <a> <a> <a>
    <g>4 <g>8 <g>~ <g> <g> <g> <g> }
}

}

\score {
  <<
    \chords { r1| f1 | f1 | a1:m | a1:m a1:m g1 }
    \new Staff 
    
    { 
       
       \override Staff.StringNumber #'transparent = 
##t 
     
      \clef "G_8" \symbols }
      
    %\new TabStaff   {
    %   \override Staff.Clef #'stencil = #(lambda (grob)
    % (grob-interpret-markup grob TAB))
    % \symbols }
  >>
}
