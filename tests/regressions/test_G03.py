import unittest

from support import run_c


class PathInitialSlot(unittest.TestCase):
    def test_unused_zero_slot(self):
        for initial in [2, 2147483647, -2147483647]:
            p = run_c(
                code=r"""
#define main archived_main
#include "paths.c"
#undef main
void insert_edge(graph *, int, int, bool);
int main(void) {
    paths_data g;
    initialize_graph(&g.g, false);
    g.g.nvertices = 2;
    insert_edge(&g.g, 1, 2, false);
    g.s = 1;
    g.t = 2;
    int a[NMAX + 1] = {INITIAL};
    backtrack(a, 0, &g);
    return solution_count != 1;
}
""".replace("INITIAL", str(initial)),
                sources=["graph.c"],
                flags=["-fsanitize=address,undefined", "-fno-sanitize-recover=all"],
            )
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertEqual(p.stdout, "{ 1 2 }\n")

    def test_distributed_path_programs(self):
        variants = [
            (["paths.c", "graph.c"], []),
            (["tmp/paths.c", "graph.c"], []),
            (
                ["original/paths.c", "original/backtrack.c", "original/graph.c"],
                [
                    "-std=gnu89",
                    "-Wno-implicit-int",
                    "-Wno-implicit-function-declaration",
                    "-include",
                    "stdio.h",
                    "-include",
                    "stdlib.h",
                ],
            ),
        ]
        for sources, flags in variants:
            p = run_c(
                sources=sources,
                data="2 1\n1 2\n",
                flags=flags + ["-ftrivial-auto-var-init=pattern"],
            )
            if sources[0].startswith("original/"):
                self.assertGreaterEqual(
                    p.returncode, 0, p.stderr
                )  # Legacy implicit main has no exit status contract.
            else:
                self.assertEqual(p.returncode, 0, p.stderr)
            self.assertIn("{ 1 2 }", p.stdout)
            self.assertNotIn("{ }", p.stdout)


if __name__ == "__main__":
    unittest.main()
