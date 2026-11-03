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

"""superman.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"

import math

from .geometry import (
    EPSILON,
    Point,
    _finite,
    _points,
    closest_point,
    distance,
    point_in_box,
    points_to_line,
)


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


if __name__ == "__main__":
    import sys

    print(superman((-3, 0), (3, 0), [(0, 0, 1)]))
