\include "../_lilypond/header"
\paper{
  paper-height =3.5\cm
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
  \key a \minor
  \numericTimeSignature
  \time 4/4 
  \repeat volta 2 {
  <a,e\4a\3>8 <a,e\4a\3> g,\6 a, c\5 a, g,\6 <a,e\4a\3>~
  <a,e\4a\3>8 <a,e\4a\3> g,\6 a, c\5 a, g,\6 <a,e\4a\3>
  <d'a\3d\2fis'\1>4  <d'a\3d\2g'\1>4  <d'a\3d\2g'\1>8<d'a\3d\2fis'\1>4 <d'a\3d\2fis'\1>8~ 
  <d'a\3d\2fis'\1>8  <d'a\3d\2fis'\1>8 <d'a\3d\2g'\1>4  <d'a\3d\2g'\1>8<d'a\3d\2fis'\1>4 <d'a\3d\2fis'\1>8  }
}
\score {
  <<
   
    \new Staff 
    
    { 
       \override Staff.StringNumber #'transparent = 
##t 
      \clef "G_8" \symbols }
    \chords { \set chordChanges = ##t  \powerChords a1:1.5 |  a1:1.5 | d4 d4.:sus4 d4. | d4 d4.:sus4 d4.  }
   \new TabStaff   {
     \override Staff.Clef #'stencil = #(lambda (grob)
    (grob-interpret-markup grob TAB))
     \symbols }
  >>
}
