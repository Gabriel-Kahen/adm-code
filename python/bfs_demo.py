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

"""Direct translation of bfs-demo.c; data structures and indexing match C."""

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
def process_vertex_early(v):
    printf("processed vertex %d\n", v)


def process_vertex_late(v):
    pass


def process_edge(x, y):
    printf("processed edge (%d,%d)\n", x, y)


def main():
    # Bind this application's callbacks to the shared C-style backend.
    graph.process_vertex_early = process_vertex_early
    graph.process_vertex_late = process_vertex_late
    graph.process_edge = process_edge
    bfs_dfs.process_vertex_early = process_vertex_early
    bfs_dfs.process_vertex_late = process_vertex_late
    bfs_dfs.process_edge = process_edge
    g = graph.graph()
    graph.read_graph(g, False)
    graph.print_graph(g)
    bfs_dfs.initialize_search(g)
    bfs_dfs.bfs(g, 1)
    i = 1
    while (i <= g.nvertices):
        printf(" %d", bfs_dfs.parent[i])
        i += 1
    printf("\n")
    i = 1
    while (i <= g.nvertices):
        bfs_dfs.find_path(1, i, bfs_dfs.parent)
        i += 1
    printf("\n")
    return 0


if __name__ == "__main__":
    exit(main())
