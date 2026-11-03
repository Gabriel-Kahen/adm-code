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

"""triangulate.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"

from .geometry import (
    EPSILON,
    Point,
    _points,
    cross,
    distance,
    orientation,
    point_in_box,
    polygon_area,
    segments_intersect,
    signed_polygon_area,
    triangle_area,
)


def validate_polygon(points: list[Point]) -> None:
    """Require a simple boundary, distinct vertices, and nonzero signed area; O(n²)."""
    _points(points)
    if len(points) < 3 or len(set(points)) != len(points) or polygon_area(points) <= EPSILON:
        raise ValueError("polygon is degenerate")
    size = len(points)
    for first in range(size):
        for second in range(first + 1, size):
            if second == first + 1 or (first == 0 and second == size - 1):
                continue
            if segments_intersect(
                points[first],
                points[(first + 1) % size],
                points[second],
                points[(second + 1) % size],
            ):
                raise ValueError("polygon boundary intersects itself")
    for index in range(size):
        previous, current, following = points[index - 1], points[index], points[(index + 1) % size]
        if orientation(previous, current, following) == 0 and not point_in_box(
            current, previous, following
        ):
            raise ValueError("adjacent polygon edges overlap")


def triangulate(points: list[Point]) -> list[list[int]]:
    """Ear clipping of a simple polygon, either winding; O(n³), n-2 index triangles."""
    validate_polygon(points)
    remaining = list(range(len(points)))
    if signed_polygon_area(points) < 0:
        remaining.reverse()
    result = []
    while len(remaining) > 3:
        for position, current in enumerate(remaining):
            previous = remaining[position - 1]
            following = remaining[(position + 1) % len(remaining)]
            a, b, c = points[previous], points[current], points[following]
            if orientation(a, b, c) <= 0:
                continue
            occupied = False
            for other in remaining:
                if other in (previous, current, following):
                    continue
                point = points[other]
                if min(cross(a, b, point), cross(b, c, point), cross(c, a, point)) >= -EPSILON:
                    occupied = True
                    break
            if not occupied:
                result.append([previous, current, following])
                remaining.pop(position)
                break
        else:
            raise ValueError("polygon cannot be triangulated at this tolerance")
    if triangle_area(*(points[index] for index in remaining)) <= EPSILON:
        raise ValueError("degenerate final triangle")
    result.append(remaining)
    return result


def minimum_weight_triangulation(points: list[Point]) -> float:
    """Minimum sum of triangle perimeters for a strictly convex polygon, O(n³)."""
    validate_polygon(points)
    signs = [
        orientation(points[index - 1], points[index], points[(index + 1) % len(points)])
        for index in range(len(points))
    ]
    if 0 in signs or len(set(signs)) != 1:
        raise ValueError("minimum-weight triangulation requires strict convexity")
    size = len(points)
    costs = [[0.0] * size for _ in range(size)]
    for gap in range(2, size):
        for first in range(size - gap):
            last = first + gap
            costs[first][last] = min(
                costs[first][middle]
                + costs[middle][last]
                + distance(points[first], points[middle])
                + distance(points[middle], points[last])
                + distance(points[last], points[first])
                for middle in range(first + 1, last)
            )
    return costs[0][-1]


if __name__ == "__main__":
    import sys

    print(triangulate([(0, 0), (1, 0), (1, 1), (0, 1)]))
