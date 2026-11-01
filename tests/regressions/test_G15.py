import unittest
from support import run_c

class BipartiteLoops(unittest.TestCase):
    def test_loops_are_not_bipartite(self):
        for data,expected in [('1 1\n1 1\n',0),('4 2\n1 2\n3 3\n',0),
                              ('4 4\n1 2\n2 3\n3 4\n4 1\n',1),('1 0\n',1)]:
            p=run_c(code=r'''
#define main archived_main
#include "bipartite.c"
#undef main
int main(void){graph g;read_graph(&g,0);twocolor(&g);return bipartite!=EXPECTED;}
'''.replace('EXPECTED',str(expected)),sources=['graph.c','bfs-dfs.c','queue.c'],data=data,
                    flags=['-fsanitize=undefined','-fno-sanitize-recover=all'])
            self.assertEqual(p.returncode,0,p.stderr)

    def test_legacy_bfs_reports_self_edges(self):
        p=run_c(sources=['original/bfs-demo.c','original/bfs-dfs.c','original/graph.c','original/queue.c'],
                data='1 1\n1 1\n',flags=['-std=gnu89','-Wno-implicit-int','-Wno-implicit-function-declaration',
                    '-include','stdio.h','-include','stdlib.h','-fsanitize=undefined','-fno-sanitize-recover=all'])
        self.assertGreaterEqual(p.returncode,0,p.stderr)
        self.assertNotIn('runtime error',p.stderr)
        self.assertIn('processed edge (1,1)',p.stdout)

if __name__ == '__main__': unittest.main()
