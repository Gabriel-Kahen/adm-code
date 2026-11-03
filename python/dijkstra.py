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

"""dijkstra.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"

import heapq

from .graph import Graph


def dijkstra(graph: Graph, source: int) -> tuple[list[int | None], list[int | None]]:
    """O((V+E) log E), nonnegative edges only; validates even unreachable edges."""
    graph.vertex(source)
    if any(edge.weight < 0 for edge in graph.edges.values()):
        raise ValueError("Dijkstra requires nonnegative edges")
    distances: list[int | None] = [None] * graph.n
    parents: list[int | None] = [None] * graph.n
    distances[source] = 0
    pending = [(0, source)]
    while pending:
        cost, vertex = heapq.heappop(pending)
        if cost != distances[vertex]:
            continue
        for neighbor, weight, _ in graph.adjacency[vertex]:
            candidate = cost + weight
            if distances[neighbor] is None or candidate < distances[neighbor]:
                distances[neighbor] = candidate
                parents[neighbor] = vertex
                heapq.heappush(pending, (candidate, neighbor))
    return distances, parents


if __name__ == "__main__":
    import sys

    from .wgraph import read_weighted_graph

    graph = read_weighted_graph(sys.stdin)
    print(dijkstra(graph, 0)[0])
