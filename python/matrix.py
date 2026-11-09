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

"""Direct translation of matrix.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import printf, scanf

# maximum number of vertices
# maximum outdegree of a vertex
class matrix:
    def __init__(self):
        # m: adjacency/weight info
        self.m = [[0 for _ in range((MAXV + 1))] for _ in range((MAXV + 1))]
        # rows: number of rows
        self.rows = 0
        # columns: number of columns
        self.columns = 0


MAXV = 100
MAXDEGREE = 50
MAXINT = 100007


def initialize_matrix(m):
    # i, j: counters
    i = 1
    while (i <= m.rows):
        j = 1
        while (j <= m.columns):
            m.m[i][j] = 0
            j += 1
        i += 1


def read_matrix(m):
    # i, j: counters
    _, m.rows, m.columns = scanf("%d %d\n", m.rows, m.columns)
    i = 1
    while (i <= m.rows):
        j = 1
        while (j <= m.columns):
            _, m.m[i][j] = scanf("%d", m.m[i][j])
            j += 1
        i += 1


def print_matrix(g):
    # i, j: counters
    i = 1
    while (i <= g.rows):
        j = 1
        while (j <= g.columns):
            printf(" %d", g.m[i][j])
            j += 1
        printf("\n")
        i += 1
    printf("\n")


def multiply(a, b, c):
    # i, j, k: dimension counters
    if (a.columns != b.rows):
        printf("Error: bounds dont match!\n")
        return
    c.rows = a.rows
    c.columns = b.columns
    i = 1
    while (i <= a.rows):
        j = 1
        while (j <= b.columns):
            c.m[i][j] = 0
            k = 1
            while (k <= b.rows):
                c.m[i][j] += (a.m[i][k] * b.m[k][j])
                k += 1
            j += 1
        i += 1


def main():
    a = matrix()
    b = matrix()
    c = matrix()
    read_matrix(a)
    print_matrix(a)
    read_matrix(b)
    print_matrix(b)
    multiply(a, b, c)
    print_matrix(c)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
