import unittest

from support import ROOT, run_c

HILL_STUBS = r"""
#include <stdbool.h>
#define TRUE true
#define FALSE false

typedef struct {
    int n;
} tsp_instance;
typedef struct {
    int n;
} tsp_solution;

int calls;
void initialize_solution(int n, tsp_solution *solution) {
    solution->n = n;
}
void random_solution(tsp_solution *solution) {}
double solution_cost(tsp_solution *solution, tsp_instance *instance) {
    return 1;
}
double transition(tsp_solution *solution, tsp_instance *instance, int i, int j) {
    return 0;
}
void solution_count_update(tsp_solution *solution, tsp_instance *instance) {
    calls++;
}
"""

DRIVER = r"""
int main(void) {
    tsp_instance instance = {2};
    tsp_solution solution;
    hill_climbing(&instance, &solution);
    return calls != 1;
}
"""


class HillCopies(unittest.TestCase):
    def test_no_improvement_terminates(self):
        for name in ["code-fragments/hill_climbing_cut", "datafiles/tsp-examples/annealing.c"]:
            with self.subTest(source=name):
                function = (ROOT / name).read_text()
                if name.endswith(".c"):
                    function = function.split("/* [[[ hill_climbing_cut */", 1)[1]
                    function = function.split("/* ]]] */", 1)[0]
                result = run_c(HILL_STUBS + function + DRIVER, timeout=2)
                self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
