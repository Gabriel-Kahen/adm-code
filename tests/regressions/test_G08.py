import unittest
from support import run_c

class FloydReachability(unittest.TestCase):
    def test_negative_arcs_do_not_create_paths(self):
        for source in ['floyd.c','original/floyd.c']:
            legacy=source.startswith('original/')
            flags=(['-std=gnu89','-Wno-implicit-int','-Wno-implicit-function-declaration',
                    '-include','stdio.h','-include','stdlib.h'] if legacy else [])
            p=run_c(code=r'''
#define main archived_main
#include "SOURCE"
#undef main
int main(void){adjacency_matrix g;int i;read_adjacency_matrix(&g,1);floyd(&g);
for(i=1;i<=4;i++)if(g.weight[1][i]!=(i==1?0:MAXINT))return 1;
return g.weight[2][4]!=-3 || g.weight[4][2]!=MAXINT;}
'''.replace('SOURCE',source),data='4 2\n2 3 -5\n3 4 2\n',
                    flags=flags+['-fsanitize=undefined','-fno-sanitize-recover=all'])
            self.assertEqual(p.returncode,0,p.stderr)

if __name__ == '__main__': unittest.main()
