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

"""Direct translation of random.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import *
from . import _c



# These functions generate random numbers in the designated ranges
def swap(a, b):
    x = a[0]
    a[0] = b[0]
    b[0] = x


# lower/upper bounds on numb
def random_int(low, high):
    # r: random number
    i = RAND_MAX // (high - low + 1)
    i *= ((high - low) + 1)
    while ((j := rand()) >= i):
        continue
    r = (j % (high - low + 1) + low)
    if ((r < low) or (r > high)):
        printf("Error: random integer %d out of range [%d,%d]\n", r, low, high)
    return r


# Construct a random permutation of the $n$ elements of the
# given array.
def random_permutation(a, n):
    i = n
    while (i > 1):
        swap(address(a, (i - 1)), address(a, random_int(0, (i - 1))))
        i -= 1


# lower/upper bounds on numb
def random_float(low, high):
    # j: avoid arithmetic trouble
    # r: random number
    i = RAND_MAX // (high - low)
    i *= (high - low)
    while ((j := rand()) >= i):
        continue
    r = (((j / i) * (high - low)) + low)
    if ((r < low) or (r > high)):
        printf("ERROR: random real %f out of range [%d,%d]\n", r, low, high)
    return r
