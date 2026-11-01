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

"""Planar geometry with absolute 1e-9 predicates; finite, moderately scaled inputs.

Floating-point tolerance is a model choice, not an exact-arithmetic guarantee.
Algorithms reject invalid polygon domains rather than iterating indefinitely.
"""

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


def _packing_dimensions(width: float, height: float, radius: float) -> None:
    _finite(width, height, radius)
    if width <= 0 or height <= 0 or radius <= 0:
        raise ValueError("packing dimensions and radius must be positive")


def dense_layers(width: float, height: float, radius: float) -> int:
    _packing_dimensions(width, height, radius)
    if width < 2 * radius or height < 2 * radius:
        return 0
    return 1 + math.floor((height - 2 * radius) / (math.sqrt(3) * radius))


def plates_per_row(row: int, width: float, radius: float) -> int:
    _finite(width, radius)
    if row < 0 or width <= 0 or radius <= 0:
        raise ValueError("invalid packing row")
    full = math.floor(width / (2 * radius))
    if full == 0:
        return 0
    return full if row % 2 == 0 or width / (2 * radius) - full >= 0.5 else full - 1


def grid_plates(width: float, height: float, radius: float) -> int:
    _packing_dimensions(width, height, radius)
    return math.floor(height / (2 * radius)) * plates_per_row(0, width, radius)


def dense_plates(width: float, height: float, radius: float) -> int:
    layers = dense_layers(width, height, radius)
    return (layers + 1) // 2 * plates_per_row(0, width, radius) + layers // 2 * plates_per_row(
        1, width, radius
    )


def packing(width: float, height: float, radius: float) -> tuple[int, int]:
    """Best row-based grid and triangular-lattice counts across both box orientations."""
    return max(grid_plates(width, height, radius), grid_plates(height, width, radius)), max(
        dense_plates(width, height, radius), dense_plates(height, width, radius)
    )


def hex_to_cartesian(row: float, diagonal: float, radius: float) -> Point:
    _finite(row, diagonal, radius)
    if radius <= 0:
        raise ValueError("radius must be positive")
    result = radius * row + 2 * radius * diagonal, math.sqrt(3) * radius * row
    _finite(*result)
    return result


def cartesian_to_hex(x: float, y: float, radius: float) -> Point:
    _finite(x, y, radius)
    if radius <= 0:
        raise ValueError("radius must be positive")
    row = y / (math.sqrt(3) * radius)
    result = row, (x - radius * row) / (2 * radius)
    _finite(*result)
    return result


def array_to_hex(row: int, column: int) -> tuple[int, int]:
    return row, column - row // 2


def hex_to_array(row: int, diagonal: int) -> tuple[int, int]:
    return row, diagonal + row // 2


def plates_on_top(row: int, diagonal: int, width: float, height: float, radius: float) -> int:
    """Count the triangular dependency cone above one plate in a fixed packing."""
    layers = dense_layers(width, height, radius)
    _, column = hex_to_array(row, diagonal)
    if not 0 <= row < layers or not 0 <= column < plates_per_row(row, width, radius):
        raise ValueError("plate lies outside packing")
    result = 0
    for higher in range(row + 1, layers):
        left = max(0, hex_to_array(higher, diagonal - (higher - row))[1])
        right = min(plates_per_row(higher, width, radius) - 1, hex_to_array(higher, diagonal)[1])
        result += max(0, right - left + 1)
    return result


def superman(
    start: Point, target: Point, circles: list[tuple[float, float, float]]
) -> tuple[float, float]:
    """Original chord/arc detour model, not a general shortest-path solver; O(n²).

    Circles must be disjoint, positive-radius, and both segment endpoints outside.
    This model replaces each crossed chord by its shorter circular arc.
    """
    _points([start, target])
    for index, (x, y, radius) in enumerate(circles):
        _finite(x, y, radius)
        if radius <= 0 or min(distance(start, (x, y)), distance(target, (x, y))) < radius - EPSILON:
            raise ValueError("circle radius must be positive and endpoints outside")
        for other_x, other_y, other_radius in circles[:index]:
            if distance((x, y), (other_x, other_y)) < radius + other_radius - EPSILON:
                raise ValueError("overlapping circles are outside the model")
    direct = distance(start, target)
    if direct == 0:
        return 0.0, 0.0
    line = points_to_line(start, target)
    through, around = 0.0, 0.0
    for x, y, radius in circles:
        foot = closest_point((x, y), line)
        separation = distance(foot, (x, y))
        if separation < radius and point_in_box(foot, start, target):
            through += 2 * math.sqrt(max(0, radius * radius - separation * separation))
            around += 2 * radius * math.acos(min(1.0, separation / radius))
    return through, direct - through + around
