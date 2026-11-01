import unittest
from support import ROOT,run_c

class SudokuCandidates(unittest.TestCase):
    def test_candidate_counts_are_initialized_and_selection_is_empty(self):
        for source in ['sudoku.c','original/sudoku.c','tmp/sudoku.c','tmp/sudoku-v2','datafiles/sudoku-examples/sudoku.v1']:
            legacy=source in ['original/sudoku.c','datafiles/sudoku-examples/sudoku.v1']
            if source.endswith('sudoku.v1'):
                body='''int x,y;init_board();
if(possible_count(0,0,possible)!=9)return 1;
fill_square(0,0,1);
if(possible_count(0,0,possible)!=0 || possible_count(0,1,possible)!=8)return 2;
next_square(&x,&y);return board[x][y]!=0;'''
            elif source in ['original/sudoku.c','tmp/sudoku.c']:
                body='''boardtype b;int x,y;init_board(&b);fast=smart=1;
if(possible_count(0,0,&b)!=9)return 1;
fill_square(0,0,1,&b);
if(possible_count(0,0,&b)!=0 || possible_count(0,1,&b)!=8)return 2;
next_square(&x,&y,&b);return b.m[x][y]!=0;'''
            else:
                body='''boardtype b;point p={0,0},chosen;init_board(&b);fast=smart=1;
if(possible_count(0,0,&b)!=9)return 1;
fill_square(p,1,&b);
if(possible_count(0,0,&b)!=0 || possible_count(0,1,&b)!=8)return 2;
next_square(&chosen,&b);return b.m[chosen.x][chosen.y]!=0;'''
            code='#include <stdio.h>\n#define main demo_main\n#include "'+source+'"\n#undef main\nint main(void){'+body+'}'
            flags=['-std=gnu89','-w','-Wno-return-mismatch','-fPIE','-pie','-fsanitize=memory','-fno-sanitize-memory-param-retval','-I',str(ROOT/'original')]
            r=run_c(code,sources=['original/backtrack.c'] if legacy else [],flags=flags,compiler='clang')
            self.assertEqual(r.returncode,0,source+'\n'+r.stderr)
if __name__=='__main__':unittest.main()
