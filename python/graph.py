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

"""graph.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"

from dataclasses import dataclass


@dataclass(frozen=True)
class Edge:
    source: int
    target: int
    weight: int
    identifier: int


class Graph:
    """Mutable multigraph. Deletion uses stable edge IDs; an undirected edge is stored twice."""

    def __init__(self, size: int, directed: bool = False) -> None:
        if size < 0:
            raise ValueError("negative vertex count")
        self.n = size
        self.directed = directed
        self.adjacency: list[list[tuple[int, int, int]]] = [[] for _ in range(size)]
        self.edges: dict[int, Edge] = {}
        self._next_id = 0

    def vertex(self, value: int) -> None:
        if not 0 <= value < self.n:
            raise ValueError("vertex out of range")

    def require_directed(self, directed: bool) -> None:
        if self.directed != directed:
            raise ValueError(
                "algorithm requires " + ("directed" if directed else "undirected") + " graph"
            )

    def add_edge(self, source: int, target: int, weight: int = 1) -> int:
        self.vertex(source)
        self.vertex(target)
        identifier = self._next_id
        self._next_id += 1
        self.edges[identifier] = Edge(source, target, weight, identifier)
        self.adjacency[source].append((target, weight, identifier))
        if not self.directed:
            self.adjacency[target].append((source, weight, identifier))
        return identifier

    def delete_edge(self, identifier: int) -> bool:
        edge = self.edges.pop(identifier, None)
        if edge is None:
            return False
        for vertex in {edge.source, edge.target}:
            self.adjacency[vertex] = [arc for arc in self.adjacency[vertex] if arc[2] != identifier]
        return True


def read_graph(stream, directed=False, weighted=False):
    """Read the original C input format; convert vertex labels 1..n to 0..n-1."""
    tokens = list(map(int, stream.read().split()))
    if len(tokens) < 2:
        raise ValueError("expected vertex and edge counts")
    size, count = tokens[:2]
    width = 3 if weighted else 2
    if count < 0 or len(tokens) != 2 + width * count:
        raise ValueError("incorrect edge count")
    graph = Graph(size, directed)
    for offset in range(2, len(tokens), width):
        source, target = tokens[offset : offset + 2]
        graph.add_edge(source - 1, target - 1, tokens[offset + 2] if weighted else 1)
    return graph
