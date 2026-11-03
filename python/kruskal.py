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

"""kruskal.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"

from .graph import Graph
from .set_union import DisjointSet


def minimum_spanning_forest(graph: Graph) -> dict:
    """Kruskal minimum spanning forest, O(E log E)."""
    graph.require_directed(False)
    selected = []
    sets = DisjointSet(graph.n)
    for edge in sorted(graph.edges.values(), key=lambda item: (item.weight, item.identifier)):
        if sets.union(edge.source, edge.target):
            selected.append([edge.source, edge.target, edge.weight])
    return {"cost": sum(edge[2] for edge in selected), "edges": selected}


if __name__ == "__main__":
    import sys

    from .wgraph import read_weighted_graph

    graph = read_weighted_graph(sys.stdin)
    print(minimum_spanning_forest(graph))
