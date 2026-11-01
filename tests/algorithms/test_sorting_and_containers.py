"""Deterministic comparisons with independent standard-library models."""

import heapq
import itertools
import random
import unittest
from collections import deque
from pathlib import Path

from harness import run_c

CALLERS = Path(__file__).with_name("c")
SANITIZERS = ("-fsanitize=undefined", "-fno-sanitize-recover=all")


class SortingAlgorithms(unittest.TestCase):
    def test_five_sorts_and_binary_search_against_python(self):
        random_source = random.Random(373)
        cases = [
            list(values)
            for size in range(6)
            for values in itertools.product((-1, 0, 1), repeat=size)
        ]
        cases += [[], [0], [-2147483648, 2147483647, 0, -1, 1]]
        cases += [list(range(1000)), list(range(999, -1, -1)), [7] * 1000]
        cases += [
            [random_source.randrange(-100, 101) for _ in range(random_source.randrange(129))]
            for _ in range(100)
        ]
        data = (
            str(len(cases))
            + "\n"
            + "".join(f"{len(values)} " + " ".join(map(str, values)) + "\n" for values in cases)
        )
        result = run_c(
            (CALLERS / "sorting_caller.c").read_text(),
            sources=("queue.c", "priority_queue.c", "random.c"),
            data=data,
            flags=SANITIZERS,
            timeout=10,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        lines = iter(result.stdout.splitlines())
        for case_number, values in enumerate(cases):
            for algorithm in range(5):
                with self.subTest(case=case_number, algorithm=algorithm):
                    self.assertEqual(list(map(int, next(lines).split()[1:])), sorted(values))
            self.assertEqual(
                list(map(int, next(lines).split())), [int(key in values) for key in range(-4, 5)]
            )
        self.assertIsNone(next(lines, None), "caller emitted unexpected extra output")


class ContainerAlgorithms(unittest.TestCase):
    def test_fifo_lifo_and_priority_order_with_wraparound_and_full_capacity(self):
        random_source = random.Random(374)
        operations, expected = [], []
        for insertion, removal, model, take in [
            ("q", "Q", deque(), lambda values: values.popleft()),
            ("s", "S", [], lambda values: values.pop()),
            ("p", "P", [], lambda values: heapq.heappop(values)),
        ]:

            def add(value):
                if insertion == "p":
                    heapq.heappush(model, value)
                else:
                    model.append(value)
                operations.append(f"{insertion} {value}\n")

            def remove():
                operations.append(f"{removal} 0\n")
                expected.append(take(model))

            for value in range(1000):
                add(-value)
            for _ in range(1000):
                remove()
            for _ in range(5000):
                if not model or len(model) < 150 and random_source.random() < 0.55:
                    add(random_source.randrange(-1000, 1001))
                else:
                    remove()
            while model:
                remove()
        result = run_c(
            (CALLERS / "containers_caller.c").read_text(),
            sources=("queue.c", "stack.c", "priority_queue.c"),
            data="".join(operations),
            flags=SANITIZERS,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(list(map(int, result.stdout.split())), expected)

    def test_union_find_matches_reference_partitions(self):
        random_source = random.Random(375)
        operations, expected = [], []
        for size in range(2, 51):
            labels = list(range(size + 1))
            operations.append(f"I {size} 0\n")
            for _ in range(100):
                first, second = (random_source.randint(1, size) for _ in range(2))
                if random_source.random() < 0.5:
                    operations.append(f"U {first} {second}\n")
                    old, new = labels[second], labels[first]
                    labels = [new if label == old else label for label in labels]
                else:
                    operations.append(f"F {first} {second}\n")
                    expected.append(int(labels[first] == labels[second]))
        result = run_c(
            (CALLERS / "union_find_caller.c").read_text(),
            sources=("set_union.c",),
            data="".join(operations),
            flags=SANITIZERS,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(list(map(int, result.stdout.split())), expected)


if __name__ == "__main__":
    unittest.main()
