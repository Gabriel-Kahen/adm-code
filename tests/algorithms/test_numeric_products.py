"""Signed convolution and rectangular matrix products stay in exact int range."""

import random
import unittest
from pathlib import Path

from harness import compiled_c, run_c, run_executable

CALLERS = Path(__file__).with_name("c")
SANITIZERS = ("-fsanitize=undefined", "-fno-sanitize-recover=all")


class NumericProducts(unittest.TestCase):
    def test_convolution_matches_independent_coefficient_accumulation(self):
        random_source = random.Random(381)
        cases = [([0], [0]), ([1], [-1]), ([1, -1] * 50, [-1, 1] * 50)]
        cases += [
            (
                [random_source.randint(-10, 10) for _ in range(random_source.randint(1, 40))],
                [random_source.randint(-10, 10) for _ in range(random_source.randint(1, 40))],
            )
            for _ in range(80)
        ]
        with compiled_c(sources=("convolve.c",), flags=SANITIZERS) as executable:
            for case_number, (first, second) in enumerate(cases):
                with self.subTest(case=case_number):
                    expected = [0] * (len(first) + len(second) - 1)
                    for left, a in enumerate(first):
                        for right, b in enumerate(second):
                            expected[left + right] += a * b
                    data = (
                        f"{len(first)}\n"
                        + " ".join(map(str, first))
                        + f"\n{len(second)}\n"
                        + " ".join(map(str, second))
                        + "\n"
                    )
                    result = run_executable(executable, data=data)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(list(map(int, result.stdout.split())), expected)

    def test_rectangular_matrix_products_match_dot_products(self):
        random_source = random.Random(382)
        cases = []
        for _ in range(100):
            rows, inner, columns = (random_source.randint(1, 8) for _ in range(3))
            first = [[random_source.randint(-10, 10) for _ in range(inner)] for _ in range(rows)]
            second = [
                [random_source.randint(-10, 10) for _ in range(columns)] for _ in range(inner)
            ]
            cases.append((first, second))
        data = str(len(cases)) + "\n"
        expected = []
        for first, second in cases:
            data += (
                f"{len(first)} {len(first[0])}\n"
                + "\n".join(" ".join(map(str, row)) for row in first)
                + "\n"
            )
            data += (
                f"{len(second)} {len(second[0])}\n"
                + "\n".join(" ".join(map(str, row)) for row in second)
                + "\n"
            )
            expected.append(
                [
                    sum(a * b for a, b in zip(row, column))
                    for row in first
                    for column in zip(*second)
                ]
            )
        result = run_c((CALLERS / "matrix_caller.c").read_text(), data=data, flags=SANITIZERS)
        self.assertEqual(result.returncode, 0, result.stderr)
        actual = [
            list(map(int, line.split()[1:]))
            for line in result.stdout.splitlines()
            if line.startswith("RESULT")
        ]
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
