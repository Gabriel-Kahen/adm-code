import unittest
from support import run_c

FLAGS=['-std=gnu89','-Wno-implicit-int','-Wno-implicit-function-declaration',
       '-include','stdio.h','-include','stdlib.h','-fsanitize=address,undefined','-fno-sanitize-recover=all']
CALLER=r'''
#define main archived_main
#include "original/netflow.c"
#undef main
int main(void){flow_graph g;read_flow_graph(&g,1);netflow(&g,1,g.nvertices);
return find_edge(&g,1,g.nvertices)->flow!=1 || g.degree[g.nvertices]!=g.nvertices-1;}
'''

class ResidualNeighborCapacity(unittest.TestCase):
    def test_incoming_arcs_expand_residual_outdegree(self):
        for n in [52,100]:
            p=run_c(code=CALLER,sources=['original/queue.c'],flags=FLAGS,
                    data=f'{n} {n-1}\n'+''.join(f'{i} {n} 1\n' for i in range(1,n)))
            self.assertEqual(p.returncode,0,p.stderr)

    def test_invalid_graph_sizes_and_labels_fail_explicitly(self):
        for data in ['101 0\n','2 -1\n','2 1\n1 3 1\n','2 1\n0 2 1\n','2 1\n1 2 -1\n']:
            p=run_c(code=CALLER,sources=['original/queue.c'],flags=FLAGS,data=data)
            self.assertEqual(p.returncode,1,p.stderr)
            self.assertIn('Invalid flow',p.stderr)
            self.assertNotIn('runtime error',p.stderr)
            self.assertNotIn('ERROR: AddressSanitizer',p.stderr)

if __name__ == '__main__': unittest.main()
