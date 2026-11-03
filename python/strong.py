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

"""strong.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"

from .graph import Graph


def strongly_connected_components(graph: Graph) -> list[list[int]]:
    """Tarjan low-link SCC in O(V+E)."""
    graph.require_directed(True)
    result = []
    index = [-1] * graph.n
    low = [0] * graph.n
    active: set[int] = set()
    stack = []
    clock = 0

    def visit(vertex: int) -> None:
        nonlocal clock
        index[vertex] = low[vertex] = clock
        clock += 1
        stack.append(vertex)
        active.add(vertex)
        for neighbor, _, _ in graph.adjacency[vertex]:
            if index[neighbor] < 0:
                visit(neighbor)
                low[vertex] = min(low[vertex], low[neighbor])
            elif neighbor in active:
                low[vertex] = min(low[vertex], index[neighbor])
        if low[vertex] == index[vertex]:
            component = []
            while True:
                member = stack.pop()
                active.remove(member)
                component.append(member)
                if member == vertex:
                    break
            result.append(sorted(component))

    for vertex in range(graph.n):
        if index[vertex] < 0:
            visit(vertex)
    return sorted(result)


if __name__ == "__main__":
    import sys

    from .graph import read_graph

    graph = read_graph(sys.stdin, directed=True)
    print(strongly_connected_components(graph))
