import unittest
from support import run_c

class HillRoundoff(unittest.TestCase):
    def test_equal_edge_tours_do_not_cycle(self):
        code=r'''#define main tsp_demo_main
#include "tsp.c"
#undef main
#include <float.h>
void hill_climbing(tsp_instance *,tsp_solution *);
int main(void){
    tsp_instance t={0};t.n=4;
    t.p[1].x=29;t.p[1].y=76;t.p[2].x=40;t.p[2].y=84;
    t.p[3].x=18;t.p[3].y=19;t.p[4].x=8;t.p[4].y=23;
    for(int seed=0;seed<100;seed++){
        tsp_solution s={0};srand(seed);solution_count=0;hill_climbing(&t,&s);
        if(solution_count>1000)return 1;
        double cost=solution_cost(&s,&t);
        for(int i=1;i<=4;i++)for(int j=i+1;j<=4;j++){
            double delta=transition(&s,&t,i,j);transition(&s,&t,i,j);
            if(delta < -64*DBL_EPSILON*(fabs(cost)+1))return 2;
        }
    }
    return 0;
}'''
        result=run_c(code,sources=["annealing.c","random.c"],timeout=3)
        self.assertEqual(result.returncode,0,result.stderr)

if __name__=="__main__":unittest.main()
