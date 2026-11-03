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

"""bfs-dfs.c translated to Python; indices start at zero."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path

    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"

from collections import deque

from .graph import Graph


def breadth_first_search(graph: Graph, source: int) -> tuple[list[int | None], list[int | None]]:
    """O(V+E) distances and predecessor forest from source; unreachable entries are None."""
    graph.vertex(source)
    distances: list[int | None] = [None] * graph.n
    parents: list[int | None] = [None] * graph.n
    distances[source] = 0
    pending = deque([source])
    while pending:
        vertex = pending.popleft()
        for neighbor, _, _ in graph.adjacency[vertex]:
            if distances[neighbor] is None:
                distances[neighbor] = distances[vertex] + 1
                parents[neighbor] = vertex
                pending.append(neighbor)
    return distances, parents


def reconstruct_path(parents: list[int | None], source: int, target: int) -> list[int] | None:
    """Follow predecessor links; reject malformed cyclic chains."""
    if not 0 <= source < len(parents) or not 0 <= target < len(parents):
        raise ValueError("path endpoint out of range")
    reverse = []
    visited = set()
    current: int | None = target
    while current is not None:
        if not 0 <= current < len(parents) or current in visited:
            raise ValueError("invalid predecessor chain")
        visited.add(current)
        reverse.append(current)
        if current == source:
            return reverse[::-1]
        current = parents[current]
    return None


def depth_first_search(graph: Graph, source: int) -> list[int]:
    """Iterative O(V+E) preorder, following adjacency insertion order."""
    graph.vertex(source)
    result = []
    visited = set()
    pending = [source]
    while pending:
        vertex = pending.pop()
        if vertex in visited:
            continue
        visited.add(vertex)
        result.append(vertex)
        pending.extend(arc[0] for arc in reversed(graph.adjacency[vertex]) if arc[0] not in visited)
    return result
