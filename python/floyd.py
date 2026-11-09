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

"""Direct translation of floyd.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import LLONG_MAX, address, printf, scanf

# maximum number of vertices
# maximum outdegree of a vertex
class edge:
    def __init__(self):
        # v: neighboring vertex
        self.v = 0
        # weight: edge weight
        self.weight = 0
        # in: is the edge "in" the solution?
        self.in_ = 0


class graph:
    def __init__(self):
        # edges: adjacency info
        self.edges = [[edge() for _ in range(MAXDEGREE)] for _ in range((MAXV + 1))]
        # degree: outdegree of each vertex
        self.degree = [0 for _ in range((MAXV + 1))]
        # nvertices: number of vertices in graph
        self.nvertices = 0
        # nedges: number of edges in the graph
        self.nedges = 0


class adjacency_matrix:
    def __init__(self):
        # weight: adjacency/weight info
        self.weight = [[0 for _ in range((MAXV + 1))] for _ in range((MAXV + 1))]
        # nvertices: number of vertices in graph
        self.nvertices = 0


MAXV = 100
MAXDEGREE = 50
MAXINT = LLONG_MAX // 4


def initialize_adjacency_matrix(g):
    # j: counters
    g.nvertices = 0
    i = 1
    while (i <= MAXV):
        j = 1
        while (j <= MAXV):
            g.weight[i][j] = (0 if (i == j) else MAXINT)
            j += 1
        i += 1


def read_adjacency_matrix(g, directed):
    # i: counter
    # m: number of edges
    m = [0]
    # w: placeholder for edge and weight
    x = [0]
    y = [0]
    w = [0]
    initialize_adjacency_matrix(g)
    scanf("%d %d\n", address(g, 'nvertices'), m)
    i = 1
    while (i <= m[0]):
        scanf("%d %d %d\n", x, y, w)
        if (w[0] < g.weight[x[0]][y[0]]):
            g.weight[x[0]][y[0]] = w[0]
        if (not directed):
            if (w[0] < g.weight[y[0]][x[0]]):
                g.weight[y[0]][x[0]] = w[0]
        i += 1


def print_graph(g):
    # j: counters
    i = 1
    while (i <= g.nvertices):
        printf("%d: ", i)
        j = 1
        while (j <= g.nvertices):
            if (g.weight[i][j] < MAXINT):
                printf(" %d", j)
            j += 1
        printf("\n")
        i += 1


def print_adjacency_matrix(g):
    # j: counters
    i = 1
    while (i <= g.nvertices):
        printf("%3d: ", i)
        j = 1
        while (j <= g.nvertices):
            printf(" %3lld", g.weight[i][j])
            j += 1
        printf("\n")
        i += 1


def floyd(g):
    # j: dimension counters
    # k: intermediate vertex counter
    # through_k: distance through vertex k
    # Phase k permits intermediate vertices 1..k on each shortest path.
    k = 1
    while (k <= g.nvertices):
        i = 1
        while (i <= g.nvertices):
            j = 1
            while (j <= g.nvertices):
                # The sentinel represents no path and must never participate in addition.
                if ((g.weight[i][k] == MAXINT) or (g.weight[k][j] == MAXINT)):
                    j += 1
                    continue
                through_k = (g.weight[i][k] + g.weight[k][j])
                if (through_k < g.weight[i][j]):
                    g.weight[i][j] = through_k
                j += 1
            i += 1
        k += 1


def main():
    g = adjacency_matrix()
    read_adjacency_matrix(g, False)
    print_graph(g)
    floyd(g)
    print_adjacency_matrix(g)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
