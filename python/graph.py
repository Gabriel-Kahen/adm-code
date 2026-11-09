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

"""Direct translation of graph.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import printf, scanf

# #define _NULL       0       null pointer
# DFS edge types
# tree edge
# back edge
# cross edge
# forward edge
# maximum number of vertices
class edgenode:
    def __init__(self):
        # y: adjacency info
        self.y = 0
        # weight: edge weight, if any
        self.weight = 0
        # next: next edge in list
        self.next = None


class graph:
    def __init__(self):
        # edges: adjacency info
        self.edges = [None for _ in range((MAXV + 1))]
        # degree: outdegree of each vertex
        self.degree = [0 for _ in range((MAXV + 1))]
        # nvertices: number of vertices in the graph
        self.nvertices = 0
        # nedges: number of edges in the graph
        self.nedges = 0
        # directed: is the graph directed?
        self.directed = 0


TREE = 0
BACK = 1
CROSS = 2
FORWARD = 3
MAXV = 100


def initialize_graph(g, directed):
    # i: counter
    g.nvertices = 0
    g.nedges = 0
    g.directed = directed
    i = 1
    while (i <= MAXV):
        g.degree[i] = 0
        i += 1
    i = 1
    while (i <= MAXV):
        g.edges[i] = None
        i += 1


def insert_edge(g, x, y, directed):
    # p: temporary pointer
    # allocate edgenode storage
    p = edgenode()
    p.weight = 0
    p.y = y
    p.next = g.edges[x]
    # insert at head of list
    g.edges[x] = p
    g.degree[x] += 1
    if (not directed):
        insert_edge(g, y, x, True)
    else:
        g.nedges += 1


def read_graph(g, directed):
    # i: counter
    # m: number of edges
    m = 0
    # x, y: vertices in edge (x,y)
    x = 0
    y = 0
    initialize_graph(g, directed)
    _, g.nvertices, m = scanf("%d %d", g.nvertices, m)
    i = 1
    while (i <= m):
        _, x, y = scanf("%d %d", x, y)
        insert_edge(g, x, y, directed)
        i += 1


def delete_edge(g, x, y, directed):
    # p, p_back: temporary pointers
    p = g.edges[x]
    p_back = None
    while (p != None):
        if (p.y == y):
            g.degree[x] -= 1
            if (p_back != None):
                p_back.next = p.next
            else:
                g.edges[x] = p.next
            # Python releases this node when its references disappear.
            if (not directed):
                delete_edge(g, y, x, True)
            else:
                g.nedges -= 1
            return
        else:
            p_back = p
            p = p.next
    printf("Warning: deletion(%d,%d) not found in g.\n", x, y)


def print_graph(g):
    # i: counter
    # p: temporary pointer
    i = 1
    while (i <= g.nvertices):
        printf("%d: ", i)
        p = g.edges[i]
        while (p != None):
            printf(" %d", p.y)
            p = p.next
        printf("\n")
        i += 1


def transpose(g):
    # gt: transpose of graph g
    # x: counter
    # p: temporary pointer
    gt = graph()
    # initialize directed graph
    initialize_graph(gt, True)
    gt.nvertices = g.nvertices
    x = 1
    while (x <= g.nvertices):
        p = g.edges[x]
        while (p != None):
            insert_edge(gt, p.y, x, True)
            p = p.next
        x += 1
    return gt
