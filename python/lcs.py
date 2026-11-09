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

"""Direct translation of lcs.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import *
from . import _c
from . import editdistance
from . import editinput

# m: dynamic programming table
m = [[editdistance.cell() for _ in range((editdistance.MAXLEN + 1))] for _ in range((editdistance.MAXLEN + 1))]


# For normal edit distance computation
def goal_cell(s, t, i, j):
    i[0] = (strlen(s) - 1)
    j[0] = (strlen(t) - 1)


def match(c, d):
    if (c == d):
        return 0
    return editdistance.MAXLEN


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
        printf("%c", s[i])


def insert_out(t, j):
    pass


def delete_out(s, i):
    pass


def main():
    # Bind this application's callbacks to the shared C-style backend.
    editdistance.goal_cell = goal_cell
    editdistance.match = match
    editdistance.indel = indel
    editdistance.row_init = row_init
    editdistance.column_init = column_init
    editdistance.match_out = match_out
    editdistance.insert_out = insert_out
    editdistance.delete_out = delete_out
    i = [0]
    j = [0]
    # s: input strings
    s = [0 for _ in range((editdistance.MAXLEN + 2))]
    t = [0 for _ in range((editdistance.MAXLEN + 2))]
    t[0] = ord(' ')
    s[0] = t[0]
    if ((not editinput.read_edit_string(s, editdistance.MAXLEN)) or (not editinput.read_edit_string(t, editdistance.MAXLEN))):
        fprintf(stderr, "expected two strings of at most %d characters\n", editdistance.MAXLEN)
        return 1
    complen = editdistance.string_compare(s, t, m)
    lcslen = c_div((((strlen(s) + strlen(t)) - 2) - complen), 2)
    printf("length of longest common subsequence = %d\n", lcslen)
    goal_cell(s, t, i, j)
    editdistance.reconstruct_path(s, t, i[0], j[0], m)
    printf("\n")
    return 0


if __name__ == "__main__":
    exit(main())
