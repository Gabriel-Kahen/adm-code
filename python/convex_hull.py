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
# or http://www.amazon.com/exec/obidos/ASIN/0387001638/thealgorithmrepo/

"""Direct translation of convex-hull.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from functools import cmp_to_key

from ._c import address, scanf
from . import geometry

TRUE = 1
FALSE = 0
# first_point: first hull point
first_point = [0.0 for _ in range(geometry.DIMENSION)]


def sort_and_remove_duplicates(in_, n):
    # i: counter
    # input_count: number of points before deletion
    # unique_count: index marked for potential deletion
    in_[:n[0]] = sorted(in_[:n[0]], key=cmp_to_key(leftlower))
    input_count = n[0]
    # in[0..unique_count-1] is the compacted distinct prefix.
    unique_count = 1
    i = 1
    while (i < input_count):
        if ((in_[(unique_count - 1)][geometry.X] == in_[i][geometry.X]) and (in_[(unique_count - 1)][geometry.Y] == in_[i][geometry.Y])):
            n[0] -= 1
        else:
            geometry.copy_point(in_[i], in_[unique_count])
            unique_count = (unique_count + 1)
        i += 1


def convex_hull(in_, n, hull):
    n = [n]
    # i: input counter
    # top: current hull size
    if (n[0] <= 0):
        hull.n = 0
        return
    sort_and_remove_duplicates(in_, n)
    # A collinear hull is a segment, not a closed scan with a sentinel.
    i = 1
    while ((i + 1) < n[0]):
        if (not geometry.collinear(in_[0], in_[(n[0] - 1)], in_[i])):
            break
        i += 1
    if ((n[0] <= 2) or ((i + 1) == n[0])):
        geometry.copy_point(in_[0], hull.p[0])
        hull.n = 1
        if (n[0] > 1):
            geometry.copy_point(in_[(n[0] - 1)], hull.p[1])
            hull.n = 2
        return
    geometry.copy_point(in_[0], first_point)
    in_[1:n[0]] = sorted(in_[1:n[0]], key=cmp_to_key(smaller_angle))
    geometry.copy_point(first_point, hull.p[0])
    geometry.copy_point(in_[1], hull.p[1])
    top = 1
    i = 2
    while (i < n[0]):
        if geometry.cw(hull.p[(top - 1)], hull.p[top], in_[i]):
            # top not on hull
            top = (top - 1)
        else:
            if (not geometry.collinear(hull.p[(top - 1)], hull.p[top], in_[i])):
                top = (top + 1)
            geometry.copy_point(in_[i], hull.p[top])
            i = (i + 1)
    hull.n = (top + 1)


def leftlower(left, right):
    p1 = left
    p2 = right
    if (p1[geometry.X] < p2[geometry.X]):
        return (-1)
    if (p1[geometry.X] > p2[geometry.X]):
        return 1
    if (p1[geometry.Y] < p2[geometry.Y]):
        return (-1)
    if (p1[geometry.Y] > p2[geometry.Y]):
        return 1
    return 0


def smaller_angle(left, right):
    # The legacy geometry predicates accept mutable pointers but only read them.
    p1 = left
    p2 = right
    if geometry.collinear(first_point, p1, p2):
        if (geometry.distance(first_point, p1) <= geometry.distance(first_point, p2)):
            return (-1)
        else:
            return 1
    if geometry.ccw(first_point, p1, p2):
        return (-1)
    else:
        return 1


def main():
    # in: input points
    in_ = [[0.0 for _ in range(geometry.DIMENSION)] for _ in range(geometry.MAXPOLY)]
    # hull: convex hull
    hull = geometry.polygon()
    # n: number of points
    n = [0]
    # i: counter
    scanf("%d", n)
    i = 0
    while (i < n[0]):
        scanf("%lf %lf", address(in_[i], geometry.X), address(in_[i], geometry.Y))
        i += 1
    convex_hull(in_, n[0], hull)
    geometry.print_polygon(hull)


if __name__ == "__main__":
    raise SystemExit(main())
