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

"""convex-hull.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"

from .geometry import Point, _points, orientation


def convex_hull(points: list[Point]) -> list[Point]:
    """Monotone-chain hull, O(n log n); retain only endpoints of collinear edges."""
    _points(points)
    unique = sorted(set(points))
    if len(unique) < 2:
        return unique
    lower = []
    for point in unique:
        while len(lower) >= 2 and orientation(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    upper = []
    for point in reversed(unique):
        while len(upper) >= 2 and orientation(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    return lower[:-1] + upper[:-1]


if __name__ == "__main__":
    import sys

    values = list(map(float, sys.stdin.read().split()))
    points = (
        [(0, 0), (1, 0), (1, 1), (0, 1)] if not values else list(zip(values[1::2], values[2::2]))
    )
    if values and int(values[0]) != len(points):
        raise ValueError("incorrect point count")
    print(convex_hull(points))
