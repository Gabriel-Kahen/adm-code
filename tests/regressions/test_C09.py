import unittest
from support import ROOT,run_c
class HillCopies(unittest.TestCase):
    def test_no_improvement_terminates(self):
        for name in ["code-fragments/hill_climbing_cut","datafiles/tsp-examples/annealing.c"]:
            text=(ROOT/name).read_text()
            if name.endswith(".c"):text=text.split("/* [[[ hill_climbing_cut */",1)[1].split("/* ]]] */",1)[0]
            code="""#include <stdbool.h>
#define TRUE true
#define FALSE false
+typedef struct { int n; } tsp_instance;
+typedef struct { int n; } tsp_solution;
+int calls;
+void initialize_solution(int n,tsp_solution*s){s->n=n;}
+void random_solution(tsp_solution*s){}
+double solution_cost(tsp_solution*s,tsp_instance*t){return 1;}
+double transition(tsp_solution*s,tsp_instance*t,int i,int j){return 0;}
+void solution_count_update(tsp_solution*s,tsp_instance*t){calls++;}
+""".replace("\n+","\n")+text+"\nint main(void){tsp_instance t={2};tsp_solution s;hill_climbing(&t,&s);return calls!=1;}"
            result=run_c(code,timeout=2)
            self.assertEqual(result.returncode,0,result.stderr)
if __name__=="__main__":unittest.main()
