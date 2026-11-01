import re
import unittest

from support import run_c


class DiagonalTraversal(unittest.TestCase):
    def test_rectangles_visit_every_cell_once(self):
        sizes = [(n, m) for n in range(1, 7) for m in range(1, 7)]
        calls = "".join('puts("CASE");diagonal_order(%d,%d);' % size for size in sizes)
        for source in ["order.c", "original/order.c"]:
            code = (
                '#include <stdio.h>\n#define main demo_main\n#include "'
                + source
                + '"\n#undef main\nint main(void){'
                + calls
                + "return 0;}"
            )
            r = run_c(
                code,
                sources=["geometry.c"],
                flags=["-std=gnu89", "-w", "-fsanitize=address,undefined"],
            )
            self.assertEqual(r.returncode, 0, r.stderr)
            for (n, m), text in zip(sizes, r.stdout.split("CASE\n")[1:]):
                visits = [tuple(map(int, p)) for p in re.findall(r"\((\d+),(\d+)\)", text)]
                self.assertEqual(len(visits), n * m)
                self.assertEqual(
                    set(visits), {(i, j) for i in range(1, n + 1) for j in range(1, m + 1)}
                )
                self.assertEqual([sum(p) for p in visits], sorted(map(sum, visits)))


if __name__ == "__main__":
    unittest.main()
