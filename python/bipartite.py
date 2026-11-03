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

"""bipartite.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"

from collections import deque

from .graph import Graph


def bipartite_coloring(graph: Graph) -> list[int] | None:
    """O(V+E) two-coloring of every component; None denotes an odd cycle."""
    graph.require_directed(False)
    colors = [-1] * graph.n
    for start in range(graph.n):
        if colors[start] != -1:
            continue
        colors[start] = 0
        pending = deque([start])
        while pending:
            vertex = pending.popleft()
            for neighbor, _, _ in graph.adjacency[vertex]:
                if colors[neighbor] == -1:
                    colors[neighbor] = 1 - colors[vertex]
                    pending.append(neighbor)
                elif colors[neighbor] == colors[vertex]:
                    return None
    return colors


if __name__ == "__main__":
    import sys

    from .graph import read_graph

    graph = read_graph(sys.stdin, directed=False)
    print(bipartite_coloring(graph))
