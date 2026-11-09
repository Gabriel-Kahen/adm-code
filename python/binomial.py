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

"""Direct translation of binomial.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import EDOM, ERANGE, LONG_MAX, perror, printf, scanf
from . import _c

# binomial.c
# Compute the binomial coefficients using dynamic programming
# by: Steven Skiena
# largest n or k
MAXN = 100


# compute n choose k
# Returns -1 with errno set for invalid arguments or an unrepresentable result.
def binomial_coefficient(n, k):
    bc = [0] * (MAXN + 1)
    _c.errno = 0
    if ((((n < 0) or (n > MAXN)) or (k < 0)) or (k > n)):
        _c.errno = EDOM
        return (-1)
    if (k > (n - k)):
        k = (n - k)
    bc[0] = 1
    i = 1
    while (i <= n):
        last = (i if (i < k) else k)
        j = last
        while (j > 0):
            if (bc[j] > (LONG_MAX - bc[(j - 1)])):
                _c.errno = ERANGE
                return (-1)
            bc[j] += bc[(j - 1)]
            j -= 1
        i += 1
    return bc[k]


def main():
    a = 0
    b = 0
    n = 0
    _, n = scanf("%d", n)
    i = 0
    while (i < n):
        _, a, b = scanf("%d %d", a, b)
        coefficient = binomial_coefficient(a, b)
        if (coefficient < 0):
            perror("binomial coefficient")
            return 1
        printf("%d choose %d = %ld\n", a, b, coefficient)
        i += 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
