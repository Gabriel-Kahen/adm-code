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

"""Direct translation of strong.c; data structures and indexing match C."""

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
# low: oldest vertex surely in component of v
low = [0 for _ in range((graph.MAXV + 1))]
# scc: strong component number for each vertex
scc = [0 for _ in range((graph.MAXV + 1))]
# active: active vertices of unassigned component
active = stack.stack()
# components_found: number of strong components identified
components_found = 0


def process_vertex_early(v):
    stack.push(active, v)


def pop_component(v):
    global components_found
    # t: vertex placeholder
    components_found = (components_found + 1)
    printf("%d is in component %d \n", v, components_found)
    scc[v] = components_found
    while ((t := stack.pop(active)) != v):
        scc[t] = components_found
        printf("%d is in component %d \n", t, components_found)


def process_vertex_late(v):
    if (low[v] == v):
        pop_component(v)
    if ((bfs_dfs.parent[v] != (-1)) and (bfs_dfs.entry_time[low[v]] < bfs_dfs.entry_time[low[bfs_dfs.parent[v]]])):
        low[bfs_dfs.parent[v]] = low[v]


def process_edge(x, y):
    # class: edge class
    class_ = bfs_dfs.edge_classification(x, y)
    if (class_ == graph.BACK):
        if (bfs_dfs.entry_time[y] < bfs_dfs.entry_time[low[x]]):
            low[x] = y
    if (class_ == graph.CROSS):
        # component not yet assigned
        if (scc[y] == (-1)):
            if (bfs_dfs.entry_time[y] < bfs_dfs.entry_time[low[x]]):
                low[x] = y


def strong_components(g):
    global components_found
    # i: counter
    i = 1
    while (i <= g.nvertices):
        low[i] = i
        scc[i] = (-1)
        i += 1
    components_found = 0
    stack.init_stack(active)
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
    graph.read_graph(g, True)
    graph.print_graph(g)
    strong_components(g)
    return 0


if __name__ == "__main__":
    exit(main())
