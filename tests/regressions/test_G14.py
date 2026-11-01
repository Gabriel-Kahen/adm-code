import unittest

from support import run_c


class ShortestPathTreeWeight(unittest.TestCase):
    def test_tree_edges_not_sum_of_distances(self):
        for source in ["dijkstra.c", "tmp/dijkstra-previous.c"]:
            for w in [1, 2147483647]:
                call = (
                    "total=dijkstra(&g,1);"
                    if source == "dijkstra.c"
                    else "dijkstra(&g,1);total=totalweight;"
                )
                p = run_c(
                    code=r"""
#define main archived_main
#include "SOURCE"
#undef main
int main(void) {
    graph g;
    int i;
    long long total;
    read_graph(&g, 0);
    for (i = 0; i < 2; i++) {
        CALL if (total != EXPECTED) return 1;
    }
    return parent[2] != 1 || parent[3] != 2;
}
""".replace("SOURCE", source)
                    .replace("CALL", call)
                    .replace("EXPECTED", str(2 * w) + "LL"),
                    sources=["wgraph.c"],
                    data=f"3 2\n1 2 {w}\n2 3 {w}\n",
                    flags=["-fsanitize=undefined", "-fno-sanitize-recover=all"],
                )
                self.assertEqual(p.returncode, 0, p.stderr)


if __name__ == "__main__":
    unittest.main()
