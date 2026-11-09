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

"""Direct translation of subsetsum.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import *
from . import _c

# largest n
MAXN = 100
# largest sum we will consider
MAXSUM = 10000
NIL = (-1)
# compute whether k can be made as a subset sum from s
# sum: table of realizable sums
sum = [[0 for _ in range((MAXSUM + 1))] for _ in range((MAXN + 1))]
# parent: table of parent pointers
parent = [[0 for _ in range((MAXSUM + 1))] for _ in range((MAXN + 1))]


def subset_sum(s, n, k):
    # j: counters
    sum[0][0] = True
    parent[0][0] = NIL
    i = 1
    while (i <= k):
        sum[0][i] = False
        parent[0][i] = NIL
        i += 1
    # build table
    i = 1
    while (i <= n):
        j = 0
        while (j <= k):
            sum[i][j] = sum[(i - 1)][j]
            parent[i][j] = NIL
            if ((j >= s[(i - 1)]) and (sum[(i - 1)][(j - s[(i - 1)])] == True)):
                sum[i][j] = True
                parent[i][j] = (j - s[(i - 1)])
            j += 1
        i += 1
    return sum[n][k]


def report_subset(n, k):
    if (k == 0):
        return
    if (parent[n][k] == NIL):
        report_subset((n - 1), k)
    else:
        report_subset((n - 1), parent[n][k])
        printf(" %d ", (k - parent[n][k]))


def main():
    n = [0]
    k = [0]
    s = [0 for _ in range((MAXN + 1))]
    m = [0]
    scanf("%d", m)
    j = 0
    while (j < m[0]):
        scanf("%d %d", n, k)
        printf("n=%d  k=%d \n", n[0], k[0])
        i = 0
        while (i < n[0]):
            scanf("%d", address(s, i))
            printf(" %d ", s[i])
            i += 1
        printf("\n Is %d realizable: %d\n", k[0], (r := subset_sum(s, n[0], k[0])))
        if r:
            report_subset(n[0], k[0])
        printf("\n\n")
        j += 1
    return 0


if __name__ == "__main__":
    exit(main())
