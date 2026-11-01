"""Failures in the test infrastructure must remain actionable and bounded."""

import os
import unittest
from unittest.mock import patch

from harness import compiled_c, run_c, run_executable


class CTestHarness(unittest.TestCase):
    def test_one_compilation_can_serve_multiple_input_cases(self):
        code = r"""
#include <stdio.h>
int main(void) {
    int value;
    scanf("%d", &value);
    printf("%d\n", value * 2);
    return 0;
}
"""
        with compiled_c(code) as executable:
            for value in (-10, 0, 12):
                result = run_executable(executable, data=str(value))
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout, f"{value * 2}\n")

    def test_explicit_compiler_overrides_the_cc_environment(self):
        code = r"""
int main(void) {
#ifdef __clang__
    return 0;
#else
    return 1;
#endif
}
"""
        with patch.dict(os.environ, {"CC": "clang"}):
            self.assertEqual(run_c(code).returncode, 0)
            self.assertEqual(run_c(code, compiler="gcc").returncode, 1)

    def test_compiler_failure_includes_the_command_and_diagnostic(self):
        with self.assertRaises(AssertionError) as failure:
            run_c(r"""
int main(void) {
    return missing_value;
}
""")
        self.assertIn("C compilation failed:", str(failure.exception))
        self.assertIn("missing_value", str(failure.exception))

    def test_nonterminating_caller_has_an_input_diagnostic(self):
        with self.assertRaises(AssertionError) as failure:
            run_c(
                r"""
int main(void) {
    for (;;) {
    }
}
""",
                data="case 17",
                timeout=0.05,
            )
        self.assertIn("exceeded 0.05s", str(failure.exception))
        self.assertIn("case 17", str(failure.exception))


if __name__ == "__main__":
    unittest.main()
