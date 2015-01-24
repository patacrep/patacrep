import glob
import os
import unittest

from patacrep.songs.chordpro import syntax as chordpro

class ParserTestCase(unittest.TestCase):

    def test_txt(self):
        for txt in sorted(glob.glob(os.path.join(
            os.path.dirname(__file__),
            '*.txt',
        ))):
            basename = txt[:-len('.txt')]
            with open("{}.sgc".format(basename), 'r', encoding='utf8') as sourcefile:
                with open("{}.txt".format(basename), 'r', encoding='utf8') as expectfile:
                    #print(os.path.basename(sourcefile.name))
                    #with open("{}.txt.diff".format(basename), 'w', encoding='utf8') as difffile:
                    #    difffile.write(
                    #        str(chordpro.parse_song(
                    #            sourcefile.read(),
                    #            os.path.basename(sourcefile.name),
                    #            )).strip()
                    #        )
                    #    sourcefile.seek(0)
                    self.assertMultiLineEqual(
                        str(chordpro.parse_song(
                            sourcefile.read(),
                            os.path.basename(sourcefile.name),
                            )).strip(),
                        expectfile.read().strip(),
                        )

    def test_tex(self):
        # TODO
        pass
