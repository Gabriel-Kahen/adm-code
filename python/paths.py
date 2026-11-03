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

"""paths.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"

from .graph import Graph


def simple_paths(graph: Graph, source: int, target: int) -> list[list[int]]:
    """Enumerate distinct simple vertex paths; exponential output is unavoidable."""
    graph.vertex(source)
    graph.vertex(target)
    result = []
    path = [source]
    visited = {source}

    def visit(vertex: int) -> None:
        if vertex == target:
            result.append(list(path))
            return
        for neighbor in sorted({arc[0] for arc in graph.adjacency[vertex]}):
            if neighbor not in visited:
                visited.add(neighbor)
                path.append(neighbor)
                visit(neighbor)
                path.pop()
                visited.remove(neighbor)

    visit(source)
    return sorted(result)


if __name__ == "__main__":
    import sys

    from .graph import read_graph

    graph = read_graph(sys.stdin, directed=False)
    print(simple_paths(graph, 0, graph.n - 1))
