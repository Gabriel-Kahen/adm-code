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

"""Direct translation of gcd.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import *
from . import _c



# integers to compute the GCD of
def gcd1(p, q):
    if (q > p):
        return gcd1(q, p)
    if (q == 0):
        return p
    printf(" gcd(%ld,%ld) &=& gcd(%ld \\mod %ld, %ld) = gcd(%ld,%ld) \n", p, q, p, q, q, q, c_mod(p, q))
    return gcd1(q, c_mod(p, q))


# Find the gcd(p,q) and x,y such that p*x + q*y = gcd(p,q)
def gcd(p, q, x, y):
    # y1: previous coefficients
    x1 = [0]
    y1 = [0]
    # g: value of gcd(p,q)
    if (q > p):
        return gcd(q, p, y, x)
    if (q == 0):
        x[0] = 1
        y[0] = 0
        return p
    g = gcd(q, c_mod(p, q), x1, y1)
    x[0] = y1[0]
    y[0] = (x1[0] - (c_div(p, q) * y1[0]))
    return g


def main():
    p = [0]
    q = [0]
    x = [0]
    y = [0]
    while (scanf("%ld %ld", p, q) != EOF):
        g1 = gcd1(p[0], q[0])
        g2 = gcd(p[0], q[0], x, y)
        printf("gcd of p=%ld and q=%ld = %ld\n", p[0], q[0], g1)
        printf(" %ld*%ld + %ld*%ld = %ld\n", p[0], x[0], q[0], y[0], g2)
        if (g1 != g2):
            printf("ERROR: GCD\n")
        if (((p[0] * x[0]) + (q[0] * y[0])) != g1):
            printf("ERROR: DIOPHONINE SOLUTION WRONG!\n")
    return 0


if __name__ == "__main__":
    exit(main())
