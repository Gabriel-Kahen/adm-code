import unittest
from support import run_c

class ParallelTraversal(unittest.TestCase):
    def test_count_each_undirected_edge(self):
        cases=[('2 2\n1 2\n1 2\n',2),('3 3\n1 2\n2 3\n3 1\n',3),
               ('3 2\n1 2\n2 3\n',2),('1 1\n1 1\n',1),('1 2\n1 1\n1 1\n',2)]
        for data,count in cases:
            p=run_c(sources=['countedges.c','bfs-dfs.c','graph.c','queue.c'],data=data,
                    flags=['-fsanitize=undefined','-fno-sanitize-recover=all'])
            self.assertEqual(p.returncode,0,p.stderr)
            self.assertIn(f'nedges = {count} ',p.stdout)

    def test_cycle_detection_in_both_versions(self):
        for legacy in [False,True]:
            for data,expected in [('2 2\n1 2\n1 2\n',1),('2 1\n1 2\n',0),('1 1\n1 1\n',1)]:
                source='original/findcycle.c' if legacy else 'findcycle.c'
                prefix='original/' if legacy else ''
                p=run_c(code=r'''
#define main archived_main
#include "SOURCE"
#undef main
int main(void){graph g;read_graph(&g,0);initialize_search(&g);dfs(&g,1);return finished!=EXPECTED;}
'''.replace('SOURCE',source).replace('EXPECTED',str(expected)),
                        sources=[prefix+'bfs-dfs.c',prefix+'graph.c',prefix+'queue.c'],data=data,
                        flags=['-fsanitize=undefined','-fno-sanitize-recover=all']+(
                            ['-std=gnu89','-Wno-implicit-int','-Wno-implicit-function-declaration',
                             '-include','stdio.h','-include','stdlib.h'] if legacy else []))
                self.assertEqual(p.returncode,0,p.stderr)

if __name__ == '__main__': unittest.main()
