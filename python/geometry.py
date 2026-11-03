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

"""geometry.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"

import math
from dataclasses import dataclass

EPSILON = 1e-9

Point = tuple[float, float]


def _finite(*values: float) -> None:
    if not all(math.isfinite(value) for value in values):
        raise ValueError("geometry requires finite coordinates")


def _points(points: list[Point]) -> None:
    for point in points:
        _finite(*point)


def distance(first: Point, second: Point) -> float:
    _points([first, second])
    result = math.hypot(first[0] - second[0], first[1] - second[1])
    if not math.isfinite(result):
        raise ValueError("distance exceeds floating-point range")
    return result


def cross(first: Point, second: Point, third: Point) -> float:
    """Twice the signed area; positive means counterclockwise."""
    _points([first, second, third])
    value = (second[0] - first[0]) * (third[1] - first[1]) - (second[1] - first[1]) * (
        third[0] - first[0]
    )
    if not math.isfinite(value):
        raise ValueError("orientation exceeds floating-point range")
    return value


def orientation(first: Point, second: Point, third: Point, epsilon: float = EPSILON) -> int:
    if not math.isfinite(epsilon) or epsilon < 0:
        raise ValueError("orientation tolerance must be finite and nonnegative")
    value = cross(first, second, third)
    return 1 if value > epsilon else -1 if value < -epsilon else 0


def signed_triangle_area(first: Point, second: Point, third: Point) -> float:
    return cross(first, second, third) / 2


def triangle_area(first: Point, second: Point, third: Point) -> float:
    return abs(signed_triangle_area(first, second, third))


@dataclass(frozen=True)
class Line:
    """Normalized ax+by+c=0 with canonical coefficient sign."""

    a: float
    b: float
    c: float

    def __post_init__(self) -> None:
        _finite(self.a, self.b, self.c)
        norm = math.hypot(self.a, self.b)
        if norm == 0 or not math.isfinite(norm):
            raise ValueError("invalid line normal")
        sign = -1 if self.a < 0 or (self.a == 0 and self.b < 0) else 1
        object.__setattr__(self, "a", sign * self.a / norm)
        object.__setattr__(self, "b", sign * self.b / norm)
        object.__setattr__(self, "c", sign * self.c / norm)
        _finite(self.a, self.b, self.c)


def points_to_line(first: Point, second: Point) -> Line:
    _points([first, second])
    if first == second:
        raise ValueError("two distinct points required")
    a, b = first[1] - second[1], second[0] - first[0]
    return Line(a, b, -(a * first[0] + b * first[1]))


def point_and_slope_to_line(point: Point, slope: float) -> Line:
    _finite(*point, slope)
    return Line(slope, -1, point[1] - slope * point[0])


def parallel(first: Line, second: Line) -> bool:
    return abs(first.a * second.b - second.a * first.b) <= EPSILON


def same_line(first: Line, second: Line) -> bool:
    return parallel(first, second) and abs(first.c - second.c) <= EPSILON


def intersection(first: Line, second: Line) -> Point | None:
    """Unique intersection, or None for parallel/coincident lines."""
    determinant = first.a * second.b - second.a * first.b
    if abs(determinant) <= EPSILON:
        return None
    result = (
        (first.b * second.c - second.b * first.c) / determinant,
        (first.c * second.a - second.c * first.a) / determinant,
    )
    _finite(*result)
    return result


def closest_point(point: Point, line: Line) -> Point:
    _points([point])
    signed_distance = line.a * point[0] + line.b * point[1] + line.c
    result = point[0] - signed_distance * line.a, point[1] - signed_distance * line.b
    _finite(*result)
    return result


def point_in_box(point: Point, first: Point, second: Point) -> bool:
    _points([point, first, second])
    return all(
        min(a, b) - EPSILON <= value <= max(a, b) + EPSILON
        for value, a, b in zip(point, first, second)
    )


def segments_intersect(first: Point, second: Point, third: Point, fourth: Point) -> bool:
    """Closed-segment intersection, including point segments and overlap."""
    signs = (
        orientation(first, second, third),
        orientation(first, second, fourth),
        orientation(third, fourth, first),
        orientation(third, fourth, second),
    )
    if signs[0] * signs[1] < 0 and signs[2] * signs[3] < 0:
        return True
    return (
        (signs[0] == 0 and point_in_box(third, first, second))
        or (signs[1] == 0 and point_in_box(fourth, first, second))
        or (signs[2] == 0 and point_in_box(first, third, fourth))
        or (signs[3] == 0 and point_in_box(second, third, fourth))
    )


def signed_polygon_area(points: list[Point]) -> float:
    _points(points)
    if len(points) < 3:
        return 0.0
    # Translate to reduce cancellation when coordinates have a large common offset.
    result = (
        sum(
            cross(points[0], points[index], points[index + 1])
            for index in range(1, len(points) - 1)
        )
        / 2
    )
    _finite(result)
    return result


def polygon_area(points: list[Point]) -> float:
    return abs(signed_polygon_area(points))
