import itertools
import random
import re
import unittest
from support import run_c

class NonemptyPartitions(unittest.TestCase):
    def test_valid_partitions_match_exhaustive_optimum(self):
        rng=random.Random(2)
        cases=[([10,1,1],3),([10],1)]+[([rng.randint(1,20) for _ in range(n)],k) for n in range(2,8) for k in range(1,n+1)]
        calls=''.join('puts("CASE");{int s[]={0,'+','.join(map(str,s))+'};partition(s,'+str(len(s))+','+str(k)+');}' for s,k in cases)
        for source in ['partition.c','original/partition.c']:
            code='#define main demo_main\n#include "'+source+'"\n#undef main\nint main(void){'+calls+'return 0;}'
            r=run_c(code,flags=['-std=gnu89','-w','-fsanitize=address,undefined'])
            self.assertEqual(r.returncode,0,r.stderr)
            for (s,k),text in zip(cases,r.stdout.split('CASE\n')[1:]):
                groups=[list(map(int,re.findall(r'\d+',line))) for line in text.splitlines()]
                self.assertEqual(len(groups),k)
                self.assertTrue(all(groups))
                self.assertEqual(sum(groups,[]),s)
                best=min(max(sum(s[a:b]) for a,b in zip((0,*cuts),(*cuts,len(s)))) for cuts in itertools.combinations(range(1,len(s)),k-1))
                self.assertEqual(max(map(sum,groups)),best)
    def test_reject_more_groups_than_items(self):
        r=run_c(sources=['partition.c'],data='1 2\n10\n')
        self.assertEqual(r.stdout,'')
        self.assertIn('invalid partition dimensions',r.stderr)
if __name__=='__main__':unittest.main()
