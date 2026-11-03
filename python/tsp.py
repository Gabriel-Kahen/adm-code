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

"""tsp.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"

import math

from .geometry import Point, distance


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


if __name__ == "__main__":
    import sys

    from .annealing import traveling_salesperson

    print(traveling_salesperson([(0, 0), (1, 0), (1, 1), (0, 1)], "hill"))
