import itertools
import math
import random
import unittest

from support import run_c


class BranchBound(unittest.TestCase):
    def test_cost_matches_exhaustive_tours(self):
        rng = random.Random(407)
        cases = [[(0, 9), (4, 5), (6, 7), (5, 0)]]
        cases += [
            rng.sample([(x, y) for x in range(11) for y in range(11)], rng.randint(3, 7))
            for _ in range(40)
        ]
        code = r"""
#define main archived_main
#include "tsp-astar.c"
#undef main
int main(void) {
    int count;
    scanf("%d", &count);
    while (count--) {
        tsp_instance t = {0};
        tsp_solution s = {0};
        scanf("%d", &t.n);
        for (int i = 1; i <= t.n; i++)
            scanf("%d %d", &t.p[i].x, &t.p[i].y);
        minlb = find_vertex_lower_bounds(&t, lb);
        first_solution(&s, &t);
        best_cost = solution_cost(&s, &t);
        branch_and_bound(&s, &t);
        printf("%.17g\n", best_cost);
    }
    return 0;
}
"""
        data = (
            str(len(cases))
            + "\n"
            + "".join(str(len(p)) + "\n" + "".join(f"{x} {y}\n" for x, y in p) for p in cases)
        )
        result = run_c(code, sources=["tsp-pq.c"], data=data, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        for points, got in zip(cases, map(float, result.stdout.split())):
            n = len(points)
            expected = min(
                sum(math.dist(points[t[i - 1]], points[t[i]]) for i in range(n))
                for tail in itertools.permutations(range(1, n))
                for t in [(0,) + tail]
            )
            self.assertAlmostEqual(got, expected, places=9)
        self.assertEqual(len(result.stdout.split()), len(cases))


if __name__ == "__main__":
    unittest.main()
