import re
import unittest
from support import ROOT, run_c

def function(text, name):
    match = re.search(r"(?:void|int) " + name + r"\([^;]*?\)\s*\{",text)
    start=match.start(); brace=text.index("{",match.start()); depth=1; end=brace+1
    while depth:
        depth += (text[end]=="{") - (text[end]=="}"); end+=1
    return text[start:end]

class HistoricalHull(unittest.TestCase):
    def test_collinear_and_small_hulls_in_all_copies(self):
        for name in ("original/convex-hull.c", "original/mwt.c", "tmp/mwt.c"):
            text=(ROOT/name).read_text()
            code='''#include <stdio.h>
#include <stdlib.h>
#include "geometry.h"
point first_point;
void sort_and_remove_duplicates(point in[],int*n);
int leftlower(); int smaller_angle();
'''+"\n".join(function(text,n) for n in ("convex_hull","sort_and_remove_duplicates","leftlower","smaller_angle"))+'''
int main(void) {
    point p[MAXPOLY]={{0,0},{1,0},{2,0},{3,0}};polygon h;
    convex_hull(p,4,&h);
    if(h.n!=2 || h.p[0][0]!=0 || h.p[1][0]!=3) return 1;
    convex_hull(p,0,&h);if(h.n!=0) return 2;
    p[0][0]=p[1][0]=p[2][0]=p[3][0]=1;
    convex_hull(p,4,&h);if(h.n!=1) return 3;
    p[0][0]=0;p[0][1]=0;p[1][0]=1;p[1][1]=0;
    p[2][0]=1;p[2][1]=1;p[3][0]=0;p[3][1]=1;
    convex_hull(p,4,&h);return h.n!=4;
}
'''
            result=run_c(code,sources=("geometry.c",),flags=("-w","-fsanitize=address,undefined","-fno-sanitize-recover=all","-no-pie"))
            self.assertEqual(result.returncode,0,result.stderr)

if __name__ == "__main__": unittest.main()
