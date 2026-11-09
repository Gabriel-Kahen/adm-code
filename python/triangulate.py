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

"""Direct translation of triangulate.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import address, printf, scanf
from . import geometry


def add_triangle(t, i, j, k, p):
    # n: number of triangles in t
    n = t.n
    t.t[n][0] = i
    t.t[n][1] = j
    t.t[n][2] = k
    t.n = (n + 1)


def point_in_triangle(p, t):
    # i: counter
    i = 0
    while (i < 3):
        if geometry.cw(t[i], t[(i + 1) % 3], p):
            return False
        i += 1
    return True


def ear_Q(i, j, k, p):
    # t: coordinates for points i,j,k
    t = [[0.0 for _ in range(geometry.DIMENSION)] for _ in range(3)]
    # m: counter
    geometry.copy_point(p.p[i], t[0])
    geometry.copy_point(p.p[j], t[1])
    geometry.copy_point(p.p[k], t[2])
    if geometry.cw(t[0], t[1], t[2]):
        return False
    m = 0
    while (m < p.n):
        if (((m != i) and (m != j)) and (m != k)):
            if point_in_triangle(p.p[m], t):
                return False
        m += 1
    return True


def triangulate(p, t):
    # l: left/right neighbor indices
    l = [0 for _ in range(geometry.MAXPOLY)]
    r = [0 for _ in range(geometry.MAXPOLY)]
    # i: counter
    # initialization
    i = 0
    while (i < p.n):
        l[i] = (i - 1 + p.n) % p.n
        r[i] = (i + 1 + p.n) % p.n
        i += 1
    t.n = 0
    i = (p.n - 1)
    while (t.n < (p.n - 2)):
        i = r[i]
        if ear_Q(l[i], i, r[i], p):
            add_triangle(t, l[i], i, r[i], p)
            l[r[i]] = l[i]
            r[l[i]] = r[i]


def area_triangulation(p):
    # t: output triangulation
    t = geometry.triangulation()
    # total area so far
    total = 0.0
    # i: counter
    triangulate(p, t)
    i = 0
    while (i < t.n):
        total += geometry.triangle_area(p.p[t.t[i][0]], p.p[t.t[i][1]], p.p[t.t[i][2]])
        i += 1
    return total


def area(p):
    # total area so far
    total = 0.0
    # j: counters
    i = 0
    while (i < p.n):
        j = (i + 1) % p.n
        total += ((p.p[i][geometry.X] * p.p[j][geometry.Y]) - (p.p[j][geometry.X] * p.p[i][geometry.Y]))
        i += 1
    return (total / 2.0)


def main():
    # p: input polygon
    p = geometry.polygon()
    # i: counter
    scanf("%d", address(p, 'n'))
    i = 0
    while (i < p.n):
        scanf("%lf %lf", address(p.p[i], geometry.X), address(p.p[i], geometry.Y))
        i += 1
    printf(" area via triangulation = %f\n", area_triangulation(p))
    printf(" area slick = %f\n", area(p))
    return 0


def print_triangulation(t):
    # j: counters
    i = 0
    while (i < t.n):
        j = 0
        while (j < 3):
            printf(" %d ", t.t[i][j])
            j += 1
        printf("\n")
        i += 1


if __name__ == "__main__":
    raise SystemExit(main())
