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

"""Direct translation of prim.c; data structures and indexing match C."""

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


def prim(g, start):
    in_tree = [0 for _ in range((graph.MAXV + 1))]
    # distance: cheapest known edge from the tree
    distance = [0 for _ in range((graph.MAXV + 1))]
    tree_weight = 0
    i = 1
    while (i <= g.nvertices):
        in_tree[i] = False
        distance[i] = MAXINT
        wgraph.parent[i] = (-1)
        i += 1
    distance[start] = 0
    vertex = start
    # Grow the tree in start's connected component; other parents remain -1.
    while (not in_tree[vertex]):
        in_tree[vertex] = True
        if (vertex != start):
            printf("edge (%d,%d) in tree \n", wgraph.parent[vertex], vertex)
            tree_weight = (tree_weight + next_distance)
        edge = g.edges[vertex]
        while (edge != None):
            neighbor = edge.y
            if ((distance[neighbor] > edge.weight) and (not in_tree[neighbor])):
                distance[neighbor] = edge.weight
                wgraph.parent[neighbor] = vertex
            edge = edge.next
        next_distance = MAXINT
        i = 1
        while (i <= g.nvertices):
            if ((not in_tree[i]) and (next_distance > distance[i])):
                next_distance = distance[i]
                vertex = i
            i += 1
    return tree_weight


def main():
    g = graph.graph()
    wgraph.read_graph(g, False)
    weight = prim(g, 1)
    printf("Out of Prim: weight = %lld \n", weight)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
