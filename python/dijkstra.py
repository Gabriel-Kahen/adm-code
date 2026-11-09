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

"""Direct translation of dijkstra.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import LLONG_MAX, printf
from . import graph
from . import wgraph

MAXINT = LLONG_MAX // 4


# Dijkstra requires nonnegative edge weights. Unreachable vertices keep parent -1.
def dijkstra(g, start):
    settled = [0 for _ in range((graph.MAXV + 1))]
    # distance: shortest known distance from start
    distance = [0 for _ in range((graph.MAXV + 1))]
    tree_weight = 0
    i = 1
    while (i <= g.nvertices):
        settled[i] = False
        distance[i] = MAXINT
        wgraph.parent[i] = (-1)
        i += 1
    distance[start] = 0
    vertex = start
    while (not settled[vertex]):
        settled[vertex] = True
        if (vertex != start):
            printf("edge (%d,%d) in tree \n", wgraph.parent[vertex], vertex)
            # The distance difference is this parent edge's weight, not a full path length.
            tree_weight += (distance[vertex] - distance[wgraph.parent[vertex]])
        edge = g.edges[vertex]
        while (edge != None):
            neighbor = edge.y
            if (distance[neighbor] > (distance[vertex] + edge.weight)):
                distance[neighbor] = (distance[vertex] + edge.weight)
                wgraph.parent[neighbor] = vertex
            edge = edge.next
        # If none is reachable, vertex stays settled and the outer loop stops.
        next_distance = MAXINT
        i = 1
        while (i <= g.nvertices):
            if ((not settled[i]) and (next_distance > distance[i])):
                next_distance = distance[i]
                vertex = i
            i += 1
    return tree_weight


def main():
    g = graph.graph()
    wgraph.read_graph(g, False)
    weight = dijkstra(g, 1)
    printf("Total SPST edgeweight = %lld \n", weight)
    i = 1
    while (i <= g.nvertices):
        wgraph.find_path(1, i, wgraph.parent)
        i += 1
    printf("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
