import unittest
from support import run_c

class TspDistances(unittest.TestCase):
    def test_promote_before_subtraction_or_squaring(self):
        for source in ["tsp.c","tsp-astar.c"]:
            if source=="tsp.c":
                main=r'''int main(void){tsp_instance t={0};tsp_solution s={0};t.n=2;initialize_solution(2,&s);t.p[1].x=INT_MIN;t.p[2].x=INT_MAX;return fabs(distance(&s,1,2,&t)-4294967295.0)>1e-6;}'''
                others=["annealing.c","random.c"]
            else:
                main=r'''int main(void){return fabs(d(INT_MIN,0,INT_MAX,0)-4294967295.0)>1e-6;}'''
                others=["tsp-pq.c"]
            code='#define main archived_main\n#include "'+source+'"\n#undef main\n#include <limits.h>\n'+main
            result=run_c(code,sources=others,flags=["-fsanitize=undefined","-fno-sanitize-recover=all"])
            self.assertEqual(result.returncode,0,result.stderr)

if __name__=="__main__":unittest.main()
