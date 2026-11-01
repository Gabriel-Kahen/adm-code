"""Independent small-instance oracles for the three language implementations.

Agreement between ports is useful, but never the sole correctness oracle here.
Witnesses are checked against the input rather than compared across tie choices.
"""

import importlib.util
import itertools
import json
import math
import os
import random
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("port_tools", ROOT / "tools" / "ports.py")
PORTS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PORTS)
LANGUAGES = tuple(os.environ.get("PORT_LANGUAGES", "cpp java python").split())


def setUpModule():
    for language in LANGUAGES:
        PORTS.build(language)


def graph(n, edges, directed=False):
    return [n, int(directed), len(edges), *itertools.chain.from_iterable(edges)]


def canonical(groups):
    return sorted(sorted(group) for group in groups)


def bellman_ford(n, edges, source, directed=False):
    distances = [math.inf] * n
    distances[source] = 0
    arcs = edges if directed else edges + [(v, u, w) for u, v, w in edges]
    for _ in range(n - 1):
        for u, v, weight in arcs:
            distances[v] = min(distances[v], distances[u] + weight)
    return [None if math.isinf(value) else value for value in distances]


def components(n, edges, removed=None):
    unseen = set(range(n)) - {removed}
    result = []
    while unseen:
        pending = [min(unseen)]
        visited = set(pending)
        while pending:
            u = pending.pop()
            for a, b, _ in edges:
                if a == u and b != removed and b not in visited:
                    visited.add(b)
                    pending.append(b)
                if b == u and a != removed and a not in visited:
                    visited.add(a)
                    pending.append(a)
        unseen -= visited
        result.append(sorted(visited))
    return sorted(result)


def edit_oracle(a, b):
    row = list(range(len(b) + 1))
    for i, left in enumerate(a, 1):
        following = [i]
        for j, right in enumerate(b, 1):
            following.append(min(row[j] + 1, following[-1] + 1, row[j - 1] + (left != right)))
        row = following
    return row[-1]


def subsequences(text):
    return {
        "".join(text[i] for i in range(len(text)) if mask & (1 << i))
        for mask in range(1 << len(text))
    }


class Conformance(unittest.TestCase):
    def invoke(self, language, operation, *arguments, error=False):
        invocation = [*PORTS.command(language), operation, *map(str, arguments)]
        result = subprocess.run(
            invocation,
            cwd=ROOT,
            env=PORTS.environment(),
            capture_output=True,
            text=True,
            timeout=15,
        )
        description = f"{language}: {operation} {arguments!r}: {result.stderr}"
        if error:
            self.assertNotEqual(result.returncode, 0, description)
            self.assertTrue(result.stderr.strip(), description)
            return None
        self.assertEqual(result.returncode, 0, description)
        try:
            value = json.loads(result.stdout)
        except (ValueError, TypeError) as failure:
            self.fail(f"{description}\nInvalid JSON: {result.stdout!r}: {failure}")
        return value

    def values(self, operation, *arguments):
        for language in LANGUAGES:
            with self.subTest(language=language, operation=operation, args=arguments):
                yield language, self.invoke(language, operation, *arguments)

    def expect(self, expected, operation, *arguments):
        for _, actual in self.values(operation, *arguments):
            self.assertEqual(actual, expected)

    def rejects(self, operation, *arguments):
        for language in LANGUAGES:
            with self.subTest(language=language, operation=operation):
                self.invoke(language, operation, *arguments, error=True)

    def test_native_library_invariants(self):
        self.expect(True, "selftest")

    def test_all_five_sorts(self):
        rng = random.Random(731)
        cases = [[], [4], [2, 2, -1, 2], list(range(15)), list(range(14, -1, -1))]
        cases += [[rng.randrange(-20, 21) for _ in range(rng.randrange(20))] for _ in range(4)]
        for method, numbers in itertools.product(
            ("insertion", "selection", "quick", "heap", "merge"), cases
        ):
            self.expect(sorted(numbers), "sort", method, *numbers)

    def test_binary_search_first_occurrence_and_insertion(self):
        for numbers in ([], [-3, 0, 0, 0, 5, 9]):
            for target in (-4, 0, 2, 10):
                index = numbers.index(target) if target in numbers else -1
                self.expect(index, "binary", target, *numbers)
                self.expect(sorted([*numbers, target]), "insert", target, *numbers)

    def test_arbitrary_precision_integer_arithmetic(self):
        cases = [(0, 1), (-123, 17), (123, -17), (-123, -17), (10**100 + 3, 10**45 + 7)]
        for a, b in cases:
            quotient = (abs(a) // abs(b)) * (-1 if (a < 0) != (b < 0) else 1)
            for operation, result in (
                ("add", a + b),
                ("sub", a - b),
                ("mul", a * b),
                ("div", quotient),
            ):
                self.expect(str(result), "bigint", operation, a, b)
        self.expect(str(2**64 - 1), "absdiff", -(2**63), 2**63 - 1)
        self.rejects("bigint", "div", 12, 0)

    def test_fibonacci_and_binomial(self):
        a, b = 0, 1
        sequence = [a]
        for _ in range(120):
            a, b = b, a + b
            sequence.append(a)
        for method in ("recursive", "memo", "table", "constant"):
            for n in (0, 1, 2, 10, 18) + (() if method == "recursive" else (92, 120)):
                self.expect(str(sequence[n]), "fib", method, n)
        for n, k in ((0, 0), (10, 0), (10, 10), (40, 20), (100, 50), (300, 150)):
            self.expect(str(math.comb(n, k)), "binomial", n, k)
        self.rejects("binomial", 4, 5)
        self.rejects("fib", "table", -1)

    def test_gcd_bezout_and_factorization(self):
        for a, b in ((0, 0), (0, -7), (-7, 0), (-24, 18), (252, 198), (1, 19)):
            for _, result in self.values("gcd", a, b):
                gcd, x, y = result
                self.assertEqual(gcd, math.gcd(a, b))
                self.assertEqual(a * x + b * y, gcd)
        for n in (1, 2, 49, 360, 1009):
            for _, factors in self.values("factors", n):
                self.assertEqual(math.prod(factors), n)
                self.assertEqual(factors, sorted(factors))
                for prime in factors:
                    self.assertGreaterEqual(prime, 2)
                    self.assertFalse(any(prime % d == 0 for d in range(2, math.isqrt(prime) + 1)))
        self.rejects("factors", 0)

    def test_finite_width_limits_are_checked_and_not_unreachable_sentinels(self):
        maximum = 2**63 - 1
        prefix = graph(2, [(0, 1, maximum)], True)
        self.expect([0, maximum], "dijkstra", *prefix, 0)
        self.expect([[0, maximum], [None, 0]], "floyd", *prefix)
        self.expect(maximum, "maxflow", *prefix, 0, 1)
        for language in LANGUAGES:
            if language in ("cpp", "java"):
                self.invoke(language, "matrix", 1, 1, 1, maximum, 2, error=True)
                self.invoke(
                    language,
                    "dijkstra",
                    *graph(3, [(0, 1, maximum), (1, 2, 1)], True),
                    0,
                    error=True,
                )
            else:
                self.assertEqual(
                    self.invoke(language, "matrix", 1, 1, 1, maximum, 2), [[2 * maximum]]
                )

    def test_distance_matrices_and_convolution(self):
        for _, result in self.values("distance", 3, 0, 1, 2, 3, 5, 2):
            self.assertAlmostEqual(result, 5)
        rng = random.Random(88)
        for rows, inner, columns in ((1, 3, 2), (3, 2, 4), (2, 1, 3)):
            left = [[rng.randrange(-5, 6) for _ in range(inner)] for _ in range(rows)]
            right = [[rng.randrange(-5, 6) for _ in range(columns)] for _ in range(inner)]
            expected = [
                [sum(left[i][k] * right[k][j] for k in range(inner)) for j in range(columns)]
                for i in range(rows)
            ]
            self.expect(expected, "matrix", rows, inner, columns, *sum(left, []), *sum(right, []))
        for left, right in (([1], [2]), ([1, -2, 3], [2, 4]), ([], [3])):
            result = [0] * (len(left) + len(right) - 1) if left and right else []
            for i, a in enumerate(left):
                for j, b in enumerate(right):
                    result[i + j] += a * b
            self.expect(result, "convolve", len(left), len(right), *left, *right)

    def test_edit_distance_and_trace(self):
        for a, b in (
            ("", ""),
            ("", "abc"),
            ("abc", ""),
            ("kitten", "sitting"),
            ("aab", "aba"),
            ("a b", "ab"),
        ):
            for _, result in self.values("edit", a, b):
                self.assertEqual(result["cost"], edit_oracle(a, b))
                i = j = cost = 0
                for operation in result["operations"]:
                    self.assertIn(operation, "MSID")
                    if operation in "MS":
                        self.assertLess(i, len(a))
                        self.assertLess(j, len(b))
                        self.assertEqual(a[i] == b[j], operation == "M")
                    i += operation in "MSD"
                    j += operation in "MSI"
                    cost += operation != "M"
                self.assertEqual((i, j, cost), (len(a), len(b), result["cost"]))
            if len(a) + len(b) < 9:
                self.expect(edit_oracle(a, b), "editbrute", a, b)

    def test_lcs_and_substring_distance_against_exhaustive_oracle(self):
        rng = random.Random(12)
        for _ in range(6):
            a = "".join(rng.choices("abc", k=rng.randrange(6)))
            b = "".join(rng.choices("abc", k=rng.randrange(6)))
            common = subsequences(a) & subsequences(b)
            for _, result in self.values("lcs", a, b):
                self.assertIn(result, common)
                self.assertEqual(len(result), max(map(len, common)))
            expected = min(
                edit_oracle(a, b[i:j]) for i in range(len(b) + 1) for j in range(i, len(b) + 1)
            )
            self.expect(expected, "substring", a, b)

    def test_partition_against_all_cuts_and_validate_witness(self):
        rng = random.Random(401)
        for n, k in ((1, 1), (5, 1), (5, 5), (7, 3), (6, 2)):
            numbers = [rng.randrange(8) for _ in range(n)]
            expected = min(
                max(sum(numbers[a:b]) for a, b in zip((0, *cuts), (*cuts, n)))
                for cuts in itertools.combinations(range(1, n), k - 1)
            )
            for _, result in self.values("partition", k, *numbers):
                groups = result["groups"]
                self.assertEqual(result["cost"], expected)
                self.assertEqual(len(groups), k)
                self.assertTrue(all(groups))
                self.assertEqual(sum(groups, []), numbers)
                self.assertEqual(max(map(sum, groups)), expected)
        self.rejects("partition", 3, 1, 2)
        self.rejects("partition", 1, -1)

    def test_subset_sum_exhaustive_witness(self):
        rng = random.Random(15)
        for numbers, target in (
            ([], 0),
            ([], 1),
            ([0, 0, 3], 0),
            *[([rng.randrange(8) for _ in range(7)], rng.randrange(28)) for _ in range(6)],
        ):
            achievable = any(
                sum(numbers[i] for i in range(len(numbers)) if mask & (1 << i)) == target
                for mask in range(1 << len(numbers))
            )
            for _, result in self.values("subsetsum", target, *numbers):
                self.assertEqual(result is not None, achievable)
                if result is not None:
                    self.assertEqual(len(result), len(set(result)))
                    self.assertTrue(all(0 <= index < len(numbers) for index in result))
                    self.assertEqual(sum(numbers[index] for index in result), target)
        self.rejects("subsetsum", 3, -2, 5)

    def test_elevator_exhaustive_stop_sets(self):
        for budget, maximum, riders in (
            (0, 6, [2, 4, 6]),
            (1, 6, [1, 3, 6]),
            (2, 6, [1, 3, 6]),
            (8, 3, [0, 1, 1, 3]),
            (2, 0, []),
        ):

            def cost(stops):
                return sum(min(abs(floor - stop) for stop in (0, *stops)) for floor in riders)

            expected = min(
                cost(stops)
                for count in range(min(budget, maximum) + 1)
                for stops in itertools.combinations(range(1, maximum + 1), count)
            )
            for _, result in self.values("elevator", budget, maximum, *riders):
                stops = result["stops"]
                self.assertLessEqual(len(stops), budget)
                self.assertEqual(stops, sorted(set(stops)))
                self.assertTrue(all(1 <= stop <= maximum for stop in stops))
                self.assertEqual(result["cost"], expected)
                self.assertEqual(cost(stops), expected)

    def test_shortest_paths_against_bellman_ford(self):
        rng = random.Random(641)
        for directed in (False, True):
            for n in (1, 4, 6):
                edges = [
                    (u, v, rng.randrange(8))
                    for u in range(n)
                    for v in range(u + 1, n)
                    if rng.random() < 0.45
                ]
                prefix = graph(n, edges, directed)
                expected = [bellman_ford(n, edges, source, directed) for source in range(n)]
                self.expect(expected, "floyd", *prefix)
                for source in (0, n - 1):
                    self.expect(expected[source], "dijkstra", *prefix, source)
                    unit = [(u, v, 1) for u, v, _ in edges]
                    self.expect(bellman_ford(n, unit, source, directed), "bfs", *prefix, source)
                    for _, visits in self.values("dfs", *prefix, source):
                        reachable = {
                            i for i, value in enumerate(expected[source]) if value is not None
                        }
                        self.assertEqual(set(visits), reachable)
                        self.assertEqual(len(visits), len(set(visits)))
                        self.assertEqual(visits[0], source)
        edges = [(0, 1, -4), (1, 2, 1), (0, 2, 7)]
        self.expect(
            [bellman_ford(3, edges, i, True) for i in range(3)], "floyd", *graph(3, edges, True)
        )
        self.rejects("dijkstra", *graph(3, edges, True), 2)
        self.rejects("floyd", *graph(2, [(0, 1, -1)]))

    def test_components_articulation_and_cycles_with_parallel_edges(self):
        cases = [
            (0, []),
            (1, []),
            (3, [(0, 1, 1), (1, 2, 1)]),
            (4, [(0, 1, 1), (0, 1, 1), (1, 2, 1)]),
            (2, [(0, 0, 1)]),
            (3, [(0, 1, 1), (1, 2, 1), (2, 0, 1)]),
        ]
        for n, edges in cases:
            expected = components(n, edges)
            prefix = graph(n, edges)
            self.expect(expected, "components", *prefix)
            articulation = [v for v in range(n) if len(components(n, edges, v)) > len(expected)]
            self.expect(articulation, "articulation", *prefix)
            self.expect(len(edges) > n - len(expected), "cycle", *prefix)
            self.expect(len(edges), "edgecount", *prefix)
            possible = any(
                all(((mask >> u) & 1) != ((mask >> v) & 1) for u, v, _ in edges)
                for mask in range(1 << n)
            )
            self.expect(possible, "bipartite", *prefix)

    def test_scc_both_algorithms_against_mutual_reachability(self):
        rng = random.Random(45)
        for n in (0, 1, 4, 7):
            edges = [(u, v, 1) for u in range(n) for v in range(n) if rng.random() < 0.27]
            distances = [bellman_ford(n, edges, i, True) for i in range(n)]
            groups = {
                tuple(
                    j
                    for j in range(n)
                    if distances[i][j] is not None and distances[j][i] is not None
                )
                for i in range(n)
            }
            expected = sorted(map(list, groups))
            for method in ("tarjan", "kosaraju"):
                self.expect(expected, "scc", method, *graph(n, edges, True))

    def test_both_topological_sorts_and_cycle_rejection(self):
        edges = [(0, 2, 1), (1, 2, 1), (2, 4, 1), (1, 3, 1), (3, 4, 1)]
        for method in ("kahn", "dfs"):
            for _, order in self.values("topo", method, *graph(6, edges, True)):
                self.assertEqual(sorted(order), list(range(6)))
                position = {v: i for i, v in enumerate(order)}
                self.assertTrue(all(position[u] < position[v] for u, v, _ in edges))
            self.rejects("topo", method, *graph(2, [(0, 1, 1), (1, 0, 1)], True))
            self.rejects("topo", method, *graph(1, [(0, 0, 1)], True))
            self.expect([], "topo", method, *graph(0, [], True))

    def test_both_spanning_forests_against_exhaustive_subsets(self):
        rng = random.Random(22)
        cases = [(0, []), (1, []), (4, [(0, 1, 2), (0, 1, 1), (2, 3, -2)])]
        cases += [
            (
                5,
                [
                    (u, v, rng.randrange(-3, 8))
                    for u in range(5)
                    for v in range(u + 1, 5)
                    if rng.random() < 0.7
                ],
            )
            for _ in range(3)
        ]
        for n, edges in cases:
            groups = components(n, edges)
            count = n - len(groups)
            possible = [
                sum(w for _, _, w in chosen)
                for chosen in itertools.combinations(edges, count)
                if components(n, list(chosen)) == groups
            ]
            expected = min(possible)
            for method in ("prim", "kruskal"):
                for _, result in self.values("mst", method, *graph(n, edges)):
                    self.assertEqual(result["cost"], expected)
                    self.assertEqual(len(result["edges"]), count)
                    self.assertEqual(components(n, result["edges"]), groups)
                    self.assertEqual(sum(edge[2] for edge in result["edges"]), expected)
                    for u, v, w in result["edges"]:
                        self.assertTrue((u, v, w) in edges or (v, u, w) in edges)

    def test_maxflow_against_all_cuts(self):
        rng = random.Random(5)
        cases = [
            (2, [(0, 1, 4), (0, 1, 7), (1, 0, 2)]),
            # A later augmenting path must cancel part of the first matching.
            (6, [(0, 1, 1), (0, 2, 1), (1, 3, 1), (1, 4, 1), (2, 3, 1), (3, 5, 1), (4, 5, 1)]),
        ]
        cases += [
            (
                n,
                [
                    (u, v, rng.randrange(6))
                    for u in range(n)
                    for v in range(n)
                    if u != v and rng.random() < 0.45
                ],
            )
            for n in (3, 4, 5, 6)
        ]
        for n, edges in cases:
            cuts = [
                set((0, *selection))
                for size in range(n - 1)
                for selection in itertools.combinations(range(1, n - 1), size)
            ]
            expected = min(
                sum(w for u, v, w in edges if u in side and v not in side) for side in cuts
            )
            self.expect(expected, "maxflow", *graph(n, edges, True), 0, n - 1)
        self.rejects("maxflow", *graph(2, [(0, 1, -1)], True), 0, 1)
        self.rejects("maxflow", *graph(2, [], True), 0, 0)

    def test_all_simple_paths_and_enumerations(self):
        edges = [(0, 1, 1), (0, 2, 1), (1, 2, 1), (1, 3, 1), (2, 3, 1), (0, 1, 1)]
        expected = [[0, 1, 2, 3], [0, 1, 3], [0, 2, 1, 3], [0, 2, 3]]
        self.expect(expected, "paths", *graph(4, edges), 0, 3)
        self.expect([[0]], "paths", *graph(1, []), 0, 0)
        for n in (0, 1, 4):
            self.expect(list(map(list, itertools.permutations(range(n)))), "permutations", n)
            expected = sorted([i for i in range(n) if mask & (1 << i)] for mask in range(1 << n))
            self.expect(expected, "subsets", n)
        for n, count in enumerate((1, 1, 0, 0, 2, 10, 4, 40, 92)):
            self.expect(count, "queens", n)

    def test_sudoku_validates_givens_and_returns_a_solution(self):
        puzzle = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
        for _, solved in self.values("sudoku", puzzle):
            self.assertEqual(len(solved), 81)
            for before, after in zip(puzzle, solved):
                if before != "0":
                    self.assertEqual(before, after)
            for i in range(9):
                self.assertEqual(set(solved[i * 9 : i * 9 + 9]), set("123456789"))
                self.assertEqual(set(solved[i::9]), set("123456789"))
            for row, column in itertools.product(range(0, 9, 3), repeat=2):
                self.assertEqual(
                    {solved[(row + i) * 9 + column + j] for i in range(3) for j in range(3)},
                    set("123456789"),
                )
        self.rejects("sudoku", "11" + "0" * 79)
        self.rejects("sudoku", "0" * 80)

    def test_convex_hull_contains_extreme_points_and_removes_collinear(self):
        cases = [
            ([], []),
            ([(1, 2)], [[1, 2]]),
            ([(0, 0), (1, 1), (2, 2), (1, 1)], [[0, 0], [2, 2]]),
            (
                [(1, 1), (0, 1), (1, 0), (0, 0), (0.5, 0.5), (0, 0)],
                [[0, 0], [1, 0], [1, 1], [0, 1]],
            ),
        ]
        for points, expected in cases:
            self.expect(expected, "hull", len(points), *sum((list(p) for p in points), []))

    def test_segments_lines_and_projections(self):
        for points, expected in (
            ((0, 0, 2, 2, 0, 2, 2, 0), True),
            ((0, 0, 1, 0, 1, 0, 2, 0), True),
            ((0, 0, 2, 0, 1, 0, 3, 0), True),
            ((0, 0, 1, 0, 2, 0, 3, 0), False),
            ((0, 0, 0, 0, 0, 0, 1, 1), True),
        ):
            self.expect(expected, "segment", *points)
        self.expect([1, 1], "intersection", 0, 0, 2, 2, 0, 2, 2, 0)
        self.expect(None, "intersection", 0, 0, 1, 0, 0, 1, 1, 1)
        for _, result in self.values("project", 3, 5, 0, 1, 4, 1):
            self.assertAlmostEqual(result[0], 3)
            self.assertAlmostEqual(result[1], 1)
        self.rejects("project", 1, 2, 0, 0, 0, 0)

    def test_triangulation_covers_polygon_and_rejects_invalid_input(self):
        for points in (
            [(0, 0), (3, 0), (3, 3), (1, 1), (0, 3)],
            [(0, 3), (1, 1), (3, 3), (3, 0), (0, 0)],
        ):
            coords = sum((list(p) for p in points), [])
            area = (
                abs(
                    sum(
                        points[i][0] * points[(i + 1) % len(points)][1]
                        - points[(i + 1) % len(points)][0] * points[i][1]
                        for i in range(len(points))
                    )
                )
                / 2
            )
            self.expect(area, "area", len(points), *coords)
            for _, triangles in self.values("triangulate", len(points), *coords):
                self.assertEqual(len(triangles), len(points) - 2)
                total = 0
                for triangle in triangles:
                    self.assertEqual(len(set(triangle)), 3)
                    self.assertTrue(all(0 <= index < len(points) for index in triangle))
                    a, b, c = [points[index] for index in triangle]
                    total += abs((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])) / 2
                self.assertAlmostEqual(total, area)
        self.rejects("triangulate", 4, 0, 0, 2, 2, 0, 2, 2, 0)
        self.rejects("triangulate", 3, 0, 0, 1, 1, 2, 2)

    def test_minimum_weight_triangulation_against_all_splits(self):
        for n in (3, 4, 6):
            points = [
                (math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n)) for i in range(n)
            ]

            def cost(i, j):
                if j - i < 2:
                    return 0
                return min(
                    cost(i, k)
                    + cost(k, j)
                    + math.dist(points[i], points[k])
                    + math.dist(points[k], points[j])
                    + math.dist(points[j], points[i])
                    for k in range(i + 1, j)
                )

            for _, result in self.values("mwt", n, *sum((list(p) for p in points), [])):
                self.assertAlmostEqual(result, cost(0, n - 1), places=7)

    def test_disk_packings_and_superman_model(self):
        for width, height, radius in ((1, 1, 1), (4, 4, 1), (10, 9, 0.7), (3, 8, 1)):

            def dense(w, h):
                if min(w, h) < 2 * radius:
                    return 0
                layers = 1 + math.floor((h - 2 * radius) / (math.sqrt(3) * radius))
                full = math.floor(w / (2 * radius))
                alternate = full if w / (2 * radius) - full >= 0.5 else full - 1
                return ((layers + 1) // 2) * full + (layers // 2) * alternate

            expected = [
                math.floor(width / (2 * radius)) * math.floor(height / (2 * radius)),
                max(dense(width, height), dense(height, width)),
            ]
            self.expect(expected, "packing", width, height, radius)
        self.rejects("packing", 2, 2, 0)
        for _, result in self.values("superman", -3, 0, 3, 0, 1, 0, 0, 1):
            self.assertAlmostEqual(result[0], 2)
            self.assertAlmostEqual(result[1], 4 + math.pi)
        self.expect([0, 0], "superman", 1, 1, 1, 1, 0)

    def test_tsp_exact_and_heuristics_validate_tours(self):
        rng = random.Random(513)
        for n in (0, 1, 2, 5, 7):
            points = [(rng.randrange(10), rng.randrange(10)) for _ in range(n)]

            def cost(tour):
                return (
                    sum(math.dist(points[tour[i]], points[tour[(i + 1) % n]]) for i in range(n))
                    if n
                    else 0
                )

            optimum = min(cost(tour) for tour in itertools.permutations(range(n)))
            for method in ("exact", "best", "sample", "hill", "anneal"):
                arguments = [method, n, *sum((list(p) for p in points), [])]
                if method in ("sample", "hill", "anneal"):
                    arguments += [37, 80]
                for language, result in self.values("tsp", *arguments):
                    self.assertEqual(sorted(result["tour"]), list(range(n)))
                    self.assertAlmostEqual(result["cost"], cost(result["tour"]), places=7)
                    self.assertGreaterEqual(result["cost"] + 1e-8, optimum)
                    if method in ("exact", "best"):
                        self.assertAlmostEqual(result["cost"], optimum, places=7)
                    else:
                        self.assertEqual(result, self.invoke(language, "tsp", *arguments))

    def test_grid_orders_are_permutations_of_rectangles(self):
        for rows, columns in ((0, 3), (2, 5), (5, 2)):
            pairs = [[i, j] for i in range(rows) for j in range(columns)]
            expected = {
                "row": pairs,
                "column": [[i, j] for j in range(columns) for i in range(rows)],
                "snake": [
                    [i, j]
                    for i in range(rows)
                    for j in (range(columns) if i % 2 == 0 else range(columns - 1, -1, -1))
                ],
                "diagonal": [
                    [i, d - i]
                    for d in range(rows + columns - 1)
                    for i in range(rows)
                    if 0 <= d - i < columns
                ],
            }
            for method, order in expected.items():
                self.expect(order, "grid", method, rows, columns)

    def test_replacement_and_suitor_ranking(self):
        for pattern, text in (("", "abc"), ("aa", "baaa"), ("z", "abc"), (" ", "a b")):
            self.expect(text.find(pattern), "find", pattern, text)
        self.expect("bbbb", "replace", "aa", 2, "a", "aa", "a", "b")
        self.expect("bbb", "replace", "aaa", 1, "a", "b")
        self.rejects("replace", "text", 1, "", "new")
        suitors = [
            ("Zoe", "A", 180, 75),
            ("Amy", "Z", 180, 70),
            ("Amy", "A", 181, 75),
            ("Bob", "B", 180, 76),
        ]
        ranked = sorted(
            suitors, key=lambda p: (abs(p[2] - 180), p[3] - 75 if p[3] > 75 else -p[3], p[1], p[0])
        )
        self.expect(
            [list(p[:2]) for p in ranked],
            "suitors",
            len(suitors),
            *sum((list(p) for p in suitors), []),
        )

    def test_card_encoding_and_war_rules(self):
        for index in (0, 3, 4, 25, 48, 51):
            card = "23456789TJQKA"[index // 4] + "cdhs"[index % 4]
            self.expect(index, "card", card)
            self.expect(card, "uncard", index)
        self.expect({"winner": "a", "steps": 1}, "war", 100, 1, 1, 48, 0)
        self.expect({"winner": "draw", "steps": 1}, "war", 100, 1, 1, 0, 1)
        self.expect({"winner": "draw", "steps": 0}, "war", 0, 1, 1, 48, 0)
        self.rejects("card", "Xs")
        self.rejects("war", 100, 1, 1, 0, 0)

    def test_cli_errors_and_arity_are_explicit(self):
        self.rejects("unknown-command")
        self.rejects("binomial", 5)
        self.rejects("binomial", 5, 2, "extra")
        self.rejects("sort", "unknown", 1, 2)
        self.rejects("matrix", 2, 2, 2, 1)
        self.rejects("bfs", *graph(2, []), 2)
        self.rejects("components", *graph(2, [(0, 1, 1)], True))
        self.rejects("distance", 2, "nan", 0, 0, 0)


if __name__ == "__main__":
    unittest.main()
