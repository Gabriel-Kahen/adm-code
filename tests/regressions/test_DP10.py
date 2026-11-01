import re
import unittest
from support import run_c

class SubsetTraceInitialization(unittest.TestCase):
    def test_base_and_last_rows_use_only_supplied_items(self):
        for source in ['tmp/subsetsum.c','tmp/subsetsum-debug.c']:
            for n,k,items in [(0,0,[]),(1,1,[1]),(100,1,[1]*100)]:
                data=('%d %d\n'%(n,k))+' '.join(map(str,items))+'\n'
                if source.endswith('-debug.c'):data='1\n'+data
                r=run_c(sources=[source],data=data,compiler='clang',flags=['-fPIE','-pie','-fsanitize=memory'])
                self.assertEqual(r.returncode,0,r.stderr)
                self.assertEqual(r.stderr,'')
                self.assertRegex(r.stdout,r'Is %d realizable: 1'%k)
                self.assertIn('i=0: ',r.stdout)
                if n:self.assertIn('i=%d: item=1: '%n,r.stdout)
if __name__=='__main__':unittest.main()
