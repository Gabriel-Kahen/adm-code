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

"""Direct translation of strong1.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import *
from . import _c
from . import bfs_dfs
from . import graph
from . import stack

# processed: which vertices have been processed
# discovered: which vertices have been found
# parent: discovery relation
# entry_time: time of vertex entry
# exit_time: time of vertex exit
# finished: if true, cut off search immediately
# low: oldest vertex surely in component of v
low = [0 for _ in range((graph.MAXV + 1))]
# scc: strong component number for each vertex
scc = [0 for _ in range((graph.MAXV + 1))]
# dfs1order: stack for reverse finishing order
dfs1order = stack.stack()
# active: active vertices of unassigned component
active = stack.stack()
# components_found: number of strong components identified
components_found = 0


# replicate dfs call so it can use different process vertex functions
def dfs2(g, v):
    # p: temporary pointer
    # y: successor vertex
    if bfs_dfs.finished:
        # return: allow for search termination
        return
    bfs_dfs.discovered[v] = True
    bfs_dfs.time = (bfs_dfs.time + 1)
    bfs_dfs.entry_time[v] = bfs_dfs.time
    process_vertex_early2(v)
    p = g.edges[v]
    while (p != None):
        y = p.y
        if (not bfs_dfs.discovered[y]):
            bfs_dfs.parent[y] = v
            process_edge2(v, y)
            dfs2(g, y)
        else:
            if (((not bfs_dfs.processed[y]) and (bfs_dfs.parent[v] != y)) or g.directed):
                process_edge2(v, y)
        if bfs_dfs.finished:
            return
        p = p.next
    process_vertex_late2(v)
    bfs_dfs.time = (bfs_dfs.time + 1)
    bfs_dfs.exit_time[v] = bfs_dfs.time
    bfs_dfs.processed[v] = True


def process_vertex_early(v):
    pass


def process_vertex_late(v):
    stack.push(dfs1order, v)


def process_edge(x, y):
    pass


def process_vertex_early2(v):
    printf(" %d", v)


def process_vertex_late2(v):
    pass


def process_edge2(x, y):
    pass


def strong_components(g):
    global components_found
    # gt: transpose of graph g
    # i: counter
    # v: vertex in component
    stack.init_stack(dfs1order)
    bfs_dfs.initialize_search(g)
    i = 1
    while (i <= g.nvertices):
        if (not bfs_dfs.discovered[i]):
            bfs_dfs.dfs(g, i)
        i += 1
    gt = graph.transpose(g)
    bfs_dfs.initialize_search(gt)
    components_found = 0
    while (not stack.empty_stack(dfs1order)):
        v = stack.pop(dfs1order)
        if (not bfs_dfs.discovered[v]):
            components_found += 1
            printf("Component %d:", components_found)
            dfs2(gt, v)
            printf("\n")


def main():
    # Bind this application's callbacks to the shared C-style backend.
    bfs_dfs.process_vertex_early = process_vertex_early
    bfs_dfs.process_vertex_late = process_vertex_late
    bfs_dfs.process_edge = process_edge
    graph.process_vertex_early = process_vertex_early
    graph.process_vertex_late = process_vertex_late
    graph.process_edge = process_edge
    g = graph.graph()
    graph.read_graph(g, True)
    graph.print_graph(g)
    strong_components(g)
    return 0


if __name__ == "__main__":
    exit(main())
