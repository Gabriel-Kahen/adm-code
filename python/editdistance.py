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

from ._c import printf, strlen

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
    # i, j, k: counters
    i = 0
    j = 0
    # opt: cost of the three options
    opt = [0 for _ in range(3)]
    while (i <= MAXLEN):
        row_init(i, m)
        column_init(i, m)
        i += 1
    i = 1
    while (i < strlen(s)):
        j = 1
        while (j < strlen(t)):
            opt[MATCH] = (m[(i - 1)][(j - 1)].cost + match(s[i], t[j]))
            opt[INSERT] = (m[i][(j - 1)].cost + indel(t[j]))
            opt[DELETE] = (m[(i - 1)][j].cost + indel(s[i]))
            m[i][j].cost = opt[MATCH]
            m[i][j].parent = MATCH
            k = INSERT
            while (k <= DELETE):
                if (opt[k] < m[i][j].cost):
                    m[i][j].cost = opt[k]
                    m[i][j].parent = k
                k += 1
            j += 1
        i += 1
    i, j = goal_cell(s, t)
    return m[i][j].cost


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
    # i, j: counters
    # x, y: string lengths
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
