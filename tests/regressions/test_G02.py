import itertools
import unittest

from support import run_c


class KruskalEdges(unittest.TestCase):
    def test_edge_count_and_loops(self):
        dense = list(itertools.combinations(range(1, 16), 2))
        for data, expected in [
            ("15 105\n" + "".join(f"{u} {v} 1\n" for u, v in dense), 14),
            ("2 2\n1 1 1\n1 2 2\n", 2),
            ("1 0\n", 0),
        ]:
            with self.subTest(expected=expected):
                p = run_c(
                    sources=["kruskal.c", "set_union.c", "wgraph.c"],
                    data=data,
                    flags=["-fsanitize=address,undefined", "-fno-sanitize-recover=all"],
                )
                self.assertEqual(p.returncode, 0, p.stderr)
                self.assertIn(f"Out of Kruskal: weight={expected}", p.stdout)


if __name__ == "__main__":
    unittest.main()
