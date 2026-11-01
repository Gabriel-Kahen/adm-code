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

"""Backtracking and tour search; exponential algorithms have explicit practical limits."""

import heapq
import math
from collections.abc import Callable, Iterable
from typing import TypeVar

from .geometry import Point, distance
from .numeric import RandomSource

T = TypeVar("T")


def backtrack(
    prefix: list[T],
    is_solution: Callable[[list[T]], bool],
    candidates: Callable[[list[T]], Iterable[T]],
    process: Callable[[list[T]], bool],
    make_move: Callable[[list[T]], None] = lambda _: None,
    unmake_move: Callable[[list[T]], None] = lambda _: None,
) -> bool:
    """Generic DFS: process returns False to stop; every made move is undone.

    Callbacks see the current prefix including its latest move. The caller's
    prefix is copied. Undo runs even when recursive callbacks raise exceptions.
    Returns True on exhaustive completion and False on requested early stop.
    """
    current = list(prefix)

    def visit() -> bool:
        if is_solution(current):
            return process(current)
        for candidate in candidates(current):
            current.append(candidate)
            make_move(current)
            try:
                if not visit():
                    return False
            finally:
                unmake_move(current)
                current.pop()
        return True

    return visit()


def permutations(size: int) -> list[list[int]]:
    """All permutations of 0..n-1, O(n*n!) output; restricted to n<=9."""
    if not 0 <= size <= 9:
        raise ValueError("permutations require 0 <= n <= 9")
    result = []
    backtrack(
        [],
        lambda prefix: len(prefix) == size,
        lambda prefix: (value for value in range(size) if value not in prefix),
        lambda prefix: result.append(list(prefix)) is None,
    )
    return result


def subsets(size: int) -> list[list[int]]:
    """All subsets of 0..n-1 in lexicographic order; restricted to n<=20."""
    if not 0 <= size <= 20:
        raise ValueError("subsets require 0 <= n <= 20")
    result = []

    def visit(prefix: list[int], next_value: int) -> None:
        result.append(list(prefix))
        for value in range(next_value, size):
            prefix.append(value)
            visit(prefix, value + 1)
            prefix.pop()

    visit([], 0)
    return result


def queens(size: int) -> int:
    """Count n-queens solutions by bitmask backtracking; restricted to n<=15."""
    if not 0 <= size <= 15:
        raise ValueError("queens requires 0 <= n <= 15")
    full = (1 << size) - 1

    def count(columns: int, down: int, up: int) -> int:
        if columns == full:
            return 1
        available = full & ~(columns | down | up)
        result = 0
        while available:
            bit = available & -available
            available -= bit
            result += count(columns | bit, ((down | bit) << 1) & full, (up | bit) >> 1)
        return result

    return count(0, 0, 0)


def solve_sudoku(encoded: str, strategy: str = "mrv") -> str | None:
    """MRV or row-order backtracking; reject malformed or conflicting givens."""
    if strategy not in ("mrv", "row"):
        raise ValueError("unknown Sudoku strategy")
    if len(encoded) != 81 or any(character not in "0123456789" for character in encoded):
        raise ValueError("Sudoku must contain exactly 81 ASCII digits")
    board = [int(character) for character in encoded]
    rows, columns, boxes = [0] * 9, [0] * 9, [0] * 9
    empty = []
    for index, value in enumerate(board):
        row, column = divmod(index, 9)
        box = row // 3 * 3 + column // 3
        if value == 0:
            empty.append(index)
            continue
        bit = 1 << value
        if (rows[row] | columns[column] | boxes[box]) & bit:
            raise ValueError("conflicting Sudoku givens")
        rows[row] |= bit
        columns[column] |= bit
        boxes[box] |= bit

    def solve(position: int) -> bool:
        if position == len(empty):
            return True
        best, best_mask, best_count = position, 0, 10
        candidates = range(position, len(empty)) if strategy == "mrv" else (position,)
        for candidate in candidates:
            row, column = divmod(empty[candidate], 9)
            mask = 0x3FE & ~(rows[row] | columns[column] | boxes[row // 3 * 3 + column // 3])
            count = mask.bit_count()
            if count < best_count:
                best, best_mask, best_count = candidate, mask, count
        if best_count == 0:
            return False
        empty[position], empty[best] = empty[best], empty[position]
        index = empty[position]
        row, column = divmod(index, 9)
        box = row // 3 * 3 + column // 3
        mask = best_mask
        while mask:
            bit = mask & -mask
            mask -= bit
            board[index] = bit.bit_length() - 1
            rows[row] |= bit
            columns[column] |= bit
            boxes[box] |= bit
            if solve(position + 1):
                return True
            rows[row] ^= bit
            columns[column] ^= bit
            boxes[box] ^= bit
        board[index] = 0
        empty[position], empty[best] = empty[best], empty[position]
        return False

    return "".join(map(str, board)) if solve(0) else None


def tour_cost(points: list[Point], tour: list[int]) -> float:
    """Closed tour length; require each city exactly once. O(n)."""
    if sorted(tour) != list(range(len(points))):
        raise ValueError("tour must be a permutation of city indices")
    for point in points:
        distance(point, point)
    result = sum(
        distance(points[tour[index - 1]], points[tour[index]]) for index in range(len(tour))
    )
    if not math.isfinite(result):
        raise ValueError("tour cost exceeds floating-point range")
    return result


def swap_delta(points: list[Point], tour: list[int], first: int, second: int) -> float:
    """Recomputed swap-cost difference, O(n), including adjacent/cyclic edge cases."""
    if not 0 <= first < len(tour) or not 0 <= second < len(tour):
        raise ValueError("swap index out of range")
    previous = tour_cost(points, tour)
    changed = list(tour)
    changed[first], changed[second] = changed[second], changed[first]
    return tour_cost(points, changed) - previous


def _exact_tsp(points: list[Point], best_first: bool) -> dict:
    size = len(points)
    if size > 12:
        raise ValueError("exact TSP requires at most 12 cities")
    best_tour = list(range(size))
    best_cost = tour_cost(points, best_tour)
    if size < 2:
        return {"cost": best_cost, "tour": best_tour}
    costs = [[distance(first, second) for second in points] for first in points]

    def bound(cost: float, path: tuple[int, ...], remaining: tuple[int, ...]) -> float:
        # Each remaining vertex must supply one outgoing edge, as must path[-1].
        # Independent minima can only underestimate a legal completion.
        if not remaining:
            return cost + costs[path[-1]][0]
        return (
            cost
            + min(costs[path[-1]][vertex] for vertex in remaining)
            + sum(
                min(costs[vertex][other] for other in (*remaining, 0) if other != vertex)
                for vertex in remaining
            )
        )

    def visit(cost: float, path: tuple[int, ...], remaining: tuple[int, ...]) -> None:
        nonlocal best_cost, best_tour
        if not remaining:
            candidate = cost + costs[path[-1]][0]
            if candidate < best_cost:
                best_cost, best_tour = candidate, list(path)
            return
        if bound(cost, path, remaining) >= best_cost:
            return
        for vertex in remaining:
            visit(
                cost + costs[path[-1]][vertex],
                (*path, vertex),
                tuple(other for other in remaining if other != vertex),
            )

    remaining = tuple(range(1, size))
    if not best_first:
        visit(0.0, (0,), remaining)
    else:
        pending = [(bound(0.0, (0,), remaining), 0.0, (0,), remaining)]
        while pending:
            lower, cost, path, remaining = heapq.heappop(pending)
            if lower >= best_cost:
                continue
            if not remaining:
                best_cost, best_tour = lower, list(path)
                continue
            for vertex in remaining:
                extended = (*path, vertex)
                rest = tuple(other for other in remaining if other != vertex)
                candidate = cost + costs[path[-1]][vertex]
                lower = bound(candidate, extended, rest)
                if lower < best_cost:
                    if len(pending) >= 1_000_000:
                        raise ValueError("TSP best-first frontier exhausted")
                    heapq.heappush(pending, (lower, candidate, extended, rest))
    # Recompute through the public objective rather than returning a cached bound.
    return {"cost": tour_cost(points, best_tour), "tour": best_tour}


def traveling_salesperson(
    points: list[Point],
    method: str = "exact",
    seed: int = 0,
    iterations: int = 1000,
    initial_tour: list[int] | None = None,
) -> dict:
    """Exact DFS/best-first search or seeded sample/hill/anneal heuristics.

    Hill uses complete first-improvement swap sweeps (at most iterations sweeps),
    accepting strict full-objective decreases. Annealing returns its best visited
    tour, never the possibly worse final state. Heuristics do not prove optimality.
    """
    if iterations < 0:
        raise ValueError("negative iteration budget")
    if method in ("exact", "best"):
        return _exact_tsp(points, method == "best")
    if method not in ("sample", "hill", "anneal"):
        raise ValueError("unknown TSP method")
    tour = list(range(len(points))) if initial_tour is None else list(initial_tour)
    cost = tour_cost(points, tour)
    best_tour, best_cost = list(tour), cost
    if len(points) < 2:
        return {"cost": cost, "tour": tour}
    random = RandomSource(seed)
    if method == "sample":
        for _ in range(iterations):
            candidate = random.permutation(tour)
            candidate_cost = tour_cost(points, candidate)
            if candidate_cost < best_cost:
                best_tour, best_cost = candidate, candidate_cost
    elif method == "hill":
        for _ in range(iterations):
            improved = False
            for first in range(len(tour)):
                for second in range(first + 1, len(tour)):
                    candidate = list(tour)
                    candidate[first], candidate[second] = candidate[second], candidate[first]
                    candidate_cost = tour_cost(points, candidate)
                    if candidate_cost < cost:
                        tour, cost = candidate, candidate_cost
                        improved = True
                        break
                if improved:
                    break
            if not improved:
                break
        best_tour, best_cost = tour, cost
    else:
        scale = max(cost / len(tour), 1e-9)
        for step in range(iterations):
            first = random.integer(0, len(tour) - 1)
            second = random.integer(0, len(tour) - 1)
            candidate = list(tour)
            candidate[first], candidate[second] = candidate[second], candidate[first]
            candidate_cost = tour_cost(points, candidate)
            temperature = scale * max(1e-9, 1 - step / max(1, iterations))
            delta = candidate_cost - cost
            if delta <= 0 or random.real(0, 1) < math.exp(-delta / temperature):
                tour, cost = candidate, candidate_cost
            if cost < best_cost:
                best_tour, best_cost = list(tour), cost
    return {"cost": best_cost, "tour": best_tour}


def repeated_tsp(
    points: list[Point],
    method: str = "hill",
    seed: int = 0,
    iterations: int = 1000,
    runs: int = 10,
) -> dict:
    """Best of independent heuristic runs: identity first, then seeded random starts.

    The single-run iteration budget applies to each restart. Returned city indices
    always refer to the original points. Runtime is runs times the chosen method.
    """
    if runs <= 0 or method not in ("sample", "hill", "anneal"):
        raise ValueError("positive restart count and heuristic TSP method required")
    best = None
    for run in range(runs):
        initial = list(range(len(points)))
        if run:
            initial = RandomSource(seed + run).permutation(initial)
        candidate = traveling_salesperson(points, method, seed + run, iterations, initial)
        if best is None or candidate["cost"] < best["cost"]:
            best = candidate
    return best
