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

"""Direct translation of bfs-dfs.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import printf
from . import graph
from . import queue

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


def initialize_search(g):
    global time
    # i: counter
    time = 0
    i = 0
    while (i <= g.nvertices):
        processed[i] = False
        discovered[i] = False
        parent[i] = (-1)
        i += 1


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
            y = p.y
            if (((not processed[y]) or g.directed) or (y == v)):
                process_edge(v, y)
            if (not discovered[y]):
                queue.enqueue(q, y)
                discovered[y] = True
                parent[y] = v
            p = p.next
        process_vertex_late(v)


def edge_classification(x, y):
    if (parent[y] == x):
        return graph.TREE
    if (discovered[y] and (not processed[y])):
        return graph.BACK
    if (processed[y] and (entry_time[y] > entry_time[x])):
        return graph.FORWARD
    if (processed[y] and (entry_time[y] < entry_time[x])):
        return graph.CROSS
    printf("Warning: self loop (%d,%d)\n", x, y)
    return (-1)


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
