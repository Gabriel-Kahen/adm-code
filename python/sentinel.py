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

"""Direct translation of sentinel.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import *
from . import _c

MAXINT = 1000000
a = [0 for _ in range(100)]


def main():
    i = 1
    while (i <= 20):
        a[i] = i
        i += 1
    n = 20
    x = (-1)
    i = n
    while ((a[i] >= x) and (i >= 1)):
        a[(i + 1)] = a[i]
        i = (i - 1)
    a[(i + 1)] = x
    printf("without sentinel, i=%d a[1]=%d\n", i, a[1])
    i = 1
    while (i <= 25):
        printf("%d ", a[i])
        i += 1
    x = (-2)
    n = 21
    i = n
    a[0] = (-MAXINT)
    while (a[i] >= x):
        a[(i + 1)] = a[i]
        i = (i - 1)
    a[(i + 1)] = x
    printf("\nwith sentinel, i=%d a[1]=%d\n", i, a[1])
    i = 1
    while (i <= 25):
        printf("%d ", a[i])
        i += 1
    return 0


if __name__ == "__main__":
    exit(main())
