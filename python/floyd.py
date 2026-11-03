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

"""floyd.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"

from .graph import Graph


def floyd_warshall(graph: Graph) -> list[list[int | None]]:
    """O(V³) all-pairs distances; negative cycles raise ValueError."""
    distances: list[list[int | None]] = [[None] * graph.n for _ in range(graph.n)]
    for vertex in range(graph.n):
        distances[vertex][vertex] = 0
        for neighbor, weight, _ in graph.adjacency[vertex]:
            current = distances[vertex][neighbor]
            distances[vertex][neighbor] = weight if current is None else min(current, weight)
    for middle in range(graph.n):
        for source in range(graph.n):
            for target in range(graph.n):
                first, second = distances[source][middle], distances[middle][target]
                if first is None or second is None:
                    continue
                candidate = first + second
                current = distances[source][target]
                if current is None or candidate < current:
                    distances[source][target] = candidate
    if any(distances[vertex][vertex] < 0 for vertex in range(graph.n)):
        raise ValueError("negative cycle")
    return distances


if __name__ == "__main__":
    import sys

    from .wgraph import read_weighted_graph

    graph = read_weighted_graph(sys.stdin)
    print(floyd_warshall(graph))
