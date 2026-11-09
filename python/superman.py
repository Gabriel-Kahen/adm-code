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

"""Direct translation of superman.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import *
from . import _c
from . import geometry

# maximum number of circles
MAXN = 100
# s: Superman's initial position
s = [0.0 for _ in range(geometry.DIMENSION)]
# t: target position
t = [0.0 for _ in range(geometry.DIMENSION)]
# ncircles: number of circles
ncircles = 0
# c: circles data structure
c = [geometry.circle() for _ in range((MAXN + 1))]


def superman():
    # l: line from start to target position
    l = geometry.line()
    # close: closest point
    close = [0.0 for _ in range(geometry.DIMENSION)]
    # d: distance from circle-center
    # length of intersection with circles
    xray = 0.0
    # length around circular arcs
    around = 0.0
    # angle: angle subtended by arc
    # travel: total travel distance
    # i: counter
    geometry.points_to_line(s, t, l)
    i = 1
    while (i <= ncircles):
        geometry.closest_point(c[i].c, l, close)
        d = geometry.distance(c[i].c, close)
        if (((d >= 0) and (d < c[i].r)) and geometry.point_in_box(close, s, t)):
            xray += (2 * sqrt(((c[i].r * c[i].r) - (d * d))))
            angle = acos((d / c[i].r))
            around += (((2 * angle) / (2 * geometry.PI)) * ((2 * geometry.PI) * c[i].r))
            printf("circle %d (%7.3lf,%7.3lf,%7.3lf) is %7.3lf away from l, xray=%7.3lf around=%7.3lf angle=%7.3lf.\n", i, c[i].c[geometry.X], c[i].c[geometry.Y], c[i].r, d, xray, around, angle)
        i += 1
    travel = ((geometry.distance(s, t) - xray) + around)
    printf("Superman sees through %7.3lf units, and flies %7.3lf units\n", xray, travel)


def main():
    # i: counter
    scanf("%lf %lf", address(s, geometry.X), address(s, geometry.Y))
    scanf("%lf %lf", address(t, geometry.X), address(t, geometry.Y))
    scanf("%d", address(globals(), 'ncircles'))
    if ((ncircles < 0) or (ncircles > MAXN)):
        fprintf(stderr, "circle count exceeds capacity\n")
        return 1
    i = 1
    while (i <= ncircles):
        scanf("%lf %lf %lf", address(c[i].c, geometry.X), address(c[i].c, geometry.Y), address(c[i], 'r'))
        i += 1
    printf("%7.3lf %7.3lf\n", s[geometry.X], s[geometry.Y])
    printf("%7.3lf %7.3lf\n", t[geometry.X], t[geometry.Y])
    printf("%d\n", ncircles)
    i = 1
    while (i <= ncircles):
        printf("%7.3lf %7.3lf %7.3lf\n", c[i].c[geometry.X], c[i].c[geometry.Y], c[i].r)
        i += 1
    superman()
    return 0


if __name__ == "__main__":
    exit(main())
