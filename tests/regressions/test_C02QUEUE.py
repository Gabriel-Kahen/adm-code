import unittest
from support import run_c

CALLER=r'''
#include "tsp-pq.c"
static priority_queue q;
int main(int argc,char **argv){tsp_solution s={0};s.cost=3;
pq_init(&q);q.n=argc>1?PQ_SIZE:PQ_SIZE-1;pq_insert(&q,&s);
return q.n!=PQ_SIZE || q.q[PQ_SIZE].cost!=3;}
'''

class TspQueueCapacity(unittest.TestCase):
    def test_full_queue_fails_explicitly(self):
        p=run_c(code=CALLER,args=['full'],
                flags=['-fsanitize=address,undefined','-fno-sanitize-recover=all'])
        self.assertEqual(p.returncode,1,p.stderr)
        self.assertEqual(p.stderr,'TSP priority queue capacity exceeded\n')
        self.assertEqual(p.stdout,'')

    def test_final_available_slot_remains_usable(self):
        p=run_c(code=CALLER,flags=['-fsanitize=address,undefined','-fno-sanitize-recover=all'])
        self.assertEqual(p.returncode,0,p.stderr)
        self.assertEqual(p.stderr,'')

if __name__ == '__main__': unittest.main()
