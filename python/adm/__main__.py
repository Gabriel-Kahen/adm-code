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

"""Shared argv-to-JSON interface. Import the modules directly for richer APIs."""

import json
import math
import re
import sys
from dataclasses import asdict

from . import demos, dynamic, geometry, graphs, numeric, search, sorting


class Tokens:
    def __init__(self, arguments: list[str]) -> None:
        self.values = arguments
        self.position = 0

    def text(self) -> str:
        if self.position == len(self.values):
            raise ValueError("missing argument")
        value = self.values[self.position]
        self.position += 1
        return value

    def integer(self) -> int:
        value = self.text()
        if re.fullmatch(r"[+-]?[0-9]+", value) is None:
            raise ValueError("expected decimal integer")
        return int(value)

    def nonnegative(self) -> int:
        value = self.integer()
        if value < 0:
            raise ValueError("expected nonnegative integer")
        return value

    def real(self) -> float:
        value = float(self.text())
        if not math.isfinite(value):
            raise ValueError("expected finite real number")
        return value

    def point(self) -> geometry.Point:
        return self.real(), self.real()

    def points(self) -> list[geometry.Point]:
        return [self.point() for _ in range(self.nonnegative())]

    def integers(self) -> list[int]:
        return [self.integer() for _ in range(len(self.values) - self.position)]

    def graph(self) -> graphs.Graph:
        size, directed, count = self.nonnegative(), self.integer(), self.nonnegative()
        if directed not in (0, 1):
            raise ValueError("directed flag must be 0 or 1")
        graph = graphs.Graph(size, bool(directed))
        for _ in range(count):
            graph.add_edge(self.integer(), self.integer(), self.integer())
        return graph

    def done(self) -> None:
        if self.position != len(self.values):
            raise ValueError("unexpected extra argument")


def evaluate(operation: str, tokens: Tokens):
    if operation == "selftest":
        from .selftest import run

        tokens.done()
        return run()
    if operation == "sort":
        method = tokens.text()
        if method not in sorting.SORTS:
            raise ValueError("unknown sort method")
        return sorting.SORTS[method](tokens.integers())
    if operation in ("binary", "insert"):
        target, values = tokens.integer(), tokens.integers()
        if any(a > b for a, b in zip(values, values[1:])):
            raise ValueError("input array must be sorted")
        return (
            sorting.binary_search(values, target)
            if operation == "binary"
            else sorting.sentinel_insert(values, target)
        )
    if operation == "absdiff":
        return str(numeric.absolute_difference(tokens.integer(), tokens.integer()))
    if operation == "bigint":
        return str(numeric.big_integer(tokens.text(), tokens.integer(), tokens.integer()))
    if operation == "fib":
        method = tokens.text()
        return str(numeric.fibonacci(tokens.integer(), method))
    if operation == "binomial":
        return str(numeric.binomial(tokens.integer(), tokens.integer()))
    if operation == "gcd":
        return numeric.extended_gcd(tokens.integer(), tokens.integer())
    if operation == "factors":
        return numeric.prime_factors(tokens.integer())
    if operation == "distance":
        dimension = tokens.nonnegative()
        return numeric.euclidean_distance(
            [tokens.real() for _ in range(dimension)], [tokens.real() for _ in range(dimension)]
        )
    if operation == "matrix":
        rows, inner, columns = tokens.nonnegative(), tokens.nonnegative(), tokens.nonnegative()
        if min(rows, inner, columns) == 0:
            raise ValueError("matrices require positive dimensions")
        first = [[tokens.integer() for _ in range(inner)] for _ in range(rows)]
        second = [[tokens.integer() for _ in range(columns)] for _ in range(inner)]
        return numeric.matrix_multiply(first, second)
    if operation == "convolve":
        n, m = tokens.nonnegative(), tokens.nonnegative()
        return numeric.convolve(
            [tokens.integer() for _ in range(n)], [tokens.integer() for _ in range(m)]
        )
    if operation in ("edit", "editbrute", "lcs", "substring"):
        first, second = tokens.text(), tokens.text()
        functions = {
            "edit": dynamic.edit_distance,
            "editbrute": dynamic.edit_distance_brute,
            "lcs": dynamic.longest_common_subsequence,
            "substring": dynamic.substring_edit_distance,
        }
        result = functions[operation](first, second)
        return asdict(result) if operation == "edit" else result
    if operation == "partition":
        count = tokens.integer()
        return dynamic.linear_partition(tokens.integers(), count)
    if operation == "subsetsum":
        target = tokens.integer()
        return dynamic.subset_sum(tokens.integers(), target)
    if operation == "elevator":
        budget, floor = tokens.integer(), tokens.integer()
        return dynamic.elevator_stops(tokens.integers(), budget, floor)
    if operation in {
        "bfs",
        "dfs",
        "components",
        "scc",
        "bipartite",
        "cycle",
        "articulation",
        "topo",
        "mst",
        "dijkstra",
        "floyd",
        "maxflow",
        "paths",
        "edgecount",
    }:
        method = tokens.text() if operation in {"scc", "topo", "mst"} else ""
        graph = tokens.graph()
        if operation == "bfs":
            return graphs.breadth_first_search(graph, tokens.integer())[0]
        if operation == "dfs":
            return graphs.depth_first_search(graph, tokens.integer())
        if operation == "components":
            return graphs.connected_components(graph)
        if operation == "scc":
            return graphs.strongly_connected_components(graph, method)
        if operation == "bipartite":
            return graphs.bipartite_coloring(graph) is not None
        if operation == "cycle":
            return graphs.has_undirected_cycle(graph)
        if operation == "articulation":
            return graphs.articulation_points(graph)
        if operation == "topo":
            return graphs.topological_sort(graph, method)
        if operation == "mst":
            return graphs.minimum_spanning_forest(graph, method)
        if operation == "dijkstra":
            return graphs.dijkstra(graph, tokens.integer())[0]
        if operation == "floyd":
            return graphs.floyd_warshall(graph)
        if operation == "maxflow":
            return graphs.maximum_flow(graph, tokens.integer(), tokens.integer()).value
        if operation == "paths":
            return graphs.simple_paths(graph, tokens.integer(), tokens.integer())
        return len(graph.edges)
    if operation in ("hull", "area", "triangulate", "mwt"):
        functions = {
            "hull": geometry.convex_hull,
            "area": geometry.polygon_area,
            "triangulate": geometry.triangulate,
            "mwt": geometry.minimum_weight_triangulation,
        }
        return functions[operation](tokens.points())
    if operation == "segment":
        return geometry.segments_intersect(
            tokens.point(), tokens.point(), tokens.point(), tokens.point()
        )
    if operation == "project":
        point, first, second = tokens.point(), tokens.point(), tokens.point()
        return geometry.closest_point(point, geometry.points_to_line(first, second))
    if operation == "intersection":
        first, second, third, fourth = (
            tokens.point(),
            tokens.point(),
            tokens.point(),
            tokens.point(),
        )
        return geometry.intersection(
            geometry.points_to_line(first, second), geometry.points_to_line(third, fourth)
        )
    if operation == "packing":
        return geometry.packing(tokens.real(), tokens.real(), tokens.real())
    if operation == "superman":
        first, second = tokens.point(), tokens.point()
        circles = [
            (tokens.real(), tokens.real(), tokens.real()) for _ in range(tokens.nonnegative())
        ]
        return geometry.superman(first, second, circles)
    if operation in ("queens", "permutations", "subsets"):
        return {
            "queens": search.queens,
            "permutations": search.permutations,
            "subsets": search.subsets,
        }[operation](tokens.integer())
    if operation == "sudoku":
        return search.solve_sudoku(tokens.text())
    if operation == "tsp":
        method, points = tokens.text(), tokens.points()
        seed, iterations = (
            (tokens.integer(), tokens.integer())
            if method in {"sample", "hill", "anneal"}
            else (0, 1000)
        )
        return search.traveling_salesperson(points, method, seed, iterations)
    if operation == "grid":
        return demos.grid_order(tokens.text(), tokens.integer(), tokens.integer())
    if operation == "find":
        return demos.find_match(tokens.text(), tokens.text())
    if operation == "replace":
        text = tokens.text()
        changes = [(tokens.text(), tokens.text()) for _ in range(tokens.nonnegative())]
        return demos.replace_names(text, changes)
    if operation == "suitors":
        people = [
            demos.Suitor(tokens.text(), tokens.text(), tokens.integer(), tokens.integer())
            for _ in range(tokens.nonnegative())
        ]
        return [[person.first, person.last] for person in demos.rank_suitors(people)]
    if operation == "card":
        return demos.card_rank(tokens.text())
    if operation == "uncard":
        return demos.card_name(tokens.integer())
    if operation == "war":
        limit, n, m = tokens.integer(), tokens.nonnegative(), tokens.nonnegative()
        return demos.war(
            [tokens.integer() for _ in range(n)], [tokens.integer() for _ in range(m)], limit
        )
    raise ValueError("unknown operation: " + operation)


def main(arguments: list[str] | None = None) -> int:
    arguments = sys.argv[1:] if arguments is None else arguments
    try:
        if not arguments:
            raise ValueError("usage: python -m adm OPERATION ARGUMENTS...")
        tokens = Tokens(arguments[1:])
        result = evaluate(arguments[0], tokens)
        tokens.done()
        print(json.dumps(result, ensure_ascii=True, allow_nan=False))
        return 0
    except (ValueError, IndexError, OverflowError, RecursionError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
