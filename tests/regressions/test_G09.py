import unittest

from support import run_c

LEGACY = [
    "-std=gnu89",
    "-Wno-implicit-int",
    "-Wno-implicit-function-declaration",
    "-include",
    "stdio.h",
    "-include",
    "stdlib.h",
]
SAN = ["-fsanitize=undefined", "-fno-sanitize-recover=all"]


class WideGraphWeights(unittest.TestCase):
    def test_dijkstra_reaches_large_paths(self):
        for source in ["dijkstra.c", "tmp/dijkstra-previous.c", "original/dijkstra.c"]:
            legacy = source.startswith("original/")
            p = run_c(
                code=r"""
#define main archived_main
#include "SOURCE"
#undef main
int main(void) {
    graph g;
    read_graph(&g, 0);
    dijkstra(&g, 1);
    return parent[2] != 1 || parent[3] != 2;
}
""".replace("SOURCE", source),
                sources=["original/wgraph.c" if legacy else "wgraph.c"],
                data="3 2\n1 2 2147483647\n2 3 2147483647\n",
                flags=SAN + (LEGACY if legacy else []),
            )
            self.assertEqual(p.returncode, 0, p.stderr)

    def test_spanning_tree_totals(self):
        for source, deps, label in [
            ("prim.c", ["wgraph.c"], "weight = "),
            ("kruskal.c", ["wgraph.c", "set_union.c"], "weight="),
        ]:
            p = run_c(
                sources=[source, *deps], data="3 2\n1 2 2147483647\n2 3 2147483647\n", flags=SAN
            )
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertIn(label + "4294967294", p.stdout)

    def test_floyd_distances_and_infinity(self):
        for source in ["floyd.c", "original/floyd.c"]:
            legacy = source.startswith("original/")
            p = run_c(
                code=r"""
#define main archived_main
#include "SOURCE"
#undef main
int main(void) {
    adjacency_matrix g;
    read_adjacency_matrix(&g, 1);
    floyd(&g);
    return g.weight[1][3] != 4294967294LL || g.weight[3][1] != MAXINT;
}
""".replace("SOURCE", source),
                data="3 2\n1 2 2147483647\n2 3 2147483647\n",
                flags=SAN + (LEGACY if legacy else []),
            )
            self.assertEqual(p.returncode, 0, p.stderr)

    def test_legacy_prim_large_edges(self):
        p = run_c(
            code=r"""
#define main archived_main
#include "original/prim.c"
#undef main
int main(void) {
    graph g;
    read_graph(&g, 0);
    prim(&g, 1);
    return parent[2] != 1 || parent[3] != 2;
}
""",
            sources=["original/wgraph.c"],
            data="3 2\n1 2 2147483647\n2 3 2147483647\n",
            flags=SAN + LEGACY,
        )
        self.assertEqual(p.returncode, 0, p.stderr)


if __name__ == "__main__":
    unittest.main()
