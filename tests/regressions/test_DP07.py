import unittest

from support import run_c


class EditInputCapacity(unittest.TestCase):
    def test_full_documented_length(self):
        for driver in ["stringedit", "lcs", "substringedit", "editbrute"]:
            sources = [driver + ".c"] + ([] if driver == "editbrute" else ["editdistance.c"])
            r = run_c(
                sources=sources, data="a" * 101 + "\na\n", flags=["-fsanitize=address,undefined"]
            )
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(r.stderr, "")
            self.assertIn(
                "length of longest common subsequence = 1"
                if driver == "lcs"
                else "matching cost = 100",
                r.stdout,
            )
        for driver in ["stringedit", "lcs"]:
            r = run_c(
                sources=["original/" + driver + ".c", "original/editdistance.c"],
                data="a" * 101 + "\na\n",
                flags=["-std=gnu89", "-w", "-include", "stdio.h", "-fsanitize=address,undefined"],
            )
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(r.stderr, "")
            self.assertIn(
                "length of longest common subsequence = 1"
                if driver == "lcs"
                else "matching cost = 100",
                r.stdout,
            )

    def test_overlength_rejected_before_algorithms(self):
        for driver in ["stringedit", "lcs", "substringedit", "editbrute", "tmp/editbrute-previous"]:
            sources = [driver + ".c"] + ([] if "editbrute" in driver else ["editdistance.c"])
            r = run_c(
                sources=sources,
                data="a" * 102 + "\na\n",
                flags=["-DTRUE=1", "-DFALSE=0", "-fsanitize=address,undefined"],
            )
            self.assertEqual(r.returncode, 1, r.stderr)
            self.assertIn("at most 101 characters", r.stderr)
            self.assertNotIn("Sanitizer", r.stderr)


if __name__ == "__main__":
    unittest.main()
