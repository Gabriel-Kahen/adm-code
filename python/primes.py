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

"""Direct translation of primes.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import *
from . import _c



def prime_factorization(x):
    # i: counter
    # c: remaining product to factor
    c = x
    while (c_mod(c, 2) == 0):
        printf("%d\n", 2)
        c = c_div(c, 2)
    i = 3
    while (i <= (sqrt(c) + 1)):
        if (c_mod(c, i) == 0):
            printf("%ld\n", i)
            c = c_div(c, i)
        else:
            i = (i + 2)
    if (c > 1):
        printf("%ld\n", c)


def main():
    p = [0]
    while (scanf("%ld", p) != EOF):
        printf("prime factorization of p=%ld \n", p[0])
        prime_factorization(p[0])
    return 0


if __name__ == "__main__":
    exit(main())
