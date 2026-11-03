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

"""biconnected.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"

from .graph import Graph


def articulation_points(graph: Graph) -> list[int]:
    """Low-link DFS in O(V+E), using edge identity to handle parallel edges."""
    graph.require_directed(False)
    discovery = [-1] * graph.n
    low = [0] * graph.n
    result = set()
    clock = 0

    def visit(vertex: int, parent_edge: int | None) -> None:
        nonlocal clock
        discovery[vertex] = low[vertex] = clock
        clock += 1
        children = 0
        for neighbor, _, edge in graph.adjacency[vertex]:
            if edge == parent_edge:
                continue
            if discovery[neighbor] < 0:
                children += 1
                visit(neighbor, edge)
                low[vertex] = min(low[vertex], low[neighbor])
                if parent_edge is not None and low[neighbor] >= discovery[vertex]:
                    result.add(vertex)
            else:
                low[vertex] = min(low[vertex], discovery[neighbor])
        if parent_edge is None and children > 1:
            result.add(vertex)

    for start in range(graph.n):
        if discovery[start] < 0:
            visit(start, None)
    return sorted(result)


if __name__ == "__main__":
    import sys

    from .graph import read_graph

    graph = read_graph(sys.stdin, directed=False)
    print(articulation_points(graph))
