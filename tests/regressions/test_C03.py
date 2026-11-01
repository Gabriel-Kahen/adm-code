import unittest

from support import run_c


class Incumbent(unittest.TestCase):
    def test_initial_optimum_is_saved_and_reset(self):
        code = r"""
#define main archived_main
#include "tsp-astar.c"
#undef main
int main(void) {
    tsp_instance t = {0};
    tsp_solution s = {0};
    t.n = 3;
    t.p[2].x = 1;
    t.p[3].y = 1;
    minlb = find_vertex_lower_bounds(&t, lb);
    best_solution.n = 0;
    solve_tsp(&t, &s);
    if (best_solution.n != 3 || fabs(best_solution.cost - best_cost) > 1e-12)
        return 1;
    t.n = 2;
    t.p[2].x = 8;
    minlb = find_vertex_lower_bounds(&t, lb);
    solve_tsp(&t, &s);
    if (best_solution.n != 2 || best_solution.p[1] != 1 || best_solution.p[2] != 2 ||
        fabs(best_solution.cost - 16) > 1e-12)
        return 2;
    return 0;
}
"""
        result = run_c(code, sources=["tsp-pq.c"])
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
