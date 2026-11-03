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

"""topsort1.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"

from .graph import Graph


def topological_sort(graph: Graph) -> list[int]:
    """O(V+E) topological order; raise ValueError if any directed cycle exists."""
    graph.require_directed(True)
    result = []
    state = [0] * graph.n

    def visit(vertex: int) -> None:
        if state[vertex] == 1:
            raise ValueError("directed cycle")
        if state[vertex] == 2:
            return
        state[vertex] = 1
        for neighbor, _, _ in graph.adjacency[vertex]:
            visit(neighbor)
        state[vertex] = 2
        result.append(vertex)

    for vertex in range(graph.n):
        visit(vertex)
    result.reverse()
    return result


if __name__ == "__main__":
    import sys

    from .graph import read_graph

    graph = read_graph(sys.stdin, directed=True)
    print(topological_sort(graph))
