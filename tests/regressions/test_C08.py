import unittest

from support import run_c


class ReplacementProgress(unittest.TestCase):
    def test_inserted_names_are_not_processed_again(self):
        for prefix in ["", "original/"]:
            for old, new, line, expected in [
                ("ACME", "ACME Corp", "ACME ACME", "ACME Corp ACME Corp"),
                ("ACME", "ACME", "ACME", "ACME"),
                ("aa", "a", "aaaa", "aa"),
                ("aa", "", "aaaa", ""),
            ]:
                result = run_c(
                    sources=[prefix + "name.c"],
                    data=f'1\n"{old}" "{new}"\n1\n{line}\n',
                    flags=[
                        "-std=gnu89",
                        "-fsanitize=address,undefined",
                        "-fno-sanitize-recover=all",
                        "-no-pie",
                    ],
                    timeout=2,
                )
                self.assertEqual(result.stdout, expected + "\n", result.stderr)
                self.assertNotIn("ERROR: AddressSanitizer", result.stderr)
                self.assertNotIn("runtime error", result.stderr)


if __name__ == "__main__":
    unittest.main()
