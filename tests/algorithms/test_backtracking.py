"""The generic callback engine must enumerate and unwind application state."""

import unittest
from pathlib import Path

from harness import compiled_c, run_executable

CALLER = Path(__file__).with_name("c") / "backtrack_caller.c"
SANITIZERS = ("-fsanitize=address,undefined", "-fno-sanitize-recover=all", "-no-pie")


class GenericBacktracking(unittest.TestCase):
    def test_binary_solution_counts_and_balanced_early_stop(self):
        cases = [(length, 0) for length in range(13)]
        cases += [(12, limit) for limit in (1, 2, 3, 17)] + [(0, 1)]
        data = str(len(cases)) + "\n" + "".join(f"{length} {limit}\n" for length, limit in cases)
        with compiled_c(
            CALLER.read_text(),
            sources=("backtrack.c",),
            flags=(*SANITIZERS, "-Wall", "-Wextra", "-Werror"),
        ) as executable:
            result = run_executable(executable, data=data)
        self.assertEqual(result.returncode, 0, result.stderr)
        results = [tuple(map(int, line.split())) for line in result.stdout.splitlines()]
        self.assertEqual(len(results), len(cases))
        for (length, limit), (solutions, moves, finished) in zip(cases, results):
            with self.subTest(length=length, stop_after=limit):
                self.assertEqual(solutions, limit or 2**length)
                self.assertEqual(finished, bool(limit))
                if not limit:
                    self.assertEqual(moves, 2 * (2**length - 1))


if __name__ == "__main__":
    unittest.main()
