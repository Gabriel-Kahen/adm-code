"""Compare graph results with exhaustive cuts/trees and Bellman–Ford distances."""

import itertools
import math
import random
import re
import unittest
from pathlib import Path

from harness import run_c

CALLERS = Path(__file__).with_name("c")
SANITIZERS = ("-fsanitize=undefined", "-fno-sanitize-recover=all")


def directed_edges(edges, directed):
    return (
        list(edges)
        if directed
        else list(edges) + [(to, source, weight) for source, to, weight in edges]
    )


def distances(vertex_count, edges, start):
    """Bellman–Ford reference: infinity remains distinct from numeric distances."""
    costs = [math.inf] * (vertex_count + 1)
    costs[start] = 0
    for _ in range(vertex_count - 1):
        previous = costs.copy()
        for source, to, weight in edges:
            costs[to] = min(costs[to], previous[source] + weight)
        if costs == previous:
            break
    return costs


def graph_cases():
    random_source = random.Random(376)
    cases = [(1, [], True, 1), (4, [(1, 2, 0), (3, 4, 7)], False, 1)]
    cases += [(100, [], True, 100), (100, [(i, i + 1, 2) for i in range(1, 100)], False, 100)]
    for _ in range(120):
        size = random_source.randint(1, 9)
        directed = random_source.choice((True, False))
        pairs = (
            itertools.permutations(range(1, size + 1), 2)
            if directed
            else itertools.combinations(range(1, size + 1), 2)
        )
        edges = [
            (source, to, random_source.randint(0, 20))
            for source, to in pairs
            if random_source.random() < 0.25
        ]
        cases.append((size, edges, directed, random_source.randint(1, size)))
    return cases


def result_lines(output):
    return [line.split()[1:] for line in output.splitlines() if line.startswith("RESULT")]


class ShortestPaths(unittest.TestCase):
    def assert_parent_paths(self, cases, output, weighted):
        results = result_lines(output)
        self.assertEqual(len(results), len(cases))
        for case_number, ((size, edges, directed, start), parents) in enumerate(
            zip(cases, results)
        ):
            with self.subTest(case=case_number, start=start):
                arcs = directed_edges(edges, directed)
                costs = distances(
                    size, arcs if weighted else [(a, b, 1) for a, b, _ in arcs], start
                )
                weights = {(a, b): weight if weighted else 1 for a, b, weight in arcs}
                parents = [-1] + list(map(int, parents))
                self.assertEqual(len(parents), size + 1)
                self.assertEqual(parents[start], -1)
                for target in range(1, size + 1):
                    if costs[target] == math.inf:
                        self.assertEqual(parents[target], -1)
                        continue
                    total, vertex, seen = 0, target, set()
                    while vertex != start:
                        self.assertNotIn(vertex, seen, "parent cycle")
                        seen.add(vertex)
                        previous = parents[vertex]
                        self.assertIn((previous, vertex), weights)
                        total += weights[previous, vertex]
                        vertex = previous
                    self.assertEqual(total, costs[target])

    def test_dijkstra_parent_paths_match_bellman_ford(self):
        cases = graph_cases()
        data = (
            str(len(cases))
            + "\n"
            + "".join(
                f"{int(directed)} {start}\n{size} {len(edges)}\n"
                + "".join(f"{a} {b} {w}\n" for a, b, w in edges)
                for size, edges, directed, start in cases
            )
        )
        result = run_c(
            (CALLERS / "shortest_paths_caller.c").read_text(),
            sources=("wgraph.c",),
            data=data,
            flags=(*SANITIZERS, "-DTEST_DIJKSTRA"),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assert_parent_paths(cases, result.stdout, weighted=True)

    def test_bfs_parent_hops_match_unit_weight_bellman_ford(self):
        cases = graph_cases()
        data = (
            str(len(cases))
            + "\n"
            + "".join(
                f"{int(directed)} {start}\n{size} {len(edges)}\n"
                + "".join(f"{a} {b}\n" for a, b, _ in edges)
                for size, edges, directed, start in cases
            )
        )
        result = run_c(
            (CALLERS / "shortest_paths_caller.c").read_text(),
            sources=("graph.c", "bfs-dfs.c", "queue.c"),
            data=data,
            flags=SANITIZERS,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assert_parent_paths(cases, result.stdout, weighted=False)

    def test_floyd_all_pairs_including_unreachable_and_negative_dag_edges(self):
        cases = graph_cases()
        random_source = random.Random(377)
        for _ in range(60):
            size = random_source.randint(2, 9)
            edges = [
                (a, b, random_source.randint(-10, 20))
                for a, b in itertools.combinations(range(1, size + 1), 2)
                if random_source.random() < 0.3
            ]
            cases.append((size, edges, True, 1))
        data = (
            str(len(cases))
            + "\n"
            + "".join(
                f"{int(directed)}\n{size} {len(edges)}\n"
                + "".join(f"{a} {b} {w}\n" for a, b, w in edges)
                for size, edges, directed, _ in cases
            )
        )
        result = run_c((CALLERS / "floyd_caller.c").read_text(), data=data, flags=SANITIZERS)
        self.assertEqual(result.returncode, 0, result.stderr)
        actual = result_lines(result.stdout)
        self.assertEqual(len(actual), len(cases))
        for case_number, ((size, edges, directed, _), values) in enumerate(zip(cases, actual)):
            with self.subTest(case=case_number):
                expected = [
                    cost
                    for start in range(1, size + 1)
                    for cost in distances(size, directed_edges(edges, directed), start)[1:]
                ]
                self.assertEqual(
                    [math.inf if value == "INF" else int(value) for value in values], expected
                )


class SpanningTreesAndFlow(unittest.TestCase):
    def test_both_mst_algorithms_match_exhaustive_spanning_trees(self):
        random_source = random.Random(378)
        cases = []
        for _ in range(80):
            size = random_source.randint(2, 6)
            pairs = list(itertools.combinations(range(1, size + 1), 2))
            chosen = {(vertex, vertex + 1) for vertex in range(1, size)}
            for pair in random_source.sample(pairs, random_source.randint(0, min(len(pairs), 8))):
                chosen.add(pair)
            edges = [(a, b, random_source.randint(-10, 20)) for a, b in sorted(chosen)]
            cases.append((size, edges))
        expected = []
        for size, edges in cases:
            best = math.inf
            for candidate in itertools.combinations(edges, size - 1):
                reached = {1}
                for _ in range(size):
                    reached |= {b for a, b, _ in candidate if a in reached} | {
                        a for a, b, _ in candidate if b in reached
                    }
                if len(reached) == size:
                    best = min(best, sum(weight for _, _, weight in candidate))
            expected.append(best)
        data = (
            str(len(cases))
            + "\n"
            + "".join(
                f"{size} {len(edges)}\n" + "".join(f"{a} {b} {w}\n" for a, b, w in edges)
                for size, edges in cases
            )
        )
        for algorithm in ("prim", "kruskal"):
            flags = (*SANITIZERS, "-DTEST_KRUSKAL") if algorithm == "kruskal" else SANITIZERS
            result = run_c(
                (CALLERS / "spanning_tree_caller.c").read_text(),
                sources=("wgraph.c", "set_union.c") if algorithm == "kruskal" else ("wgraph.c",),
                data=data,
                flags=flags,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual([int(values[0]) for values in result_lines(result.stdout)], expected)
            descriptions = result.stdout.split("CASE\n")[1:]
            self.assertEqual(len(descriptions), len(cases))
            for (size, edges), description, optimum in zip(cases, descriptions, expected):
                selected = [
                    tuple(map(int, pair))
                    for pair in re.findall(r"edge \((\d+),(\d+)\)", description)
                ]
                weights = {frozenset((a, b)): weight for a, b, weight in edges}
                self.assertEqual(len(selected), size - 1)
                self.assertEqual(sum(weights[frozenset(pair)] for pair in selected), optimum)
                reached = {1}
                for _ in range(size):
                    reached |= {b for a, b in selected if a in reached} | {
                        a for a, b in selected if b in reached
                    }
                self.assertEqual(reached, set(range(1, size + 1)))

    def test_max_flow_matches_every_source_sink_cut_and_flow_conservation(self):
        random_source = random.Random(379)
        cases = [(2, []), (2, [(1, 2, 0), (1, 2, 4), (1, 2, 3), (2, 1, 5)])]
        for _ in range(120):
            size = random_source.randint(2, 7)
            edges = [
                (a, b, random_source.randint(0, 9))
                for a, b in itertools.permutations(range(1, size + 1), 2)
                if random_source.random() < 0.3
            ]
            if edges and random_source.random() < 0.5:
                edges.append(random_source.choice(edges))
            cases.append((size, edges))
        expected = []
        for size, edges in cases:
            cuts = [
                {1} | {vertex for bit, vertex in enumerate(range(2, size)) if mask & (1 << bit)}
                for mask in range(1 << (size - 2))
            ]
            expected.append(
                min(
                    sum(
                        capacity
                        for source, to, capacity in edges
                        if source in cut and to not in cut
                    )
                    for cut in cuts
                )
            )
        data = (
            str(len(cases))
            + "\n"
            + "".join(
                f"{size} {len(edges)}\n" + "".join(f"{a} {b} {w}\n" for a, b, w in edges)
                for size, edges in cases
            )
        )
        result = run_c(
            (CALLERS / "max_flow_caller.c").read_text(),
            sources=("queue.c",),
            data=data,
            flags=SANITIZERS,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([int(values[0]) for values in result_lines(result.stdout)], expected)


if __name__ == "__main__":
    unittest.main()
