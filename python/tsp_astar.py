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

"""tsp-astar.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"

from .geometry import Point, distance
from .tsp import tour_cost
from .tsp_pq import TourQueue


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
        pending = TourQueue()
        pending.push(bound(0.0, (0,), remaining), (0.0, (0,), remaining))
        while pending:
            lower, (cost, path, remaining) = pending.pop()
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
                    pending.push(lower, (candidate, extended, rest))
    # Recompute through the public objective rather than returning a cached bound.
    return {"cost": tour_cost(points, best_tour), "tour": best_tour}


if __name__ == "__main__":
    import sys

    print(_exact_tsp([(0, 0), (1, 0), (1, 1), (0, 1)], True))
