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

"""Direct translation of editdistance.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import *
from . import _c

# longest possible string
# enumerated type symbol for match
# enumerated type symbol for insert
# enumerated type symbol for delete
class cell:
    def __init__(self):
        # cost: cost of reaching this cell
        self.cost = 0
        # parent: parent cell
        self.parent = 0


MAXLEN = 101
MATCH = 0
INSERT = 1
DELETE = 2


def string_compare(s, t, m):
    # k: counters
    i = [0]
    j = [0]
    # opt: cost of the three options
    opt = [0 for _ in range(3)]
    i[0] = 0
    while (i[0] <= MAXLEN):
        row_init(i[0], m)
        column_init(i[0], m)
        i[0] += 1
    i[0] = 1
    while (i[0] < strlen(s)):
        j[0] = 1
        while (j[0] < strlen(t)):
            opt[MATCH] = (m[(i[0] - 1)][(j[0] - 1)].cost + match(s[i[0]], t[j[0]]))
            opt[INSERT] = (m[i[0]][(j[0] - 1)].cost + indel(t[j[0]]))
            opt[DELETE] = (m[(i[0] - 1)][j[0]].cost + indel(s[i[0]]))
            m[i[0]][j[0]].cost = opt[MATCH]
            m[i[0]][j[0]].parent = MATCH
            k = INSERT
            while (k <= DELETE):
                if (opt[k] < m[i[0]][j[0]].cost):
                    m[i[0]][j[0]].cost = opt[k]
                    m[i[0]][j[0]].parent = k
                k += 1
            j[0] += 1
        i[0] += 1
    goal_cell(s, t, i, j)
    return m[i[0]][j[0]].cost


def reconstruct_path(s, t, i, j, m):
    if (m[i][j].parent == (-1)):
        return
    if (m[i][j].parent == MATCH):
        reconstruct_path(s, t, (i - 1), (j - 1), m)
        match_out(s, t, i, j)
        return
    if (m[i][j].parent == INSERT):
        reconstruct_path(s, t, i, (j - 1), m)
        insert_out(t, j)
        return
    if (m[i][j].parent == DELETE):
        reconstruct_path(s, t, (i - 1), j, m)
        delete_out(s, i)
        return


def print_matrix(s, t, costQ, m):
    # j: counters
    # y: string lengths
    x = strlen(s)
    y = strlen(t)
    printf("   ")
    i = 0
    while (i < y):
        printf("  %c", t[i])
        i += 1
    printf("\n")
    i = 0
    while (i < x):
        printf("%c: ", s[i])
        j = 0
        while (j < y):
            if costQ:
                printf(" %2d", m[i][j].cost)
            else:
                printf(" %2d", m[i][j].parent)
            j += 1
        printf("\n")
        i += 1
