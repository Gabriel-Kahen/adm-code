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

"""strong1.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"

from .graph import Graph


def strongly_connected_components(graph: Graph) -> list[list[int]]:
    """Kosaraju transpose SCC in O(V+E)."""
    graph.require_directed(True)
    result = []
    visited = set()
    order = []
    for start in range(graph.n):
        if start in visited:
            continue
        pending = [(start, False)]
        while pending:
            vertex, finished = pending.pop()
            if finished:
                order.append(vertex)
            elif vertex not in visited:
                visited.add(vertex)
                pending.append((vertex, True))
                pending.extend((arc[0], False) for arc in reversed(graph.adjacency[vertex]))
    transpose = Graph(graph.n, True)
    for edge in graph.edges.values():
        transpose.add_edge(edge.target, edge.source)
    visited.clear()
    for vertex in reversed(order):
        if vertex in visited:
            continue
        component = []
        pending = [vertex]
        visited.add(vertex)
        while pending:
            member = pending.pop()
            component.append(member)
            for neighbor, _, _ in transpose.adjacency[member]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    pending.append(neighbor)
        result.append(sorted(component))
    return sorted(result)


if __name__ == "__main__":
    import sys

    from .graph import read_graph

    graph = read_graph(sys.stdin, directed=True)
    print(strongly_connected_components(graph))
