import unittest

from support import run_c

FLAGS = [
    "-std=gnu89",
    "-Wno-implicit-int",
    "-Wno-implicit-function-declaration",
    "-include",
    "stdio.h",
    "-include",
    "stdlib.h",
    "-fsanitize=address,undefined",
    "-fno-sanitize-recover=all",
]


class LegacyMaximumVertices(unittest.TestCase):
    def test_traversal_and_weighted_arrays(self):
        tests = [
            (
                "original/bfs-demo.c",
                ["original/bfs-dfs.c", "original/graph.c", "original/queue.c"],
                "read_graph(&g,0);initialize_search(&g);bfs(&g,1);",
                False,
            ),
            (
                "original/dijkstra.c",
                ["original/wgraph.c"],
                "read_graph(&g,0);dijkstra(&g,1);",
                True,
            ),
            ("original/prim.c", ["original/wgraph.c"], "read_graph(&g,0);prim(&g,1);", True),
        ]
        for source, deps, call, weighted in tests:
            data = "100 99\n" + "".join(
                f"{i} {i + 1}" + (" 1" if weighted else "") + "\n" for i in range(1, 100)
            )
            p = run_c(
                code=r"""
#define main archived_main
#include "SOURCE"
#undef main
int main(void) {
    graph g;
    CALL return parent[100] != 99;
}
""".replace("SOURCE", source).replace("CALL", call),
                sources=deps,
                data=data,
                flags=FLAGS,
            )
            self.assertEqual(p.returncode, 0, p.stderr)

    def test_topological_arrays(self):
        p = run_c(
            code=r"""
#define main archived_main
#include "original/topsort.c"
#undef main
int main(void) {
    graph g;
    int out[MAXV + 1], i;
    read_graph(&g, 1);
    topsort(&g, out);
    for (i = 1; i <= MAXV; i++)
        if (out[i] != i)
            return 1;
    return 0;
}
""",
            sources=["original/graph.c", "original/queue.c"],
            data="100 99\n" + "".join(f"{i} {i + 1}\n" for i in range(1, 100)),
            flags=FLAGS,
        )
        self.assertEqual(p.returncode, 0, p.stderr)

    def test_flow_vertex_100(self):
        p = run_c(
            code=r"""
#define main archived_main
#include "original/netflow.c"
#undef main
int main(void) {
    flow_graph g;
    read_flow_graph(&g, 1);
    netflow(&g, 1, 100);
    return find_edge(&g, 1, 100)->flow != 1 || g.degree[100] != 1;
}
""",
            sources=["original/queue.c"],
            data="100 1\n1 100 1\n",
            flags=FLAGS,
        )
        self.assertEqual(p.returncode, 0, p.stderr)


if __name__ == "__main__":
    unittest.main()
