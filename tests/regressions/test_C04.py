import unittest

from support import run_c


class Boundary(unittest.TestCase):
    def test_all_twenty_cities_fit_maps(self):
        code = r"""
#define main archived_main
#include "tsp-astar.c"
#undef main
int main(void) {
    tsp_instance t = {0};
    tsp_solution s = {0};
    int c[MAXCANDIDATES], nc;
    t.n = NMAX;
    for (int i = 1; i <= t.n; i++)
        t.p[i].x = i;
    minlb = find_vertex_lower_bounds(&t, lb);
    s.n = 1;
    s.p[1] = 1;
    best_cost = 1e9;
    construct_candidates(&s, 2, &t, c, &nc);
    if (nc != NMAX - 1)
        return 1;
    return c[nc - 1] != NMAX;
}
"""
        result = run_c(
            code,
            sources=["tsp-pq.c"],
            flags=["-fsanitize=address,undefined", "-fno-sanitize-recover=all", "-no-pie"],
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
