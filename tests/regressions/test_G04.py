import unittest

from support import run_c


class PathMaximum(unittest.TestCase):
    def test_hundred_vertex_chain(self):
        data = "100 99\n" + "".join(f"{v} {v + 1}\n" for v in range(1, 100))
        for sources in [
            ["paths.c", "graph.c"],
            ["tmp/paths.c", "graph.c"],
            ["original/paths.c", "original/backtrack.c", "original/graph.c"],
        ]:
            legacy = sources[0].startswith("original/")
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
                sources=sources,
                data=data,
                timeout=10,
                flags=flags + ["-fsanitize=address,undefined", "-fno-sanitize-recover=all"],
            )
            self.assertNotIn("runtime error", p.stderr)
            if legacy:
                self.assertGreaterEqual(p.returncode, 0, p.stderr)
            else:
                self.assertEqual(p.returncode, 0, p.stderr)
            self.assertIn("{ " + " ".join(map(str, range(1, 101))) + " }", p.stdout)
            if sources[0] == "paths.c":
                self.assertIn("{ " + " ".join(map(str, range(100, 0, -1))) + " }", p.stdout)


if __name__ == "__main__":
    unittest.main()
