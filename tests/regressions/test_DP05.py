import itertools
import re
import unittest
from support import run_c

class LargePartitionWeights(unittest.TestCase):
    def test_costs_above_old_infinity_and_int_sum(self):
        cases=[([100000,100000],2),([2147483647]*3,2),([2147483647,1,2,2147483647],3),([1000000,2000000,1,3000000],2),([2147483647]*6,4)]
        calls=''.join('puts("CASE");{int s[]={0,'+','.join(map(str,s))+'};partition(s,'+str(len(s))+','+str(k)+');}' for s,k in cases)
        for source in ['partition.c','original/partition.c']:
            code='#define main demo_main\n#include "'+source+'"\n#undef main\nint main(void){'+calls+'return 0;}'
            r=run_c(code,flags=['-std=gnu89','-w','-fsanitize=address,undefined'])
            self.assertEqual(r.returncode,0,r.stderr)
            self.assertEqual(r.stderr,'')
            for (s,k),text in zip(cases,r.stdout.split('CASE\n')[1:]):
                groups=[list(map(int,re.findall(r'\d+',line))) for line in text.splitlines()]
                self.assertEqual(len(groups),k)
                self.assertTrue(all(groups))
                self.assertEqual(sum(groups,[]),s)
                best=min(max(sum(s[a:b]) for a,b in zip((0,*cuts),(*cuts,len(s)))) for cuts in itertools.combinations(range(1,len(s)),k-1))
                self.assertEqual(max(map(sum,groups)),best)
if __name__=='__main__':unittest.main()
