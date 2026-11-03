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

"""annealing.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"

import math

from .geometry import Point
from .random import RandomSource
from .tsp import tour_cost
from .tsp_astar import _exact_tsp


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
