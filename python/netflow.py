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

"""netflow.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"

from collections import deque
from dataclasses import dataclass

from .graph import Graph


@dataclass
class FlowResult:
    value: int
    # Coalesced signed net flows: reverse entries can be negative.
    flow: list[list[int]]
    residual: list[list[int]]


def maximum_flow(graph: Graph, source: int, sink: int) -> FlowResult:
    """Edmonds-Karp O(V E²); supports parallel/antiparallel arcs and integer capacities."""
    graph.require_directed(True)
    graph.vertex(source)
    graph.vertex(sink)
    if source == sink:
        raise ValueError("source and sink must differ")
    residual = [[0] * graph.n for _ in range(graph.n)]
    neighbors = [set() for _ in range(graph.n)]
    for edge in graph.edges.values():
        if edge.weight < 0:
            raise ValueError("negative capacity")
        residual[edge.source][edge.target] += edge.weight
        neighbors[edge.source].add(edge.target)
        neighbors[edge.target].add(edge.source)
    adjacency = [sorted(row) for row in neighbors]
    flow = [[0] * graph.n for _ in range(graph.n)]
    value = 0
    while True:
        parents = [-1] * graph.n
        parents[source] = source
        pending = deque([source])
        while pending and parents[sink] == -1:
            vertex = pending.popleft()
            for neighbor in adjacency[vertex]:
                if parents[neighbor] == -1 and residual[vertex][neighbor] > 0:
                    parents[neighbor] = vertex
                    pending.append(neighbor)
        if parents[sink] == -1:
            break
        path = []
        current = sink
        while current != source:
            previous = parents[current]
            path.append((previous, current))
            current = previous
        amount = min(residual[u][v] for u, v in path)
        for u, v in path:
            residual[u][v] -= amount
            residual[v][u] += amount
            flow[u][v] += amount
            flow[v][u] -= amount
        value += amount
    return FlowResult(value, flow, residual)


if __name__ == "__main__":
    import sys

    from .wgraph import read_weighted_graph

    source, sink = map(int, sys.stdin.readline().split())
    graph = read_weighted_graph(sys.stdin, directed=True)
    print(maximum_flow(graph, source - 1, sink - 1).value)
