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

"""Direct translation of geometry.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import *
from . import _c

# ratio of circumference to diameter
# a quantity small enough to be zero
class line:
    def __init__(self):
        # a: x-coefficient
        self.a = 0.0
        # b: y-coefficient
        self.b = 0.0
        # c: constant term
        self.c = 0.0


# dimension of points
# x-coordinate index
# y-coordinate index
# maximum number of points in a polygon
class polygon:
    def __init__(self):
        # n: number of points in polygon
        self.n = 0
        # p: array of points in polygon
        self.p = [[0.0 for _ in range(DIMENSION)] for _ in range(MAXPOLY)]


class segment:
    def __init__(self):
        # p2: endpoints of line segment
        self.p1 = [0.0 for _ in range(DIMENSION)]
        self.p2 = [0.0 for _ in range(DIMENSION)]


# triangle: triangle datatype
class triangulation:
    def __init__(self):
        # n: number of triangles in triangulation
        self.n = 0
        # t: indicies of vertices in triangulation
        self.t = [[0 for _ in range(3)] for _ in range(MAXPOLY)]


class circle:
    def __init__(self):
        # c: center of circle
        self.c = [0.0 for _ in range(DIMENSION)]
        # r: radius of circle
        self.r = 0.0


PI = 3.1415926
EPSILON = 0.000001
DIMENSION = 2
X = 0
Y = 1
MAXPOLY = 200


def points_to_line(p1, p2, l):
    if (p1[X] == p2[X]):
        l.a = 1
        l.b = 0
        l.c = (-p1[X])
    else:
        l.b = 1
        l.a = ((-(p1[Y] - p2[Y])) / (p1[X] - p2[X]))
        l.c = ((-(l.a * p1[X])) - (l.b * p1[Y]))


def point_and_slope_to_line(p, m, l):
    l.a = (-m)
    l.b = 1
    l.c = (-((l.a * p[X]) + (l.b * p[Y])))


def parallelQ(l1, l2):
    return ((fabs((l1.a - l2.a)) <= EPSILON) and (fabs((l1.b - l2.b)) <= EPSILON))


def same_lineQ(l1, l2):
    return (parallelQ(l1, l2) and (fabs((l1.c - l2.c)) <= EPSILON))


def intersection_point(l1, l2, p):
    if same_lineQ(l1, l2):
        printf("Warning: Identical lines, all points intersect.\n")
        p[Y] = 0.0
        p[X] = p[Y]
        return
    if parallelQ(l1, l2):
        printf("Error: Distinct parallel lines do not intersect.\n")
        return
    p[X] = (((l2.b * l1.c) - (l1.b * l2.c)) / ((l2.a * l1.b) - (l1.a * l2.b)))
    # test for vertical line
    if (fabs(l1.b) > EPSILON):
        p[Y] = ((-((l1.a * p[X]) + l1.c)) / l1.b)
    else:
        p[Y] = ((-((l2.a * p[X]) + l2.c)) / l2.b)


def closest_point(p_in, l, p_c):
    # perp: perpendicular to l through (x,y)
    perp = line()
    # vertical line
    if (fabs(l.b) <= EPSILON):
        p_c[X] = (-l.c)
        p_c[Y] = p_in[Y]
        return
    # horizontal line
    if (fabs(l.a) <= EPSILON):
        p_c[X] = p_in[X]
        p_c[Y] = (-l.c)
        return
    point_and_slope_to_line(p_in, (1 / l.a), perp)
    intersection_point(l, perp, p_c)


def distance(a, b):
    # i: counter
    # accumulated distance
    d = 0.0
    i = 0
    while (i < DIMENSION):
        d = (d + ((a[i] - b[i]) * (a[i] - b[i])))
        i += 1
    return sqrt(d)


def copy_point(a, b):
    # i: counter
    i = 0
    while (i < DIMENSION):
        b[i] = a[i]
        i += 1


def swap_point(a, b):
    # c: temporary point
    c = [0.0 for _ in range(DIMENSION)]
    copy_point(a, c)
    copy_point(b, a)
    copy_point(c, b)


def points_to_segment(a, b, s):
    copy_point(a, s.p1)
    copy_point(b, s.p2)


def segment_to_points(s, p1, p2):
    copy_point(s.p1, p1)
    copy_point(s.p2, p2)


def point_in_box(p, b1, b2):
    return ((((p[X] >= min(b1[X], b2[X])) and (p[X] <= max(b1[X], b2[X]))) and (p[Y] >= min(b1[Y], b2[Y]))) and (p[Y] <= max(b1[Y], b2[Y])))


def segments_intersect(s1, s2):
    a = signed_triangle_area(s1.p1, s1.p2, s2.p1)
    b = signed_triangle_area(s1.p1, s1.p2, s2.p2)
    c = signed_triangle_area(s2.p1, s2.p2, s1.p1)
    d = signed_triangle_area(s2.p1, s2.p2, s1.p2)
    # Test the input endpoints directly; a rounded line intersection can
    # fall just outside a segment that contains its shared endpoint.
    if (((((fabs(a) <= EPSILON) and point_in_box(s2.p1, s1.p1, s1.p2)) or ((fabs(b) <= EPSILON) and point_in_box(s2.p2, s1.p1, s1.p2))) or ((fabs(c) <= EPSILON) and point_in_box(s1.p1, s2.p1, s2.p2))) or ((fabs(d) <= EPSILON) and point_in_box(s1.p2, s2.p1, s2.p2))):
        return 1
    return ((((a > EPSILON) and (b < (-EPSILON))) or ((a < (-EPSILON)) and (b > EPSILON))) and (((c > EPSILON) and (d < (-EPSILON))) or ((c < (-EPSILON)) and (d > EPSILON))))


def signed_triangle_area(a, b, c):
    return (((((((a[X] * b[Y]) - (a[Y] * b[X])) + (a[Y] * c[X])) - (a[X] * c[Y])) + (b[X] * c[Y])) - (c[X] * b[Y])) / 2.0)


def triangle_area(a, b, c):
    return fabs(signed_triangle_area(a, b, c))


def ccw(a, b, c):
    return (signed_triangle_area(a, b, c) > EPSILON)


def cw(a, b, c):
    return (signed_triangle_area(a, b, c) < (-EPSILON))


def collinear(a, b, c):
    return (fabs(signed_triangle_area(a, b, c)) <= EPSILON)


def print_points(p, n):
    # i: counter
    i = 0
    while (i < n):
        printf("(%lf,%lf)\n", p[i][X], p[i][Y])
        i += 1


def print_polygon(p):
    # i: counter
    i = 0
    while (i < p.n):
        printf("(%lf,%lf)\n", p.p[i][X], p.p[i][Y])
        i += 1


def print_point(p):
    printf("%7.3lf %7.3lf\n", p[X], p[Y])


def print_line(l):
    printf("(a=%7.3lf,b=%7.3lf,c=%7.3lf)\n", l.a, l.b, l.c)


def print_segment(s):
    printf("segment: ")
    print_point(s.p1)
    print_point(s.p2)
