\version "2.18.0"
\include "../_lilypond/header"
\paper{paper-height = 7.85\cm paper-width = 8.5\cm}

accords = \chordmode {
  \set majorSevenSymbol = \markup{maj7}
  r2 | a2 fis2:m | a2 fis2:m | a2 fis2:m | a2 fis2:m |
  b1:m | e1:7 | a2 fis2:m | a2 fis2:m |
  f:maj7
}

melodie = \relative c' {
  \clef treble
  \key d \major % armure
  \time 4/4

  % (silence)
  % This was a tri-
  \partial 2 r2-\markup{\hspace #-7.5 \larger{This was a tri}}
  \repeat volta 2 {
    % La         Fa#m
    % -umph.
    | e8 a cis a fis a cis a
    % La         Fa#m
    %        I'm making a
    | e8 a cis a fis a cis a
    % La         Fa#m
    % note here: HUGE SUC-
    | e8 a cis a fis a cis a
    % La         Fa#m
    % -CESS.               It's
    | e8 a cis a fis a cis a
    % Sim
    % hard to over-
    | fis8 b d b fis b d b
    % Mi7
    % -state my satist-
    | e,8 gis d' gis, e gis d' gis,
  }
  \alternative {
    {
      % La         Fa#m
      % -faction
      | e8 a cis a fis a cis a
      % La         Fa#m
      %            Aperture
      | e8 a cis a fis a cis a
    }
    {
      % Fa/Do
      | f8 a c e~ e2
    }
  }
  \bar "|."
}

texteI = \lyricmode {
  umph _ _ _  _ _ _ _ | _ _ _ I'm  making _ a note |
  _ here: _ _  HUGE _ SUCESS _ | _ _ _ _  _ _ _ It's |
  hard _ to o -- _ _ ver -- _ | state _ my _  sa -- _ tis -- fa -- |
  _ ction _ _  _ _ _ _ | _ _ _ _  A -- per -- ture Sci- |
}
texteII = \lyricmode {
  -ence _ _ _  _ _ _ _ | _ _ _ We  do what we must |
  _ _ because _  _ _ we can. | _ _ _ _  _ _ _ _ |
  For _ the good  _ _ of _ | all _ of us.  _ Except _ the __ |
  _ _ _ _  _ _ _ _ |  _ _ _ _  _ _ _ _ |
  ones who are dead. _ _ _ _ |
}

\score {
  <<
    \new ChordNames {
      \set chordChanges = ##t
      \accords
    }
    \new Voice = "one" \melodie
    \new Lyrics \lyricsto "one" \texteI
    \new Lyrics \lyricsto "one" \texteII
  >>
  \layout { }
  \midi { }
}
