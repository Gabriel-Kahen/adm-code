import unittest

from support import run_c


class ParallelFlow(unittest.TestCase):
    def test_parallel_capacities(self):
        for source in ["netflow.c", "tmp/netflow-previous.c"]:
            for capacity in [1, 2147483647]:
                p = run_c(
                    sources=[source, "queue.c"],
                    data=f"1 2\n2 3\n1 2 {capacity}\n1 2 {capacity}\n2 1 7\n",
                    flags=["-fsanitize=undefined", "-fno-sanitize-recover=all"],
                )
                self.assertEqual(p.returncode, 0, p.stderr)
                self.assertIn(f"total flow = {2 * capacity}\n", p.stdout)

    def test_legacy_aggregation(self):
        p = run_c(
            code=r"""
#define main archived_main
#include "original/netflow.c"
#undef main
int main(void) {
    flow_graph g;
    edge *p;
    initialize_graph(&g);
    g.nvertices = 2;
    insert_flow_edge(&g, 1, 2, TRUE, 2147483647);
    insert_flow_edge(&g, 1, 2, TRUE, 2147483647);
    netflow(&g, 1, 2);
    p = find_edge(&g, 1, 2);
    return p->capacity != 4294967294LL || p->flow != 4294967294LL;
}
""",
            sources=["original/queue.c"],
            flags=[
                "-std=gnu89",
                "-Wno-implicit-int",
                "-Wno-implicit-function-declaration",
                "-include",
                "stdio.h",
                "-include",
                "stdlib.h",
                "-fsanitize=undefined",
                "-fno-sanitize-recover=all",
            ],
        )
        self.assertEqual(p.returncode, 0, p.stderr)


if __name__ == "__main__":
    unittest.main()
