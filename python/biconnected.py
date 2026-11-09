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

"""Direct translation of biconnected.c; data structures and indexing match C."""

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

# processed: which vertices have been processed
# discovered: which vertices have been found
# parent: discovery relation
# entry_time: time of vertex entry
# exit_time: time of vertex exit
# reachable_ancestor: earliest reachable ancestor of v
reachable_ancestor = [0 for _ in range((graph.MAXV + 1))]
# tree_out_degree: DFS tree outdegree of v
tree_out_degree = [0 for _ in range((graph.MAXV + 1))]


def process_vertex_early(v):
    reachable_ancestor[v] = v


def process_vertex_late(v):
    # root: is parent[v] the root of the DFS tree?
    # time_v: earliest reachable time for v
    # time_parent: earliest reachable time for parent[v]
    # test if v is the root
    if (bfs_dfs.parent[v] == (-1)):
        if (tree_out_degree[v] > 1):
            printf("root articulation vertex: %d \n", v)
        return
    # is parent[v] the root?
    root = (bfs_dfs.parent[bfs_dfs.parent[v]] == (-1))
    if (not root):
        if (reachable_ancestor[v] == bfs_dfs.parent[v]):
            printf("parent articulation vertex: %d \n", bfs_dfs.parent[v])
        if (reachable_ancestor[v] == v):
            printf("bridge articulation vertex: %d \n", bfs_dfs.parent[v])
            # is v is not a leaf?
            if (tree_out_degree[v] > 0):
                printf("bridge articulation vertex: %d \n", v)
    time_v = bfs_dfs.entry_time[reachable_ancestor[v]]
    time_parent = bfs_dfs.entry_time[reachable_ancestor[bfs_dfs.parent[v]]]
    if (time_v < time_parent):
        reachable_ancestor[bfs_dfs.parent[v]] = reachable_ancestor[v]


def process_edge(x, y):
    # class: edge class
    class_ = bfs_dfs.edge_classification(x, y)
    if (class_ == graph.TREE):
        tree_out_degree[x] = (tree_out_degree[x] + 1)
    if ((class_ == graph.BACK) and (bfs_dfs.parent[x] != y)):
        if (bfs_dfs.entry_time[y] < bfs_dfs.entry_time[reachable_ancestor[x]]):
            reachable_ancestor[x] = y


def articulation_vertices(g):
    # i: counter
    i = 1
    while (i <= g.nvertices):
        tree_out_degree[i] = 0
        i += 1
    bfs_dfs.initialize_search(g)
    i = 1
    while (i <= g.nvertices):
        if (not bfs_dfs.discovered[i]):
            bfs_dfs.dfs(g, i)
        i += 1


def main():
    # Bind this application's callbacks to the shared C-style backend.
    bfs_dfs.process_vertex_early = process_vertex_early
    bfs_dfs.process_vertex_late = process_vertex_late
    bfs_dfs.process_edge = process_edge
    graph.process_vertex_early = process_vertex_early
    graph.process_vertex_late = process_vertex_late
    graph.process_edge = process_edge
    g = graph.graph()
    graph.read_graph(g, False)
    graph.print_graph(g)
    articulation_vertices(g)
    return 0


if __name__ == "__main__":
    exit(main())
