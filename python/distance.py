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

"""Direct translation of distance.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import *
from . import _c

DIMENSION = 3


def distance(a, b):
    d = 0.0
    i = 0
    while (i < DIMENSION):
        delta = (float(a[i]) - float(b[i]))
        d += (delta * delta)
        i += 1
    return sqrt(d)


def main():
    a = array_init([0 for _ in range(DIMENSION)], [6, 2, 3])
    b = array_init([0 for _ in range(DIMENSION)], [6, 3, 4])
    printf("distance = %f\n", distance(a, b))
    return 0


if __name__ == "__main__":
    exit(main())
