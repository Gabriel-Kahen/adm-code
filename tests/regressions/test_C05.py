import unittest
from support import ROOT, run_c

class HillStrictDescent(unittest.TestCase):
    def test_termination_and_full_objective_local_optimum_in_all_copies(self):
        main=r'''int main(void){
    tsp_instance t={0};tsp_solution s={0};int example,seed,i,j;
    t.n=4;
    for(example=0;example<2;example++){
        if(example==0){
            t.p[1].x=29;t.p[1].y=76;t.p[2].x=40;t.p[2].y=84;
            t.p[3].x=18;t.p[3].y=19;t.p[4].x=8;t.p[4].y=23;
        }else{
            t.p[1].x=0;t.p[1].y=0;t.p[2].x=10000000;t.p[2].y=1;
            t.p[3].x=10000000;t.p[3].y=0;t.p[4].x=0;t.p[4].y=1;
        }
        for(seed=0;seed<100;seed++){
            double cost,candidate;
            srand(seed);solution_count=0;hill_climbing(&t,&s);
            if(solution_count>1000)return 1;
            cost=solution_cost(&s,&t);
            for(i=1;i<=4;i++)for(j=i+1;j<=4;j++){
                transition(&s,&t,i,j);candidate=solution_cost(&s,&t);
                transition(&s,&t,i,j);
                if(candidate<cost)return 2;
            }
            if(example==1 && cost!=20000002.0)return 3;
        }
    }
    return 0;
}'''
        for name in ("annealing.c","original/annealing.c","datafiles/tsp-examples/annealing.c","code-fragments/hill_climbing_cut"):
            if name.startswith("code-fragments/"):
                code=(ROOT/"tsp.c").read_text().split("int main(void)",1)[0]
                code+="\nint solution_count;\nvoid solution_count_update(tsp_solution*s,tsp_instance*t){solution_count++;}\n"
                code+=(ROOT/name).read_text()+main
                sources=["random.c"]
            else:
                old=name.startswith("original/")
                tsp="original/tsp.c" if old else "tsp.c"
                code='#include <stdio.h>\n#include <math.h>\n#include <stdlib.h>\n#define main archived_main\n#include "'+tsp+'"\n#undef main\n'
                code+=("int" if old else "void")+" hill_climbing(tsp_instance*,tsp_solution*);\n"+main
                sources=[name,"original/random.c" if old else "random.c"]
            result=run_c(code,sources=sources,flags=["-std=gnu89","-w","-I",str(ROOT/"tmp"),"-fsanitize=undefined","-fno-sanitize-recover=all"],timeout=3)
            self.assertEqual(result.returncode,0,(name,result.stderr))

if __name__=="__main__":unittest.main()
