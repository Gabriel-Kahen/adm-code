import unittest
from support import run_c

class FlowMaximumVertex(unittest.TestCase):
    def test_complete_initialization(self):
        for source in ['netflow.c','tmp/netflow-previous.c']:
            p=run_c(code=r'''
#include <string.h>
#define main archived_main
#include "SOURCE"
#undef main
int main(void){flow_graph g;int i;memset(&g,0x55,sizeof g);initialize_graph(&g);
for(i=0;i<=MAXV;i++)if(g.degree[i]!=0 || g.edges[i]!=NULL)return 1;
g.nvertices=MAXV;insert_flow_edge(&g,1,MAXV,true,1);netflow(&g,1,MAXV);
return find_edge(&g,1,MAXV)->flow!=1;}
'''.replace('SOURCE',source),sources=['queue.c'],
                    flags=['-fsanitize=address,undefined','-fno-sanitize-recover=all'])
            self.assertEqual(p.returncode,0,p.stderr)

if __name__ == '__main__': unittest.main()
