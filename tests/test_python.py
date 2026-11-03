# Copyright 2003-2020 by Steven S. Skiena; all rights reserved.
# Permission is granted for use in non-commerical applications
# provided this copyright notice remains intact and unchanged.
#
# These programs appear in my books:
#
# "The Algorithm Design Manual" by Steven Skiena, second edition, Springer,
# London 2008.  See out website www.algorist.com for additional information
# or https://www.amazon.com/exec/obidos/ASIN/1848000693/thealgorith01-20
#
# "Programming Challenges: The Programming Contest Training Manual"
# by Steven Skiena and Miguel Revilla, Springer-Verlag, New York 2003.
# See our website www.programming-challenges.com for additional information,
# or https://www.amazon.com/exec/obidos/ASIN/0387001638/thealgorithmrepo/


from python.annealing import repeated_tsp as search_repeated_tsp
from python.annealing import traveling_salesperson as search_traveling_salesperson
from python.backtrack import backtrack as search_backtrack
from python.bfs_dfs import breadth_first_search as graphs_breadth_first_search
from python.bfs_dfs import reconstruct_path as graphs_reconstruct_path
from python.bignum import big_integer as numeric_big_integer
from python.convolve import convolve as numeric_convolve
from python.distance import euclidean_distance as numeric_euclidean_distance
from python.editdistance import edit_distance as dynamic_edit_distance
from python.elevator import elevator_stops as dynamic_elevator_stops
from python.fib import fibonacci as numeric_fibonacci
from python.findcycle import has_undirected_cycle as graphs_has_undirected_cycle
from python.gcd import extended_gcd as numeric_extended_gcd
from python.geometry import Line as geometry_Line
from python.geometry import closest_point as geometry_closest_point
from python.geometry import intersection as geometry_intersection
from python.geometry import orientation as geometry_orientation
from python.geometry import parallel as geometry_parallel
from python.geometry import point_and_slope_to_line as geometry_point_and_slope_to_line
from python.geometry import points_to_line as geometry_points_to_line
from python.geometry import polygon_area as geometry_polygon_area
from python.geometry import same_line as geometry_same_line
from python.geometry import triangle_area as geometry_triangle_area
from python.graph import Graph as graphs_Graph
from python.list_demo import LinkedList as containers_LinkedList
from python.name import replace_names as demos_replace_names
from python.netflow import maximum_flow as graphs_maximum_flow
from python.order import grid_order as demos_grid_order
from python.plates import array_to_hex as geometry_array_to_hex
from python.plates import cartesian_to_hex as geometry_cartesian_to_hex
from python.plates import hex_to_array as geometry_hex_to_array
from python.plates import hex_to_cartesian as geometry_hex_to_cartesian
from python.plates import plates_on_top as geometry_plates_on_top
from python.priority_queue import MinHeap as containers_MinHeap
from python.queue import Queue as containers_Queue
from python.random import RandomSource as numeric_RandomSource
from python.set_union import DisjointSet as containers_DisjointSet
from python.sorting import SORTS as sorting_SORTS
from python.stack import Stack as containers_Stack
from python.strong import (
    strongly_connected_components as graphs_strongly_connected_components_first,
)
from python.strong1 import (
    strongly_connected_components as graphs_strongly_connected_components_second,
)
from python.subsetsum import subset_sum as dynamic_subset_sum
from python.sudoku import solve_sudoku as search_solve_sudoku
from python.tree_demo import BinarySearchTree as containers_BinarySearchTree
from python.triangulate import triangulate as geometry_triangulate
from python.tsp import swap_delta as search_swap_delta
from python.tsp import tour_cost as search_tour_cost
from python.war import card_name as demos_card_name
from python.war import card_rank as demos_card_rank
from python.war import war as demos_war


def graphs_strongly_connected_components(graph, method="tarjan"):
    return (
        graphs_strongly_connected_components_first(graph)
        if method == "tarjan"
        else graphs_strongly_connected_components_second(graph)
    )


"""Native invariant tests for APIs that the shared CLI does not expose directly."""
import itertools
import math
import os
import random
import subprocess
import sys
import unittest
from pathlib import Path


class LibraryTests(unittest.TestCase):
    def test_queue_and_stack(self):
        queue = containers_Queue(range(8))
        stack = containers_Stack(range(8))
        self.assertEqual([queue.dequeue() for _ in range(8)], list(range(8)))
        self.assertEqual([stack.pop() for _ in range(8)], list(range(7, -1, -1)))
        for operation in (queue.dequeue, stack.pop):
            with self.assertRaises(IndexError):
                operation()
        queue.enqueue(9)
        stack.push(9)
        self.assertEqual(queue.dequeue(), stack.pop())

    def test_min_heap_randomized_mutation(self):
        source = random.Random(123)
        heap = containers_MinHeap([9, 2, 4])
        oracle = [9, 2, 4]
        for _ in range(200):
            if not oracle or source.randrange(2):
                value = source.randrange(-50, 50)
                heap.push(value)
                oracle.append(value)
            else:
                expected = min(oracle)
                self.assertEqual(heap.peek(), expected)
                self.assertEqual(heap.pop(), expected)
                oracle.remove(expected)
            self.assertEqual(len(heap), len(oracle))
        self.assertEqual([heap.pop() for _ in range(len(heap))], sorted(oracle))
        with self.assertRaises(IndexError):
            heap.pop()
        with self.assertRaises(IndexError):
            heap.peek()

    def test_disjoint_set(self):
        sets = containers_DisjointSet(20)
        for first in range(0, 20, 2):
            self.assertTrue(sets.union(first, first + 1))
            self.assertFalse(sets.union(first, first + 1))
        for first in range(20):
            for second in range(20):
                self.assertEqual(sets.find(first) == sets.find(second), first // 2 == second // 2)
        for first in range(1, 20):
            sets.union(0, first)
        self.assertEqual({sets.find(value) for value in range(20)}, {sets.find(0)})
        self.assertEqual(sets.size[sets.find(0)], 20)
        with self.assertRaises(ValueError):
            sets.find(-1)

    def test_linked_list_and_binary_tree(self):
        linked = containers_LinkedList()
        for value in (2, 1, 2, 3):
            linked.insert(value)
        self.assertEqual(list(linked), [3, 2, 1, 2])
        self.assertEqual(linked.search(2).value, 2)
        self.assertTrue(linked.delete(2))
        self.assertEqual(list(linked), [3, 1, 2])
        self.assertFalse(linked.delete(8))
        self.assertIsNone(linked.search(8))
        tree = containers_BinarySearchTree()
        values = [8, 3, 10, 1, 6, 14, 4, 7, 13, 8]
        oracle = set(values)
        for value in values:
            tree.insert(value)
        for value in (8, 1, 14, 6, 10, 7, 3, 4, 13):
            self.assertEqual(list(tree), sorted(oracle))
            self.assertIsNotNone(tree.search(value))
            self.assertTrue(tree.delete(value))
            oracle.remove(value)
            self.assertIsNone(tree.search(value))
        self.assertEqual(list(tree), [])
        self.assertFalse(tree.delete(8))

    def test_all_sorts_exhaustive_small(self):
        for length in range(5):
            for values in itertools.product((-1, 0, 1), repeat=length):
                for method in sorting_SORTS.values():
                    self.assertEqual(method(list(values)), sorted(values))

    def test_numeric_and_random_source(self):
        for index in (0, 1, 2, 18, 120):
            self.assertEqual(numeric_fibonacci(index, "memo"), numeric_fibonacci(index, "constant"))
        self.assertEqual(numeric_big_integer("div", -7, 3), -2)
        self.assertEqual(numeric_euclidean_distance([], []), 0)
        self.assertEqual(numeric_convolve([], [1]), [])
        for a in range(-8, 9):
            for b in range(-8, 9):
                gcd, x, y = numeric_extended_gcd(a, b)
                self.assertEqual(gcd, math.gcd(a, b))
                self.assertEqual(a * x + b * y, gcd)
        first, second = (numeric_RandomSource(1337), numeric_RandomSource(1337))
        self.assertEqual(
            [first.integer(-9, 8) for _ in range(100)], [second.integer(-9, 8) for _ in range(100)]
        )
        for _ in range(100):
            self.assertTrue(-2 <= first.integer(-2, 3) <= 3)
            self.assertTrue(-3 <= first.real(-3, 2) < 2)
            self.assertEqual(first.real(4, 4), 4)
            self.assertEqual(sorted(first.permutation(list(range(20)))), list(range(20)))
        with self.assertRaises(ValueError):
            first.integer(2, 1)
        with self.assertRaises(ValueError):
            first.real(2, 1)

    def test_graph_mutation_and_paths(self):
        graph = graphs_Graph(5)
        first = graph.add_edge(0, 1)
        graph.add_edge(1, 2)
        second = graph.add_edge(0, 1)
        graph.add_edge(2, 2)
        self.assertTrue(graphs_has_undirected_cycle(graph))
        self.assertTrue(graph.delete_edge(first))
        self.assertTrue(graph.delete_edge(second))
        self.assertFalse(graph.delete_edge(second))
        self.assertEqual(graph.adjacency[0], [])
        distances, parents = graphs_breadth_first_search(graph, 1)
        self.assertEqual(distances, [None, 0, 1, None, None])
        self.assertEqual(graphs_reconstruct_path(parents, 1, 2), [1, 2])
        self.assertIsNone(graphs_reconstruct_path(parents, 1, 4))
        self.assertEqual(graphs_reconstruct_path(parents, 1, 1), [1])
        with self.assertRaises(ValueError):
            graphs_reconstruct_path([1, 0, None], 2, 0)
        directed = graphs_Graph(3, True)
        edge = directed.add_edge(0, 1)
        directed.add_edge(2, 0)
        self.assertTrue(directed.delete_edge(edge))
        self.assertEqual(directed.adjacency[2][0][0], 0)
        self.assertEqual(graphs_strongly_connected_components(directed), [[0], [1], [2]])

    def test_flow_signed_conservation(self):
        graph = graphs_Graph(4, True)
        edges = [(0, 1, 3), (0, 1, 2), (1, 0, 4), (1, 2, 4), (0, 2, 1), (2, 3, 5), (1, 3, 1)]
        capacities = [[0] * 4 for _ in range(4)]
        for u, v, capacity in edges:
            graph.add_edge(u, v, capacity)
            capacities[u][v] += capacity
        result = graphs_maximum_flow(graph, 0, 3)
        self.assertEqual(result.value, 6)
        for u in range(4):
            for v in range(4):
                self.assertEqual(result.flow[u][v], -result.flow[v][u])
                self.assertEqual(result.residual[u][v], capacities[u][v] - result.flow[u][v])
                self.assertGreaterEqual(result.residual[u][v], 0)
        self.assertEqual([sum(row) for row in result.flow], [6, 0, 0, -6])

    def test_dynamic_empty_and_elevator_oracle(self):
        self.assertEqual(dynamic_edit_distance("", "").operations, "")
        self.assertEqual(dynamic_subset_sum([], 0), [])
        self.assertIsNone(dynamic_subset_sum([], 1))
        destinations = [1, 2, 2, 4, 6]
        for budget in range(4):
            actual = dynamic_elevator_stops(destinations, budget, 6)
            expected = min(
                sum(min(abs(value - floor) for floor in (0, *stops)) for value in destinations)
                for count in range(budget + 1)
                for stops in itertools.combinations(range(1, 7), count)
            )
            self.assertEqual(actual["cost"], expected)
            self.assertLessEqual(len(actual["stops"]), budget)
            self.assertEqual(
                sum(
                    min(abs(value - floor) for floor in (0, *actual["stops"]))
                    for value in destinations
                ),
                expected,
            )

    def test_geometry_additional_primitives(self):
        horizontal = geometry_points_to_line((0, 1), (2, 1))
        reverse = geometry_points_to_line((2, 1), (0, 1))
        self.assertTrue(geometry_same_line(horizontal, reverse))
        self.assertTrue(geometry_parallel(horizontal, geometry_Line(0, 1, -4)))
        self.assertFalse(geometry_same_line(horizontal, geometry_Line(0, 1, -4)))
        self.assertTrue(geometry_same_line(geometry_point_and_slope_to_line((0, 1), 0), horizontal))
        self.assertEqual(geometry_closest_point((4, 7), horizontal), (4, 1))
        self.assertEqual(geometry_intersection(horizontal, geometry_Line(1, 0, -3)), (3, 1))
        self.assertIsNone(geometry_intersection(horizontal, reverse))
        self.assertEqual(geometry_orientation((0, 0), (1, 0), (0, 1)), 1)
        self.assertEqual(geometry_orientation((0, 0), (0, 1), (1, 0)), -1)
        self.assertAlmostEqual(geometry_triangle_area((0, 0), (2, 0), (0, 3)), 3)
        for row in range(-5, 6):
            for column in range(-5, 6):
                coordinates = geometry_array_to_hex(row, column)
                self.assertEqual(geometry_hex_to_array(*coordinates), (row, column))
                point = geometry_hex_to_cartesian(*coordinates, 1.5)
                actual = geometry_cartesian_to_hex(*point, 1.5)
                self.assertAlmostEqual(actual[0], coordinates[0])
                self.assertAlmostEqual(actual[1], coordinates[1])
        self.assertEqual(geometry_plates_on_top(0, 1, 8, 8, 1), 8)
        concave = [(0, 0), (3, 0), (3, 3), (1, 1), (0, 3)]
        for points in (concave, concave[::-1]):
            triangles = geometry_triangulate(points)
            self.assertEqual(len(triangles), len(points) - 2)
            self.assertAlmostEqual(
                sum(
                    geometry_triangle_area(*(points[i] for i in triangle)) for triangle in triangles
                ),
                geometry_polygon_area(points),
            )

    def test_geometry_rejects_invalid_tolerances_and_nonfinite_conversions(self):
        for tolerance in (-1, math.inf, math.nan):
            with self.assertRaises(ValueError):
                geometry_orientation((0, 0), (1, 0), (2, 0), tolerance)
        with self.assertRaises(ValueError):
            geometry_hex_to_cartesian(1e308, 1e308, 1)
        with self.assertRaises(ValueError):
            geometry_cartesian_to_hex(1e308, 1e308, 1e-308)

    def test_backtracking_undo_early_stop_and_exceptions(self):
        state = []
        solutions = []

        def make(prefix):
            state.append(prefix[-1])

        def unmake(prefix):
            self.assertEqual(state, prefix)
            state.pop()

        completed = search_backtrack(
            [],
            lambda prefix: len(prefix) == 3,
            lambda _: (0, 1),
            lambda prefix: solutions.append(list(prefix)) is None,
            make,
            unmake,
        )
        self.assertTrue(completed)
        self.assertEqual(len(solutions), 8)
        self.assertEqual(state, [])
        completed = search_backtrack(
            [], lambda prefix: len(prefix) == 3, lambda _: (0, 1), lambda _: False, make, unmake
        )
        self.assertFalse(completed)
        self.assertEqual(state, [])

        def fail(_):
            raise RuntimeError("test callback failure")

        with self.assertRaises(RuntimeError):
            search_backtrack(
                [], lambda prefix: len(prefix) == 3, lambda _: (0, 1), fail, make, unmake
            )
        self.assertEqual(state, [])

    def test_tsp_swap_and_exact_oracle(self):
        points = [(0, 0), (2, 3), (4, 1), (5, 4), (-1, 3)]
        tour = [0, 2, 1, 4, 3]
        original = search_tour_cost(points, tour)
        for first in range(len(tour)):
            for second in range(len(tour)):
                changed = list(tour)
                changed[first], changed[second] = (changed[second], changed[first])
                self.assertAlmostEqual(
                    search_swap_delta(points, tour, first, second),
                    search_tour_cost(points, changed) - original,
                )
        optimum = min(
            search_tour_cost(points, list(tour))
            for tour in itertools.permutations(range(len(points)))
        )
        for method in ("exact", "best"):
            self.assertAlmostEqual(search_traveling_salesperson(points, method)["cost"], optimum)
        for method in ("sample", "hill", "anneal"):
            first = search_traveling_salesperson(points, method, 27, 100)
            self.assertEqual(first, search_traveling_salesperson(points, method, 27, 100))
            self.assertAlmostEqual(first["cost"], search_tour_cost(points, first["tour"]))
            self.assertLessEqual(first["cost"], search_tour_cost(points, list(range(len(points)))))

    def test_repeated_tsp_and_sudoku_strategies(self):
        points = [(0, 0), (2, 3), (4, 1), (5, 4), (-1, 3)]
        for method in ("sample", "hill", "anneal"):
            candidates = []
            for run in range(4):
                initial = list(range(len(points)))
                if run:
                    initial = numeric_RandomSource(19 + run).permutation(initial)
                candidates.append(
                    search_traveling_salesperson(points, method, 19 + run, 40, initial)
                )
            actual = search_repeated_tsp(points, method, 19, 40, 4)
            self.assertEqual(actual["cost"], min(result["cost"] for result in candidates))
            self.assertEqual(actual, search_repeated_tsp(points, method, 19, 40, 4))
        with self.assertRaises(ValueError):
            search_repeated_tsp(points, runs=0)
        solved = "534678912672195348198342567859761423426853791713924856961537284287419635345286179"
        puzzle = "0" + solved[1:]
        for strategy in ("mrv", "row"):
            self.assertEqual(search_solve_sudoku(puzzle, strategy), solved)
        with self.assertRaises(ValueError):
            search_solve_sudoku(puzzle, "unknown")

    def test_demos_card_roundtrip(self):
        for card in range(52):
            self.assertEqual(demos_card_rank(demos_card_name(card)), card)
        self.assertEqual(demos_replace_names("a a", [("a", "aa")]), "aa aa")
        self.assertEqual(demos_war([4], [0], 10), {"winner": "a", "steps": 1})
        for method in ("row", "column", "snake", "diagonal"):
            actual = demos_grid_order(method, 3, 5)
            self.assertEqual(len(actual), 15)
            self.assertEqual(len({tuple(point) for point in actual}), 15)


class SourceLayout(unittest.TestCase):
    def test_each_original_source_has_a_counterpart(self):
        root = Path(__file__).resolve().parents[1]
        originals = {path.stem for path in (root / "c").glob("*.c")}
        self.assertEqual(len(originals), 66)
        self.assertEqual({path.stem for path in (root / "cpp").glob("*.cpp")}, originals)

        def java(name):
            return {"10055": "P10055", "8-queens": "EightQueens"}.get(
                name, "".join(part.capitalize() for part in name.replace("-", "_").split("_"))
            )

        def python(name):
            return {"10055": "p10055", "8-queens": "eight_queens"}.get(name, name.replace("-", "_"))

        self.assertEqual(
            {path.stem for path in (root / "java").glob("*.java")},
            {java(name) for name in originals},
        )
        self.assertEqual(
            {path.stem for path in (root / "python").glob("*.py")} - {"__init__"},
            {python(name) for name in originals},
        )
        self.assertTrue((root / "FIXES.md").is_file())


class Demonstrations(unittest.TestCase):
    def test_dijkstra_files_run_independently(self):
        root = Path(__file__).resolve().parents[1]
        data = "3 2\n1 2 2\n2 3 2\n"
        commands = (
            ([str(root / "c/dijkstra")], "Total SPST edgeweight"),
            ([str(root / "build/cpp/dijkstra")], "0 2 4"),
            (
                [os.environ.get("JAVA", "java"), "-cp", str(root / "build/java"), "Dijkstra"],
                "[0, 2, 4]",
            ),
            ([sys.executable, str(root / "python/dijkstra.py")], "[0, 2, 4]"),
        )
        for command, expected in commands:
            with self.subTest(program=command):
                result = subprocess.run(
                    command, input=data, capture_output=True, text=True, timeout=10, check=True
                )
                self.assertIn(expected, result.stdout)

    def test_ports_reject_negative_dijkstra_weights(self):
        root = Path(__file__).resolve().parents[1]
        commands = (
            [str(root / "build/cpp/dijkstra")],
            [os.environ.get("JAVA", "java"), "-cp", str(root / "build/java"), "Dijkstra"],
            [sys.executable, str(root / "python/dijkstra.py")],
        )
        for command in commands:
            with self.subTest(program=command):
                result = subprocess.run(
                    command,
                    input="2 1\n1 2 -1\n",
                    capture_output=True,
                    text=True,
                    timeout=10,
                    check=False,
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertTrue(result.stderr.strip())
