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

"""Direct translation of set_union.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import printf

class union_find:
    def __init__(self):
        # p: parent element
        self.p = [0 for _ in range((SET_SIZE + 1))]
        # size: number of elements in subtree i
        self.size = [0 for _ in range((SET_SIZE + 1))]
        # n: number of elements in set
        self.n = 0


SET_SIZE = 1000


def union_find_init(s, n):
    # i: counter
    i = 1
    while (i <= n):
        s.p[i] = i
        s.size[i] = 1
        i += 1
    s.n = n


def find(s, x):
    if (s.p[x] == x):
        return x
    return find(s, s.p[x])


def union_sets(s, s1, s2):
    # r1, r2: roots of sets
    r1 = find(s, s1)
    r2 = find(s, s2)
    if (r1 == r2):
        # return: already in same set
        return
    if (s.size[r1] >= s.size[r2]):
        s.size[r1] = (s.size[r1] + s.size[r2])
        s.p[r2] = r1
    else:
        s.size[r2] = (s.size[r1] + s.size[r2])
        s.p[r1] = r2


def same_component(s, s1, s2):
    return (find(s, s1) == find(s, s2))


def print_union_find(s):
    # i: counter
    i = 1
    while (i <= s.n):
        printf("%i  set=%d size=%d \n", i, s.p[i], s.size[i])
        i += 1
    printf("\n")
