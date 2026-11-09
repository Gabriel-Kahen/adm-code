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

"""Direct translation of wgraph.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import *
from . import _c
from . import graph

# i: counter
# p: temporary pointer
# i: counter
# m: number of edges
# w: placeholder for edge and weight
# p_back: temporary pointers
# i: counter
# p: temporary pointer
# processed: which vertices have been processed
processed = [0 for _ in range((graph.MAXV + 1))]
# discovered: which vertices have been found
discovered = [0 for _ in range((graph.MAXV + 1))]
# parent: discovery relation
parent = [0 for _ in range((graph.MAXV + 1))]
# entry_time: time of vertex entry
entry_time = [0 for _ in range((graph.MAXV + 1))]
# exit_time: time of vertex exit
exit_time = [0 for _ in range((graph.MAXV + 1))]
# time: current event time
time = 0
# if true, cut off search immediately
finished = False


def initialize_graph(g, directed):
    g.nvertices = 0
    g.nedges = 0
    g.directed = directed
    i = 1
    while (i <= graph.MAXV):
        g.degree[i] = 0
        i += 1
    i = 1
    while (i <= graph.MAXV):
        g.edges[i] = None
        i += 1


def insert_edge(g, x, y, directed, w):
    p = graph.edgenode()
    p.y = y
    p.weight = w
    p.next = g.edges[x]
    g.edges[x] = p
    g.degree[x] += 1
    if (not directed):
        insert_edge(g, y, x, True, w)
    else:
        g.nedges += 1


def read_graph(g, directed):
    m = [0]
    x = [0]
    y = [0]
    w = [0]
    initialize_graph(g, directed)
    scanf("%d %d\n", address(g, 'nvertices'), m)
    i = 1
    while (i <= m[0]):
        scanf("%d %d %d\n", x, y, w)
        insert_edge(g, x[0], y[0], directed, w[0])
        i += 1


def delete_edge(g, x, y, directed):
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
    i = 1
    while (i <= g.nvertices):
        printf("%d: ", i)
        p = g.edges[i]
        while (p != None):
            printf(" %d", p.y)
            p = p.next
        printf("\n")
        i += 1


def initialize_search(g):
    global time
    # i: counter
    time = 0
    i = 0
    while (i <= g.nvertices):
        discovered[i] = False
        processed[i] = discovered[i]
        parent[i] = (-1)
        i += 1


# vertex to process
def process_vertex_early(v):
    printf(" %d", v)


# vertex to process
def process_vertex_late(v):
    pass


# edge to process
def process_edge(x, y):
    pass


def dfs(g, v):
    global time
    # p: temporary pointer
    # y: successor vertex
    parent_edge_seen = False
    self_edge_seen = False
    if finished:
        # return: allow for search termination
        return
    discovered[v] = True
    time = (time + 1)
    entry_time[v] = time
    process_vertex_early(v)
    p = g.edges[v]
    while (p != None):
        y = p.y
        if (not discovered[y]):
            parent[y] = v
            process_edge(v, y)
            dfs(g, y)
        else:
            if ((not processed[y]) or g.directed):
                if ((y == v) and (not g.directed)):
                    self_edge_seen = (not self_edge_seen)
                    if self_edge_seen:
                        process_edge(v, y)
                else:
                    if ((g.directed or (y != parent[v])) or parent_edge_seen):
                        process_edge(v, y)
                    if (y == parent[v]):
                        parent_edge_seen = True
        if finished:
            return
        p = p.next
    process_vertex_late(v)
    time = (time + 1)
    exit_time[v] = time
    processed[v] = True


def find_path(start, end, parents):
    if (end == (-1)):
        printf("\nNo path")
        return 0
    if (start == end):
        printf("\n%d", start)
    else:
        if (not find_path(start, parents[end], parents)):
            return 0
        printf(" %d", end)
    return 1


# graph to analyze
def connected_components(g):
    # c: component number
    # i: counter
    initialize_search(g)
    c = 0
    i = 1
    while (i <= g.nvertices):
        if (not discovered[i]):
            c = (c + 1)
            printf("Component %d:", c)
            dfs(g, i)
            printf("\n")
        i += 1
