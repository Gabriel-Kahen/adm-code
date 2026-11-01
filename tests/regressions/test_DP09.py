import unittest
from support import run_c

class LegacySubstringCallbacks(unittest.TestCase):
    def test_matches_and_edits_with_original_engine(self):
        for s,t,cost in [('a','a',0),('abc','xxabcxx',0),('abc','axc',1),('abcd','xabc',1),('a','bb',1),('a'*101,'a',100)]:
            r=run_c(sources=['original/substringedit.c','original/editdistance.c'],data=s+'\n'+t+'\n',flags=['-std=gnu89','-w','-include','stdio.h','-fsanitize=address,undefined'])
            self.assertEqual(r.returncode,0,r.stderr)
            self.assertEqual(r.stderr,'')
            self.assertIn('matching cost = %d'%cost,r.stdout)
if __name__=='__main__':unittest.main()
