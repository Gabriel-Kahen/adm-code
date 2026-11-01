import unittest

from support import run_c


class FloydParallelEdges(unittest.TestCase):
    def test_read_minimum_capacity_independent_of_order(self):
        for source in ["floyd.c", "original/floyd.c"]:
            for directed in [0, 1]:
                for weights in [(1, 9), (9, 1)]:
                    p = run_c(
                        code=r"""
#define main archived_main
#include "SOURCE"
#undef main
int main(void) {
    adjacency_matrix g;
    read_adjacency_matrix(&g, DIRECTED);
    floyd(&g);
    return g.weight[1][2] != 1 || g.weight[1][3] != 3 || g.weight[1][1] != 0 ||
           g.weight[2][1] != (DIRECTED ? MAXINT : 1);
}
""".replace("SOURCE", source).replace("DIRECTED", str(directed)),
                        data=f"3 5\n1 2 {weights[0]}\n1 2 {weights[1]}\n2 3 5\n2 3 2\n1 1 5\n",
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
                            if source.startswith("original/")
                            else []
                        ),
                    )
                    self.assertEqual(p.returncode, 0, p.stderr)


if __name__ == "__main__":
    unittest.main()
