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

"""Direct translation of plates.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

import math

from ._c import printf, scanf


# how many triangular-lattice layers of radius r balls fit in height h?
def dense_layers(w, h, r):
    # gap: distance between layers
    if (((2 * r) > h) or ((2 * r) > w)):
        return 0
    gap = ((2.0 * r) * (math.sqrt(3) / 2.0))
    return (1 + math.floor(((h - (2.0 * r)) / gap)))


def plates_per_row(row, w, r):
    # plates_per_full_row: number of plates in full/even row
    if (w < (2 * r)):
        return 0
    plates_per_full_row = math.floor((w / (2 * r)))
    if (row % 2 == 0):
        return plates_per_full_row
    # odd row full, too
    if (((w / (2 * r)) - plates_per_full_row) >= 0.5):
        return plates_per_full_row
    else:
        return (plates_per_full_row - 1)


# How many radius r plates fit in a hexagonal-lattice packed w*h box?
def dense_plates(w, l, r):
    # layers: number of layers of balls
    layers = dense_layers(w, l, r)
    return ((math.ceil((layers / 2.0)) * plates_per_row(0, w, r)) + (math.floor((layers / 2.0)) * plates_per_row(1, w, r)))


def grid_plates(w, h, r):
    # layers: number of layers of balls
    layers = math.floor((h / (2 * r)))
    return (layers * plates_per_row(0, w, r))


# Hexagonal coordinates start with the center of disk (0,0) at
# geometric point (0,0).  The hexagonal coordinate $(xh,yh)$
# refers to the center of the disk on the horizontal row xh
# and positive-slope diagonal yh.   The geometric coordinate of
# such a point is a function of the radius of the disk $r$.
def hex_to_geo(xh, yh, r, xg, yg):
    yg[0] = (((2.0 * r) * xh) * (math.sqrt(3) / 2.0))
    xg[0] = ((((2.0 * r) * xh) * (1.0 / 2.0)) + ((2.0 * r) * yh))


def geo_to_hex(xg, yg, r, xh, yh):
    xh[0] = (((2.0 / math.sqrt(3)) * yg) / (2.0 * r))
    yh[0] = ((xg - (((2.0 * r) * xh[0]) * (1.0 / 2.0))) / (2.0 * r))


# Under the hexagonal coordinate system, the set of hexagons defined
# by coordinates (hx,hy), where $0 <= hx <= xmax$ and $0 <= hx <= ymax$
# forms a diamond-shaped patch, not a conventional axis-oriented
# rectangle.  To solve this problem, we define array coordinates
# so that (ax,ay) refers to the position in an axis-oriented
# rectangle with (0,0) as the lower righthand point in the matrix.
def array_to_hex(xa, ya, xh, yh):
    xh[0] = xa
    yh[0] = ((ya - xa) + math.ceil((xa / 2.0)))


def hex_to_array(xh, yh, xa, ya):
    xa[0] = xh
    ya[0] = ((yh + xh) - math.ceil((xh / 2.0)))


def plates_on_top(xh, yh, w, l, r):
    # total plates on top
    number_on_top = 0
    # layers: number of rows in grid
    # rowlength: number of plates in row
    # row: counter
    # yra: array coordinates
    xla = [0]
    yla = [0]
    xra = [0]
    yra = [0]
    layers = dense_layers(w, l, r)
    row = (xh + 1)
    while (row < layers):
        rowlength = (plates_per_row(row, w, r) - 1)
        hex_to_array(row, (yh - (row - xh)), xla, yla)
        if (yla[0] < 0):
            # left boundary
            yla[0] = 0
        hex_to_array(row, yh, xra, yra)
        if (yra[0] > rowlength):
            # right boundary
            yra[0] = rowlength
        number_on_top += ((yra[0] - yla[0]) + 1)
        row += 1
    return number_on_top


def main():
    # w: box width
    w = [0.0]
    # l: box length
    l = [0.0]
    # r: plate radius
    r = [0.0]
    # i: counters
    printf("input box width, box length, and plate radius:\n")
    scanf("%lf %lf %lf", w, l, r)
    printf("box width=%lf, box length=%lf, and plate radius=%lf:\n", w[0], l[0], r[0])
    printf("dense packing = %d\n", dense_plates(w[0], l[0], r[0]))
    printf("grid packing = %d\n", grid_plates(w[0], l[0], r[0]))
    # print all the possible hexes in the box
    xmax = math.floor((w[0] / (2 * r[0])))
    i = 0
    while (i < xmax):
        printf("(0,%d) has %d on top.\n", i, plates_on_top(0, i, w[0], l[0], r[0]))
        i += 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
