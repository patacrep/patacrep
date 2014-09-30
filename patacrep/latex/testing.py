
# Test it out
song = r"""
\selectlanguage{french}
plop = tag
% Un commentaire
\columns{3}
\beginsong{Titre un \\Titre deux \\ Tître t{ro}ïs \\ T\^itre quatre}[album={Tagada tsoin \"itsoin}, cov={pouf.png}] % un autre
%\beginsong{Titre un \\Titre deux \\ Tître t{ro}ïs \\ T\^itre quatre}[album={Tagada tsoin \"itsoin}] % un autre
%\beginsong{Titre un \\Titre deux \\ Tître t{ro}ïs \\ T\^itre quatre}

  Dans [Dm6]cette ruedots [E7]
"""

isong = r"""
\selectlanguage{french}
\songcolumns{2}
\beginsong{Tous les bateaux, tous les oiseaux}
  [by={Michel Polnareff},cov={passe-present},album={Passé Présent}]

  Dans \[Dm6]cette ruedots [E7]
"""

tex = "D\\^iacritiqu\\'Es"

# Give the lexer some input
#if 0:
#    from syntax import parser
#    print(parser.parse(data, debug=0))
#    print(parser.parse(data).song_data())
#else:
#    from lexer import SimpleLexer
#    lexer.input(data)
#    for tok in lexer:
#        print(tok)

from patacrep.latex import tex2plain
from patacrep.latex.syntax import parsesong
from patacrep.latex.ast import AST

print(tex2plain(tex) == "DîacritiquÉs")
print(parsesong(song, AST))
print({
        "@titles": ["Titre un", "Titre deux", "Tître trois", "Tpitre quatre"],
        "@languages": set(["french"]),
        "@path": "TODO",
        "album": "Tagada tsoin ïtsoin",
        "cov": "pouf.png",
        }
        )
