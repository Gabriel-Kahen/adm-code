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

"""Direct translation of paths.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import *
from . import _c
from . import graph

# max possible next extensions
# maximum solution size
# solution_count: how many solutions are there?
class paths_data:
    def __init__(self):
        # s: source vertex
        self.s = 0
        # t: destination vertex
        self.t = 0
        # g: graph to find paths in
        self.g = graph.graph()


MAXCANDIDATES = 100
NMAX = 100
finished = False
solution_count = 0


def process_solution(a, k, input):
    global solution_count
    # i: counter
    solution_count += 1
    printf("{")
    i = 1
    while (i <= k):
        printf(" %d", a[i])
        i += 1
    printf(" }\n")


def is_a_solution(a, k, g):
    return ((k > 0) and (a[k] == g.t))


def make_move(a, k, input):
    pass


def unmake_move(a, k, input):
    pass


# What are possible elements of the next slot in the path
def construct_candidates(a, k, g, c, nc):
    # i: counters
    # in_sol: what's already in the solution?
    in_sol = [0 for _ in range((NMAX + 1))]
    # p: temporary pointer
    # last: last vertex on current path
    i = 1
    while (i <= g.g.nvertices):
        in_sol[i] = False
        i += 1
    i = 1
    while (i < k):
        in_sol[a[i]] = True
        i += 1
    if (k == 1):
        # always start from vertex s
        c[0] = g.s
        nc[0] = 1
    else:
        nc[0] = 0
        last = a[(k - 1)]
        p = g.g.edges[last]
        while (p != None):
            if (not in_sol[p.y]):
                c[nc[0]] = p.y
                nc[0] = (nc[0] + 1)
            p = p.next


def backtrack(a, k, input):
    # c: candidates for next position
    c = [0 for _ in range(MAXCANDIDATES)]
    # ncandidates: next position candidate count
    ncandidates = [0]
    # i: counter
    if is_a_solution(a, k, input):
        process_solution(a, k, input)
    else:
        k = (k + 1)
        construct_candidates(a, k, input, c, ncandidates)
        i = 0
        while (i < ncandidates[0]):
            a[k] = c[i]
            make_move(a, k, input)
            backtrack(a, k, input)
            unmake_move(a, k, input)
            if finished:
                # return: terminate early
                return
            i += 1


def main():
    # a: solution vector
    a = [0 for _ in range((NMAX + 1))]
    # i: counter
    g = paths_data()
    graph.read_graph(g.g, False)
    graph.print_graph(g.g)
    i = 1
    while (i <= g.g.nvertices):
        g.s = 1
        g.t = i
        printf("\nPaths from 1 to %d:\n", i)
        backtrack(a, 0, g)
        i += 1
    i = 1
    while (i <= g.g.nvertices):
        g.s = i
        g.t = 1
        printf("\nPaths from %d to 1:\n", i)
        backtrack(a, 0, g)
        i += 1
    return 0


if __name__ == "__main__":
    exit(main())
