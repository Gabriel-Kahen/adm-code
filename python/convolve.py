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

"""Direct translation of convolve.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import *
from . import _c

# largest n or m
MAXN = 100


def max(x, y):
    if (x > y):
        return x
    else:
        return y


def min(x, y):
    if (x < y):
        return x
    else:
        return y


def main():
    # j: counters
    # a: sequences
    a = [0 for _ in range(MAXN)]
    b = [0 for _ in range(MAXN)]
    c = [0 for _ in range(((2 * MAXN) - 1))]
    # m: sequence lengths
    n = [0]
    m = [0]
    i = 0
    while (i < MAXN):
        b[i] = 0
        a[i] = b[i]
        i += 1
    i = 0
    while (i < ((2 * MAXN) - 1)):
        c[i] = 0
        i += 1
    if (((scanf("%d", m) != 1) or (m[0] < 1)) or (m[0] > MAXN)):
        return 1
    i = 0
    while (i < m[0]):
        scanf("%d", address(a, i))
        i += 1
    if (((scanf("%d", n) != 1) or (n[0] < 1)) or (n[0] > MAXN)):
        return 1
    i = 0
    while (i < n[0]):
        scanf("%d", address(b, i))
        i += 1
    i = 0
    while (i < ((n[0] + m[0]) - 1)):
        j = max(0, (i - (n[0] - 1)))
        while (j <= min((m[0] - 1), i)):
            c[i] = (c[i] + (a[j] * b[(i - j)]))
            j += 1
        i += 1
    i = 0
    while (i < ((m[0] + n[0]) - 1)):
        printf("%d ", c[i])
        i += 1
    printf("\n")
    return 0


if __name__ == "__main__":
    exit(main())
