\include "../_lilypond/header"
\paper{
  paper-height =3\cm
  paper-width= 10\cm
  line-width= 10\cm
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
  \key e \minor
  \numericTimeSignature
  \time 4/4 
  \repeat volta 2 {
  <e'\3>4-. b'\2-. g'\3-. e'\3-. dis'\3-.  e'\3-. fis'\3-. <g'\3>8-. fis'\3-.
  <e'\3>4-. b'\2-. g'\3-. e'\3-.  dis'\3-.  e'\3-. <fis'\3>2\prall
  }
  <d\5>8. <e\5>16 <d\5>8 <g,\6>8  <fis,\6>4.  <b,\5>8~
  <b,\5>1\prall
 %  <d'\4>8. <e'\4>16 <d'\4>8 <g\5>8  <fis\5>4.  <b\4>8~
 % <b\4>1\prall
}
\score {
  <<
   
    \new Staff 
    
    { 
       \override Staff.StringNumber #'transparent = 
##t 
      \clef "G_8" \symbols }
    %\chords { e1:m }
   \new TabStaff   {
     \override Staff.Clef #'stencil = #(lambda (grob)
    (grob-interpret-markup grob TAB))
     \symbols }
  >>
}
