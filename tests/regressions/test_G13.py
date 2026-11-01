import unittest
from support import run_c

class UnreachablePath(unittest.TestCase):
    def test_paths_report_failure_without_fabricated_vertices(self):
        sources=['bfs-dfs.c','wgraph.c','netflow.c','tmp/netflow-previous.c',
                 'original/bfs-dfs.c','original/wgraph.c','original/netflow.c']
        for source in sources:
            legacy=source.startswith('original/')
            callbacks=''
            if source.endswith('bfs-dfs.c'):
                callbacks=('int process_vertex_early(int v){return 0;} int process_vertex_late(int v){return 0;} '
                           'int process_edge(int x,int y){return 0;} int valid_edge(int e){return 1;}' if legacy else
                           'void process_vertex_early(int v){} void process_vertex_late(int v){} void process_edge(int x,int y){}')
            p=run_c(code=callbacks+r'''
#define main archived_main
#include "SOURCE"
#undef main
int main(void){int parents[4]={-1,-1,1,-1};
if(!find_path(1,2,parents))return 1;
if(find_path(1,3,parents))return 2;
if(!find_path(1,1,parents))return 3;
return 0;}
'''.replace('SOURCE',source),sources=['original/queue.c' if legacy else 'queue.c'],
                    flags=['-fsanitize=undefined','-fno-sanitize-recover=all']+(
                        ['-std=gnu89','-Wno-implicit-int','-Wno-implicit-function-declaration',
                         '-include','stdio.h','-include','stdlib.h'] if legacy else []))
            self.assertEqual(p.returncode,0,p.stderr)
            self.assertEqual(p.stdout,'\n1 2\nNo path\n1')

if __name__ == '__main__': unittest.main()
