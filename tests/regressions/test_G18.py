import unittest

from support import run_c


class LegacyFlowTotal(unittest.TestCase):
    def test_sum_only_source_adjacencies(self):
        for data, total in [
            ("1 2\n51 0\n", 0),
            ("1 2\n2 2\n1 2 5\n1 2 7\n", 12),
            ("100 2\n100 1\n100 2 7\n", 7),
            ("1 3\n3 3\n1 2 5\n2 3 4\n3 2 2\n", 4),
        ]:
            p = run_c(
                sources=["original/netflow.c", "original/queue.c"],
                data=data,
                flags=[
                    "-std=gnu89",
                    "-Wno-implicit-int",
                    "-Wno-implicit-function-declaration",
                    "-include",
                    "stdio.h",
                    "-include",
                    "stdlib.h",
                    "-fsanitize=address,undefined",
                    "-fno-sanitize-recover=all",
                ],
            )
            # The historical implicit-int main has no defined success status.
            self.assertGreaterEqual(p.returncode, 0, p.stderr)
            self.assertNotIn("runtime error", p.stderr)
            self.assertNotIn("ERROR: AddressSanitizer", p.stderr)
            self.assertIn(f"total flow = {total}\n", p.stdout)


if __name__ == "__main__":
    unittest.main()
