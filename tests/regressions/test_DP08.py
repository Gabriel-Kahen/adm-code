import unittest
from support import ROOT,run_c

class BacktrackingCapacity(unittest.TestCase):
    def test_first_maximum_length_solution(self):
        for source in ['permutations.c','subsets.c','original/permutations.c','original/subsets.c']:
            original=source.startswith('original/')
            invocation=('int a[NMAX+1];backtrack(a,0,(data)(intptr_t)NMAX);' if original else
                        ('generate_permutations(NMAX);' if 'permutations' in source else 'generate_subsets(NMAX);'))
            code='''#include <stdio.h>
#include <stdarg.h>
#include <stdint.h>
#include <string.h>
int capture_printf(const char *format,...);
#define printf capture_printf
#define main demo_main
#include "'''+source+'''"
#undef main
#undef printf
extern bool finished;
static int seen[NMAX+1],count,error;
int capture_printf(const char *format,...){
    va_list args;va_start(args,format);
    if(!strcmp(format," %d")){
        int value=va_arg(args,int);
        if(value<1 || value>NMAX)error=1;
        else seen[value]++;
        count++;
    }
    va_end(args);
    if(strchr(format,'\\n'))finished=1;
    return 0;
}
int main(void){int i;'''+invocation+'''
    if(error || count!=NMAX)return 1;
    for(i=1;i<=NMAX;i++)if(seen[i]!=1)return 2;
    return 0;
}
'''
            r=run_c(code,sources=['original/backtrack.c'] if original else [],flags=['-std=gnu89','-w','-I',str(ROOT/'original'),'-fsanitize=address,undefined'])
            self.assertEqual(r.returncode,0,source+'\n'+r.stderr)
            self.assertEqual(r.stderr,'')
if __name__=='__main__':unittest.main()
