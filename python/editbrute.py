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

"""Direct translation of editbrute.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import fprintf, printf, stderr, strlen
from . import editdistance
from . import editinput

# [[ cell_instance_cut
# m: dynamic programming table
m = [[editdistance.cell() for _ in range((editdistance.MAXLEN + 1))] for _ in range((editdistance.MAXLEN + 1))]


# ]]
def goal_cell(s, t):
    i = (strlen(s) - 1)
    j = (strlen(t) - 1)
    return i, j


def match(c, d):
    if (c == d):
        return 0
    return 1


def indel(c):
    return 1


def row_init(i, m):
    m[0][i].cost = i
    if (i > 0):
        m[0][i].parent = editdistance.INSERT
    else:
        m[0][i].parent = (-1)


def column_init(i, m):
    m[i][0].cost = i
    if (i > 0):
        m[i][0].parent = editdistance.DELETE
    else:
        m[0][i].parent = (-1)


def match_out(s, t, i, j):
    if (s[i] == t[j]):
        printf("M")
    else:
        printf("S")


def insert_out(t, j):
    printf("I")


def delete_out(s, i):
    printf("D")


def string_compare2(s, t, i, j, m):
    # k: counter
    # opt: cost of the three options
    opt = [0 for _ in range(3)]
    # lowest_cost: lowest cost
    # indel is the cost of an insertion or deletion
    if (i == 0):
        m[i][j].cost = (j * indel(ord(' ')))
        m[i][j].parent = (editdistance.INSERT if j else (-1))
        return m[i][j].cost
    if (j == 0):
        m[i][j].cost = (i * indel(ord(' ')))
        m[i][j].parent = editdistance.DELETE
        return m[i][j].cost
    opt[editdistance.MATCH] = (string_compare2(s, t, (i - 1), (j - 1), m) + match(s[i], t[j]))
    opt[editdistance.INSERT] = (string_compare2(s, t, i, (j - 1), m) + indel(t[j]))
    opt[editdistance.DELETE] = (string_compare2(s, t, (i - 1), j, m) + indel(s[i]))
    lowest_cost = opt[editdistance.MATCH]
    m[i][j].parent = editdistance.MATCH
    k = editdistance.INSERT
    while (k <= editdistance.DELETE):
        if (opt[k] < lowest_cost):
            lowest_cost = opt[k]
            m[i][j].parent = k
        k += 1
    # REMOVE FROM PRINTED VERSION
    m[i][j].cost = lowest_cost
    return lowest_cost


def string_compare_r(s, t, i, j):
    # k: counter
    # opt: cost of the three options
    opt = [0 for _ in range(3)]
    # lowest_cost: lowest cost
    # indel is the cost of an insertion or deletion
    if (i == 0):
        m[i][j].cost = (j * indel(ord(' ')))
        m[i][j].parent = (editdistance.INSERT if j else (-1))
        return m[i][j].cost
    if (j == 0):
        m[i][j].cost = (i * indel(ord(' ')))
        m[i][j].parent = editdistance.DELETE
        return m[i][j].cost
    # match is the cost of a match/substitution
    opt[editdistance.MATCH] = (string_compare_r(s, t, (i - 1), (j - 1)) + match(s[i], t[j]))
    opt[editdistance.INSERT] = (string_compare_r(s, t, i, (j - 1)) + indel(t[j]))
    opt[editdistance.DELETE] = (string_compare_r(s, t, (i - 1), j) + indel(s[i]))
    lowest_cost = opt[editdistance.MATCH]
    m[i][j].parent = editdistance.MATCH
    k = editdistance.INSERT
    while (k <= editdistance.DELETE):
        if (opt[k] < lowest_cost):
            lowest_cost = opt[k]
            m[i][j].parent = k
        k += 1
    return lowest_cost


def reconstruct_path(s, t, i, j, m):
    if (m[i][j].parent == (-1)):
        return
    if (m[i][j].parent == editdistance.MATCH):
        reconstruct_path(s, t, (i - 1), (j - 1), m)
        match_out(s, t, i, j)
        return
    if (m[i][j].parent == editdistance.INSERT):
        reconstruct_path(s, t, i, (j - 1), m)
        insert_out(t, j)
        return
    if (m[i][j].parent == editdistance.DELETE):
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


def main():
    # s: input strings
    s = [0 for _ in range((editdistance.MAXLEN + 2))]
    t = [0 for _ in range((editdistance.MAXLEN + 2))]
    t[0] = ord(' ')
    s[0] = t[0]
    if ((not editinput.read_edit_string(s, editdistance.MAXLEN)) or (not editinput.read_edit_string(t, editdistance.MAXLEN))):
        fprintf(stderr, "expected two strings of at most %d characters\n", editdistance.MAXLEN)
        return 1
    cost1 = string_compare_r(s, t, (strlen(s) - 1), (strlen(t) - 1))
    printf("matching cost = %d \n", (cost2 := string_compare2(s, t, (strlen(s) - 1), (strlen(t) - 1), m)))
    if (cost1 != cost2):
        printf("Editbrutes do not agree: cost1=%d cost2=%d\n", cost1, cost2)
    print_matrix(s, t, True, m)
    printf("\n")
    print_matrix(s, t, False, m)
    i, j = goal_cell(s, t)
    printf("%d %d\n", i, j)
    reconstruct_path(s, t, i, j, m)
    printf("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
