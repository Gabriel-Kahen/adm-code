"""Small exhaustive problems give references independent of the C recurrences."""

import itertools
import random
import unittest
from pathlib import Path

from harness import run_c

CALLERS = Path(__file__).with_name("c")
SANITIZERS = ("-fsanitize=undefined", "-fno-sanitize-recover=all")


def edit_distance(first, second):
    previous = list(range(len(second) + 1))
    for row, left in enumerate(first, start=1):
        current = [row]
        for column, right in enumerate(second, start=1):
            current.append(
                min(current[-1] + 1, previous[column] + 1, previous[column - 1] + (left != right))
            )
        previous = current
    return previous[-1]


def subsequences(word):
    return {
        "".join(word[index] for index in range(len(word)) if mask & (1 << index))
        for mask in range(1 << len(word))
    }


class StringAlgorithms(unittest.TestCase):
    def test_edit_lcs_and_substring_costs_with_parent_witnesses(self):
        words = [
            "".join(letters)
            for length in range(4)
            for letters in itertools.product("ab", repeat=length)
        ]
        pairs = list(itertools.product(words, repeat=2))
        data = (
            str(len(pairs))
            + "\n"
            + "".join(f"{first or '-'} {second or '-'}\n" for first, second in pairs)
        )
        references = {
            "edit": [edit_distance(first, second) for first, second in pairs],
            "lcs": [
                len(first)
                + len(second)
                - 2 * max(map(len, subsequences(first) & subsequences(second)))
                for first, second in pairs
            ],
            "substring": [
                min(
                    edit_distance(first, second[start:end])
                    for start in range(len(second) + 1)
                    for end in range(start, len(second) + 1)
                )
                for first, second in pairs
            ],
        }
        for algorithm, extra_flags in [
            ("edit", ()),
            ("lcs", ("-DTEST_LCS",)),
            ("substring", ("-DTEST_SUBSTRING",)),
        ]:
            with self.subTest(algorithm=algorithm):
                result = run_c(
                    (CALLERS / "string_costs_caller.c").read_text(),
                    sources=("editdistance.c",),
                    data=data,
                    flags=(*SANITIZERS, *extra_flags),
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(list(map(int, result.stdout.split())), references[algorithm])


class SubsetSum(unittest.TestCase):
    def test_truth_and_reconstruction_against_all_subset_sums(self):
        random_source = random.Random(380)
        cases = [([], 0), ([], 1), ([0, 0, 0], 0), ([0, 2, 2], 4)]
        cases += [
            (
                [random_source.randint(0, 15) for _ in range(random_source.randint(0, 12))],
                random_source.randint(0, 100),
            )
            for _ in range(250)
        ]
        expected = []
        for values, target in cases:
            achievable = {
                sum(values[index] for index in range(len(values)) if mask & (1 << index))
                for mask in range(1 << len(values))
            }
            expected.append(int(target in achievable))
        data = (
            str(len(cases))
            + "\n"
            + "".join(
                f"{len(values)} {target}\n" + " ".join(map(str, values)) + "\n"
                for values, target in cases
            )
        )
        result = run_c((CALLERS / "subset_sum_caller.c").read_text(), data=data, flags=SANITIZERS)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(list(map(int, result.stdout.split())), expected)


if __name__ == "__main__":
    unittest.main()
