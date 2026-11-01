import unittest
from support import run_c

class AdjacencyDeletion(unittest.TestCase):
    def test_preserve_other_edges(self):
        for source in ['graph.c','wgraph.c']:
            for directed in [0,1]:
                insert='insert_edge(&g,1,i,directed'+(',7)' if source=='wgraph.c' else ')')+';'
                p=run_c(code=r'''
#include "SOURCE"
int main(void){graph g;int i,directed=DIRECTED;initialize_graph(&g,directed);g.nvertices=4;
for(i=2;i<=4;i++){INSERT}
delete_edge(&g,1,3,directed);
if(g.nedges!=2 || g.degree[1]!=2 || g.edges[1]->y!=4 || g.edges[1]->next->y!=2)return 1;
if(!directed && (g.degree[3]!=0 || g.edges[3]!=NULL))return 2;
delete_edge(&g,1,4,directed);delete_edge(&g,1,2,directed);
return g.nedges!=0 || g.degree[1]!=0 || g.edges[1]!=NULL;}
'''.replace('SOURCE',source).replace('DIRECTED',str(directed)).replace('INSERT',insert),
                        flags=['-fsanitize=address,undefined','-fno-sanitize-recover=all'])
                self.assertEqual(p.returncode,0,p.stderr)

if __name__ == '__main__': unittest.main()
