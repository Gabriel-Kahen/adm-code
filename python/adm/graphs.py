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

"""Adjacency-list graph algorithms; vertices are 0..n-1 and searches own their state."""

import heapq
from collections import deque
from dataclasses import dataclass

from .containers import DisjointSet


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


def connected_components(graph: Graph) -> list[list[int]]:
    graph.require_directed(False)
    visited = set()
    components = []
    for vertex in range(graph.n):
        if vertex not in visited:
            component = depth_first_search(graph, vertex)
            visited.update(component)
            components.append(sorted(component))
    return sorted(components)


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


def has_undirected_cycle(graph: Graph) -> bool:
    """O(E α(V)); loops and a second parallel edge are cycles."""
    graph.require_directed(False)
    sets = DisjointSet(graph.n)
    return any(not sets.union(edge.source, edge.target) for edge in graph.edges.values())


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


def strongly_connected_components(graph: Graph, method: str = "tarjan") -> list[list[int]]:
    """Tarjan low-link or Kosaraju transpose DFS, both O(V+E)."""
    graph.require_directed(True)
    result = []
    if method == "tarjan":
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
    elif method == "kosaraju":
        visited = set()
        order = []
        for start in range(graph.n):
            if start in visited:
                continue
            pending = [(start, False)]
            while pending:
                vertex, finished = pending.pop()
                if finished:
                    order.append(vertex)
                elif vertex not in visited:
                    visited.add(vertex)
                    pending.append((vertex, True))
                    pending.extend((arc[0], False) for arc in reversed(graph.adjacency[vertex]))
        transpose = Graph(graph.n, True)
        for edge in graph.edges.values():
            transpose.add_edge(edge.target, edge.source)
        visited.clear()
        for vertex in reversed(order):
            if vertex in visited:
                continue
            component = []
            pending = [vertex]
            visited.add(vertex)
            while pending:
                member = pending.pop()
                component.append(member)
                for neighbor, _, _ in transpose.adjacency[member]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        pending.append(neighbor)
            result.append(sorted(component))
    else:
        raise ValueError("unknown SCC method")
    return sorted(result)


def topological_sort(graph: Graph, method: str = "kahn") -> list[int]:
    """O(V+E) topological order; raise ValueError if any directed cycle exists."""
    graph.require_directed(True)
    result = []
    if method == "kahn":
        degree = [0] * graph.n
        for edge in graph.edges.values():
            degree[edge.target] += 1
        pending = deque(vertex for vertex in range(graph.n) if degree[vertex] == 0)
        while pending:
            vertex = pending.popleft()
            result.append(vertex)
            for neighbor, _, _ in graph.adjacency[vertex]:
                degree[neighbor] -= 1
                if degree[neighbor] == 0:
                    pending.append(neighbor)
        if len(result) != graph.n:
            raise ValueError("directed cycle")
    elif method == "dfs":
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
    else:
        raise ValueError("unknown topological method")
    return result


def minimum_spanning_forest(graph: Graph, method: str = "kruskal") -> dict:
    """Prim O((V+E) log E) or Kruskal O(E log E); includes disconnected components."""
    graph.require_directed(False)
    selected = []
    if method == "kruskal":
        sets = DisjointSet(graph.n)
        for edge in sorted(graph.edges.values(), key=lambda item: (item.weight, item.identifier)):
            if sets.union(edge.source, edge.target):
                selected.append([edge.source, edge.target, edge.weight])
    elif method == "prim":
        visited = set()
        for start in range(graph.n):
            if start in visited:
                continue
            pending = [(0, -1, start, start)]
            while pending:
                weight, _, source, target = heapq.heappop(pending)
                if target in visited:
                    continue
                visited.add(target)
                if source != target:
                    selected.append([source, target, weight])
                for neighbor, edge_weight, identifier in graph.adjacency[target]:
                    if neighbor not in visited:
                        heapq.heappush(pending, (edge_weight, identifier, target, neighbor))
    else:
        raise ValueError("unknown spanning forest method")
    return {"cost": sum(edge[2] for edge in selected), "edges": selected}


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
