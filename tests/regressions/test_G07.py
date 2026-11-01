import unittest

from support import run_c


class FloydDiagonal(unittest.TestCase):
    def test_zero_length_paths(self):
        for source in ["floyd.c", "original/floyd.c"]:
            legacy = source.startswith("original/")
            flags = (
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
            )
            p = run_c(
                code=r"""
#define main archived_main
#include "SOURCE"
#undef main
int main(void) {
    adjacency_matrix g;
    int i;
    read_adjacency_matrix(&g, 0);
    floyd(&g);
    for (i = 1; i <= g.nvertices; i++)
        if (g.weight[i][i] != 0)
            return 1;
    return g.weight[1][2] != 7 || g.weight[2][1] != 7;
}
""".replace("SOURCE", source),
                data="3 2\n1 2 7\n3 3 9\n",
                flags=flags + ["-fsanitize=undefined", "-fno-sanitize-recover=all"],
            )
            self.assertEqual(p.returncode, 0, p.stderr)


if __name__ == "__main__":
    unittest.main()
