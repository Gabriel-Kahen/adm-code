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

"""Direct translation of partition.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import *
from . import _c

# largest number of books
MAXN = 45
# largest number of dividers
MAXK = 10


def max(a, b):
    return (a if (a > b) else b)


def read_partition(s, n, k):
    # i: counter
    scanf("%d %d\n", n, k)
    i = 1
    while (i <= n[0]):
        scanf("%d\n", address(s, i))
        i += 1


def print_books(s, start, end):
    # i: counter
    printf("{")
    i = start
    while (i <= end):
        printf(" %d ", s[i])
        i += 1
    printf("}\n")


def print_matrix(m, n, k):
    # j: counters
    printf("\n")
    i = 1
    while (i <= n):
        j = 1
        while (j <= k):
            printf(" %lld ", m[i][j])
            j += 1
        printf("\n")
        i += 1


def reconstruct_partition(s, d, n, k):
    if (k == 1):
        print_books(s, 1, n)
    else:
        reconstruct_partition(s, d, d[n][k], (k - 1))
        print_books(s, (d[n][k] + 1), n)


def partition(s, n, k):
    prefix_sum = [0 for _ in range((MAXN + 1))]
    best_cost = [[0 for _ in range((MAXK + 1))] for _ in range((MAXN + 1))]
    divider = [[0 for _ in range((MAXK + 1))] for _ in range((MAXN + 1))]
    if (((((n < 1) or (n > MAXN)) or (k < 1)) or (k > MAXK)) or (k > n)):
        fprintf(stderr, "invalid partition dimensions\n")
        return
    # construct prefix sums
    prefix_sum[0] = 0
    i = 1
    while (i <= n):
        prefix_sum[i] = (prefix_sum[(i - 1)] + s[i])
        i += 1
    i = 1
    while (i <= n):
        # initialize boundaries
        best_cost[i][1] = prefix_sum[i]
        i += 1
    # best_cost[i][j] balances the first i books into j nonempty groups.
    # A split after x leaves j - 1 nonempty groups on its left.
    i = 2
    while (i <= n):
        j = 2
        while ((j <= k) and (j <= i)):
            x = (j - 1)
            while (x <= (i - 1)):
                split_cost = max(best_cost[x][(j - 1)], (prefix_sum[i] - prefix_sum[x]))
                # The first feasible split initializes the cell without an infinity sentinel.
                if ((x == (j - 1)) or (best_cost[i][j] > split_cost)):
                    best_cost[i][j] = split_cost
                    divider[i][j] = x
                x += 1
            j += 1
        i += 1
    # print book partition
    reconstruct_partition(s, divider, n, k)


def main():
    # s: book thicknesses to partition
    s = [0 for _ in range((MAXN + 1))]
    # n: how many books?
    n = [0]
    # k: how many partitions?
    k = [0]
    read_partition(s, n, k)
    partition(s, n[0], k[0])
    return 0


if __name__ == "__main__":
    exit(main())
