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

"""Direct translation of kruskal.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from functools import cmp_to_key

from ._c import EXIT_FAILURE, perror, printf
from . import graph
from . import set_union
from . import wgraph

class edge_pair:
    def __init__(self):
        # y: adjacency info
        self.x = 0
        self.y = 0
        # weight: edge weight, if any
        self.weight = 0


MAXINT = 100007


def to_edge_array(g, edges):
    # edge_count: counters
    # edge: temporary pointer
    edge_count = 0
    i = 1
    while (i <= g.nvertices):
        edge = g.edges[i]
        while (edge != None):
            # An undirected edge appears twice in the adjacency lists; omit loops.
            if (edge.y > i):
                edges[edge_count].x = i
                edges[edge_count].y = edge.y
                edges[edge_count].weight = edge.weight
                edge_count = (edge_count + 1)
            edge = edge.next
        i += 1
    return edge_count


def weight_compare(x, y):
    left = x
    right = y
    if (left.weight < right.weight):
        return (-1)
    if (left.weight > right.weight):
        return 1
    return 0


def kruskal(g):
    # i: counter
    # components: union-find data structure
    components = set_union.union_find()
    # edges: storage for all input edges
    # edge_count: extracted non-loop edge count
    # cost of the minimum spanning tree
    weight = 0
    set_union.union_find_init(components, g.nvertices)
    edges = [edge_pair() for _ in range((g.nedges if g.nedges else 1))]
    if (edges == None):
        perror("kruskal edge allocation")
        raise SystemExit(EXIT_FAILURE)
    # The extracted count excludes self-loops and determines the initialized range.
    edge_count = to_edge_array(g, edges)
    edges[:edge_count] = sorted(edges[:edge_count], key=cmp_to_key(weight_compare))
    i = 0
    while (i < edge_count):
        if (not set_union.same_component(components, edges[i].x, edges[i].y)):
            printf("edge (%d,%d) in MST\n", edges[i].x, edges[i].y)
            weight = (weight + edges[i].weight)
            set_union.union_sets(components, edges[i].x, edges[i].y)
        i += 1
    # Python releases this node when its references disappear.
    return weight


def main():
    g = graph.graph()
    wgraph.read_graph(g, False)
    # print_graph(&g);
    weight = kruskal(g)
    printf("Out of Kruskal: weight=%lld \n", weight)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
