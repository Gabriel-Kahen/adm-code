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

"""Direct translation of geotest.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import *
from . import _c
from . import geometry



def main():
    p1 = [0.0 for _ in range(geometry.DIMENSION)]
    p2 = [0.0 for _ in range(geometry.DIMENSION)]
    q1 = [0.0 for _ in range(geometry.DIMENSION)]
    q2 = [0.0 for _ in range(geometry.DIMENSION)]
    i = [0.0 for _ in range(geometry.DIMENSION)]
    l1 = geometry.line()
    l2 = geometry.line()
    l3 = geometry.line()
    while (scanf("%lf %lf", address(p1, geometry.X), address(p1, geometry.Y)) != EOF):
        scanf("%lf %lf", address(p2, geometry.X), address(p2, geometry.Y))
        scanf("%lf %lf", address(q1, geometry.X), address(q1, geometry.Y))
        scanf("%lf %lf", address(q2, geometry.X), address(q2, geometry.Y))
        geometry.print_point(p1)
        geometry.print_point(p2)
        geometry.print_point(q1)
        geometry.print_point(q2)
        geometry.points_to_line(p1, p2, l1)
        geometry.points_to_line(q1, q2, l2)
        geometry.print_line(l1)
        geometry.print_line(l2)
        printf("slope and line tests\n")
        geometry.point_and_slope_to_line(p1, (-l1.a), l3)
        geometry.print_line(l3)
        geometry.point_and_slope_to_line(p2, (-l1.a), l3)
        geometry.print_line(l3)
        geometry.point_and_slope_to_line(q1, (-l2.a), l3)
        geometry.print_line(l3)
        geometry.point_and_slope_to_line(q2, (-l2.a), l3)
        geometry.print_line(l3)
        printf("parallel lines test\n")
        printf("%d\n", geometry.parallelQ(l1, l2))
        printf("intersection point\n")
        geometry.intersection_point(l1, l2, i)
        geometry.print_point(i)
        printf("closest point\n")
        geometry.closest_point(p1, l1, i)
        geometry.print_point(i)
        geometry.closest_point(p2, l1, i)
        geometry.print_point(i)
        geometry.closest_point(q1, l1, i)
        geometry.print_point(i)
        geometry.closest_point(q2, l1, i)
        geometry.print_point(i)
        geometry.closest_point(p1, l2, i)
        geometry.print_point(i)
        geometry.closest_point(p2, l2, i)
        geometry.print_point(i)
        geometry.closest_point(q1, l2, i)
        geometry.print_point(i)
        geometry.closest_point(q2, l2, i)
        geometry.print_point(i)
        printf("--------------------------------\n")
    return 0


if __name__ == "__main__":
    exit(main())
