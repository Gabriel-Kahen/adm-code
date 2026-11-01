import unittest

from support import run_c


class ReverseFlow(unittest.TestCase):
    def test_rerouting_preserves_flow_invariants(self):
        for source in ["netflow.c", "tmp/netflow-previous.c", "original/netflow.c"]:
            legacy = source.startswith("original/")
            declarations = "edge *e,*reverse;" if legacy else "edgenode *e,*reverse;"
            iteration = (
                "for(j=0;j<g.degree[i];j++){e=&g.edges[i][j];"
                if legacy
                else "for(e=g.edges[i];e!=NULL;e=(edgenode*)e->next){"
            )
            p = run_c(
                code=r"""
#define main archived_main
#include "SOURCE"
#undef main
int main(void) {
    flow_graph g;
    int i, j;
    long long sum;
    DECLARATIONS
    read_flow_graph(&g, 1);
    netflow(&g, 1, 6);
    for (i = 1; i <= 6; i++) {
        sum = 0;
        ITERATION
        reverse = find_edge(&g, e->v, i);
        if (e->flow != -reverse->flow || e->residual != e->capacity - e->flow || e->residual < 0)
            return 1;
        sum += e->flow;
    }
    if (sum != (i == 1 ? 2 : (i == 6 ? -2 : 0)))
        return 2;
}
return 0;
}
""".replace("SOURCE", source)
                .replace("DECLARATIONS", declarations)
                .replace("ITERATION", iteration),
                sources=["original/queue.c" if legacy else "queue.c"],
                data="6 7\n1 3 1\n1 2 1\n2 5 1\n2 4 1\n3 4 1\n4 6 1\n5 6 1\n",
                flags=["-fsanitize=undefined", "-fno-sanitize-recover=all"]
                + (
                    [
                        "-std=gnu89",
                        "-Wno-implicit-int",
                        "-Wno-implicit-function-declaration",
                        "-include",
                        "stdio.h",
                        "-include",
                        "stdlib.h",
                    ]
                    if legacy
                    else []
                ),
            )
            self.assertEqual(p.returncode, 0, p.stderr)


if __name__ == "__main__":
    unittest.main()
