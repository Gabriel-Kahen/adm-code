"""Partial C templates and search signatures are not complete caller programs."""

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.format_code import format_c_examples  # noqa: E402


class EmbeddedCallers(unittest.TestCase):
    def test_interpolated_include_boundary_is_preserved(self):
        sources = [
            r"""code = '#include "' + filename + '"\nint main(void) { return 0; }' """,
            "signature = 'int main(void)'",
        ]
        for source in sources:
            with self.subTest(source=source):
                with patch(
                    "tools.format_code.format_c", side_effect=AssertionError("Incomplete C unit")
                ):
                    self.assertEqual(format_c_examples(source, "unused-clang-format"), source)


if __name__ == "__main__":
    unittest.main()
