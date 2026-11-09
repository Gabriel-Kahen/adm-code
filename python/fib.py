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

"""Direct translation of fib.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import *
from . import _c

# binomial.c
# Compute the binomial coefficients using dynamic programming
# largest n for which F(n) fits in a long
MAXN = 92
# contents denote an empty cell
UNKNOWN = (-1)
# f: array for caching fib values
f = [0 for _ in range((MAXN + 1))]


# computer n choose m
# Returns -1 with errno set for invalid arguments or an unrepresentable result.
def binomial_coefficient(n, k):
    bc = array_init([0 for _ in range((MAXN + 1))], [0])
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


def fib_r(n):
    if (n == 0):
        return 0
    if (n == 1):
        return 1
    return (fib_r((n - 1)) + fib_r((n - 2)))


def fib_c(n):
    if (f[n] == UNKNOWN):
        f[n] = (fib_c((n - 1)) + fib_c((n - 2)))
    return f[n]


def fib_c_driver(n):
    # i: counter
    f[0] = 0
    f[1] = 1
    i = 2
    while (i <= n):
        f[i] = UNKNOWN
        i += 1
    return fib_c(n)


def fib_dp(n):
    # i: counter
    # f: array for caching values
    f = [0 for _ in range((MAXN + 1))]
    f[0] = 0
    f[1] = 1
    i = 2
    while (i <= n):
        f[i] = (f[(i - 1)] + f[(i - 2)])
        i += 1
    return f[n]


def fib_ultimate(n):
    # i: counter
    # last two values of f[n]
    back2 = 0
    back1 = 1
    # next: placeholder for sum
    if (n == 0):
        return 0
    i = 2
    while (i < n):
        next = (back1 + back2)
        back2 = back1
        back1 = next
        i += 1
    return (back1 + back2)


def main():
    ntest = 92
    i = 0
    while (i <= ntest):
        printf("fib_c(%d) = %ld\n", i, fib_c_driver(i))
        i += 1
    i = 0
    while (i <= ntest):
        printf("fib_dp(%d) = %ld\n", i, fib_dp(i))
        i += 1
    i = 0
    while (i <= ntest):
        printf("fib_dp2(%d) = %ld\n", i, fib_ultimate(i))
        i += 1
    # for (i = 0; i <= ntest; i++) {
    # printf("fib(%d) = %ld\n",i, fib_r(i));
    # }
    return 0


if __name__ == "__main__":
    exit(main())
