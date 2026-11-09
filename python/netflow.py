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

"""Direct translation of netflow.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import *
from . import _c
from . import queue

# maximum number of vertices
# maximum outdegree of a vertex
class edgenode:
    def __init__(self):
        # v: neighboring vertex
        self.v = 0
        # capacity: capacity of edge
        self.capacity = 0
        # flow: signed net flow; reverse edge stores its negative
        self.flow = 0
        # residual: residual capacity of edge
        self.residual = 0
        # next: next edge in list
        self.next = None


class flow_graph:
    def __init__(self):
        # edges: adjacency info
        self.edges = [None for _ in range((MAXV + 1))]
        # degree: outdegree of each vertex
        self.degree = [0 for _ in range((MAXV + 1))]
        # nvertices: number of vertices in the graph
        self.nvertices = 0
        # nedges: number of edges in the graph
        self.nedges = 0


MAXV = 100
MAXDEGREE = 50
# graph to initialize
# i: counter
# edge: temporary pointer
# Parallel arcs share a single residual-capacity entry.
# allocate storage for edgenode
# insert at head of list
# i: counter
# m: number of edges
# w: placeholder for edge and weight
# p: temporary pointer
# i: counter
# p: temporary pointer
# i: counter
# p: temporary pointer
# processed: which vertices have been processed
processed = [0 for _ in range((MAXV + 1))]
# discovered: which vertices have been found
discovered = [0 for _ in range((MAXV + 1))]
# parent: discovery relation
parent = [0 for _ in range((MAXV + 1))]
# if true, cut off search immediately
finished = False


def initialize_graph(g):
    g.nvertices = 0
    g.nedges = 0
    i = 0
    while (i <= MAXV):
        g.degree[i] = 0
        i += 1
    i = 0
    while (i <= MAXV):
        g.edges[i] = None
        i += 1


def insert_flow_edge(g, x, y, directed, w):
    parallel_edge = find_edge(g, x, y)
    if (parallel_edge != None):
        parallel_edge.capacity += w
        parallel_edge.residual += w
        if (not directed):
            insert_flow_edge(g, y, x, True, w)
        return
    edge = edgenode()
    edge.v = y
    edge.capacity = w
    edge.flow = 0
    edge.residual = w
    edge.next = g.edges[x]
    g.edges[x] = edge
    g.degree[x] += 1
    if (not directed):
        insert_flow_edge(g, y, x, True, w)
    else:
        g.nedges += 1


def read_flow_graph(g, directed):
    m = [0]
    x = [0]
    y = [0]
    w = [0]
    initialize_graph(g)
    scanf("%d %d\n", address(g, 'nvertices'), m)
    i = 1
    while (i <= m[0]):
        scanf("%d %d %d\n", x, y, w)
        insert_flow_edge(g, x[0], y[0], directed, w[0])
        i += 1


def find_edge(g, x, y):
    p = g.edges[x]
    while (p != None):
        if (p.v == y):
            return p
        p = p.next
    return None


def add_residual_edges(g):
    i = 1
    while (i <= g.nvertices):
        p = g.edges[i]
        while (p != None):
            if (find_edge(g, p.v, i) == None):
                insert_flow_edge(g, p.v, i, True, 0)
            p = p.next
        i += 1


def print_flow_graph(g):
    i = 1
    while (i <= g.nvertices):
        printf("%d: ", i)
        p = g.edges[i]
        while (p != None):
            printf(" %d(%lld,%lld,%lld)", p.v, p.capacity, p.flow, p.residual)
            p = p.next
        printf("\n")
        i += 1


# graph to traverse
def initialize_search(g):
    # i: counter
    i = 1
    while (i <= g.nvertices):
        processed[i] = False
        discovered[i] = False
        parent[i] = (-1)
        i += 1


# vertex to process
def process_vertex_early(v):
    pass


# vertex to process
def process_vertex_late(v):
    pass


# edge to process
def process_edge(x, y):
    pass


def valid_edge(e):
    return (e.residual > 0)


def bfs(g, start):
    # q: queue of vertices to visit
    q = queue.queue()
    # v: current vertex
    # y: successor vertex
    # p: temporary pointer
    queue.init_queue(q)
    queue.enqueue(q, start)
    discovered[start] = True
    while (not queue.empty_queue(q)):
        v = queue.dequeue(q)
        process_vertex_early(v)
        processed[v] = True
        p = g.edges[v]
        while (p != None):
            y = p.v
            if valid_edge(p):
                if (not processed[y]):
                    process_edge(v, y)
                if (not discovered[y]):
                    queue.enqueue(q, y)
                    discovered[y] = True
                    parent[y] = v
            p = p.next
        process_vertex_late(v)


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


def path_volume(g, start, end):
    # e: edge in question
    if (parent[end] == (-1)):
        return 0
    e = find_edge(g, parent[end], end)
    if (start == parent[end]):
        return e.residual
    else:
        return min(path_volume(g, start, parent[end]), e.residual)


def augment_path(g, start, end, volume):
    if (start == end):
        return
    forward = find_edge(g, parent[end], end)
    forward.flow += volume
    forward.residual -= volume
    # Reverse residual capacity permits undoing an earlier routing decision.
    # Each direction stores the negative of its partner's net flow.
    reverse = find_edge(g, end, parent[end])
    reverse.flow -= volume
    reverse.residual += volume
    augment_path(g, start, parent[end], volume)


def netflow(g, source, sink):
    # volume: weight of the augmenting path
    # Every arc needs a reverse entry before augmentations can cancel flow.
    add_residual_edges(g)
    initialize_search(g)
    bfs(g, source)
    volume = path_volume(g, source, sink)
    while (volume > 0):
        augment_path(g, source, sink, volume)
        initialize_search(g)
        bfs(g, source)
        volume = path_volume(g, source, sink)


def main():
    # g: graph to analyze
    g = flow_graph()
    # sink: source and sink vertices
    source = [0]
    sink = [0]
    # flow: total flow
    # p: temporary pointer
    scanf("%d %d", source, sink)
    read_flow_graph(g, True)
    netflow(g, source[0], sink[0])
    print_flow_graph(g)
    flow = 0
    p = g.edges[source[0]]
    while (p != None):
        flow += p.flow
        p = p.next
    printf("total flow = %lld\n", flow)
    return 0


if __name__ == "__main__":
    exit(main())
