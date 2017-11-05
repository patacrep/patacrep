\include "../_lilypond/header"
\paper{
  paper-height = 2.5 \cm
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
 
  
    
    \improvisationOn
    <f>4 <f>8 <f>16 <f> <f> <f> <f>8<f>8 <f>16 <f>
    <f>4 <f>8 <f>16 <f> <f> <f> <f>8<f>8 <f>16 <f>
    <f>4 <f>8 <f>8 <f>4 <f>8  <f>16 <f>
    <f>4 <f>8 <f>16 <f> <f> <f> <f>8<f>8 <f>16 <f>
    \improvisationOff
   
    
 

}

\score {
  <<
    \chords {  b1:m | a1 | g4.  fis8 e2:m | b1:m }
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
