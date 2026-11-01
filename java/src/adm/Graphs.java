/* Copyright 2003-2020 by Steven S. Skiena; all rights reserved. 
Permission is granted for use in non-commerical applications
provided this copyright notice remains intact and unchanged.

These programs appear in my books:

"The Algorithm Design Manual" by Steven Skiena, second edition, Springer,
London 2008.  See out website www.algorist.com for additional information
or https://www.amazon.com/exec/obidos/ASIN/1848000693/thealgorith01-20

"Programming Challenges: The Programming Contest Training Manual"
by Steven Skiena and Miguel Revilla, Springer-Verlag, New York 2003.
See our website www.programming-challenges.com for additional information,
or https://www.amazon.com/exec/obidos/ASIN/0387001638/thealgorithmrepo/
*/

package adm;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.PriorityQueue;

/** Graph algorithms with per-call search state. Vertices are 0..n-1. */
public final class Graphs {
    private Graphs() {}
    public record Edge(int from, int to, long weight, int id) {}
    private record Arc(int to, long weight, int id) {}

    /** Mutable multigraph; each undirected edge appears once in edges(). */
    public static final class Graph {
        public final int n;
        public final boolean directed;
        private final List<Edge> edges = new ArrayList<>();
        private int nextId;
        public Graph(int n, boolean directed) {
            if (n < 0) {
                throw new IllegalArgumentException("negative vertex count");
            }
            this.n = n;
            this.directed = directed;
        }
        public void vertex(int v) {
            if (v < 0 || v >= n) {
                throw new IllegalArgumentException("vertex outside graph");
            }
        }
        public void add(int from, int to, long weight) {
            vertex(from);
            vertex(to);
            edges.add(new Edge(from, to, weight, nextId++));
        }
        public boolean delete(int from, int to) {
            vertex(from);
            vertex(to);
            for (int i = 0; i < edges.size(); i++) {
                Edge edge = edges.get(i);
                if ((edge.from == from && edge.to == to) ||
                    (!directed && edge.from == to && edge.to == from)) {
                    edges.remove(i);
                    return true;
                }
            }
            return false;
        }
        public List<Edge> edges() {
            return List.copyOf(edges);
        }
        private List<List<Arc>> adjacency() {
            List<List<Arc>> result = new ArrayList<>();
            for (int i = 0; i < n; i++) {
                result.add(new ArrayList<>());
            }
            for (Edge edge : edges) {
                result.get(edge.from).add(new Arc(edge.to, edge.weight, edge.id));
                if (!directed) {
                    result.get(edge.to).add(new Arc(edge.from, edge.weight, edge.id));
                }
            }
            return result;
        }
    }

    public record BreadthFirst(Long[] distances, int[] parents) {}

    /** O(V+E), with null distances for unreachable vertices. */
    public static BreadthFirst breadthFirst(Graph graph, int source) {
        graph.vertex(source);
        List<List<Arc>> adjacency = graph.adjacency();
        Long[] distances = new Long[graph.n];
        int[] parents = new int[graph.n];
        Arrays.fill(parents, -1);
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        distances[source] = 0L;
        queue.add(source);
        while (!queue.isEmpty()) {
            int from = queue.remove();
            for (Arc arc : adjacency.get(from)) {
                if (distances[arc.to] == null) {
                    distances[arc.to] = distances[from] + 1;
                    parents[arc.to] = from;
                    queue.add(arc.to);
                }
            }
        }
        return new BreadthFirst(distances, parents);
    }

    /** Reconstructs source..target, or [] when unreachable. Validates malformed parent chains. */
    public static List<Integer> path(int[] parents, int source, int target) {
        if (source < 0 || target < 0 || source >= parents.length || target >= parents.length) {
            throw new IllegalArgumentException("invalid path endpoint");
        }
        List<Integer> result = new ArrayList<>();
        boolean[] seen = new boolean[parents.length];
        for (int current = target; current != -1; current = parents[current]) {
            if (current < 0 || current >= parents.length || seen[current]) {
                throw new IllegalArgumentException("invalid parent chain");
            }
            seen[current] = true;
            result.add(current);
            if (current == source) {
                Collections.reverse(result);
                return result;
            }
        }
        return List.of();
    }

    /** Depth-first preorder in adjacency insertion order. O(V+E). */
    public static List<Integer> depthFirst(Graph graph, int source) {
        graph.vertex(source);
        List<Integer> result = new ArrayList<>();
        visit(graph.adjacency(), source, new boolean[graph.n], result);
        return result;
    }
    private static void visit(List<List<Arc>> adjacency, int vertex, boolean[] seen,
                              List<Integer> result) {
        if (seen[vertex]) {
            return;
        }
        seen[vertex] = true;
        result.add(vertex);
        for (Arc arc : adjacency.get(vertex)) {
            visit(adjacency, arc.to, seen, result);
        }
    }
    private static void requireUndirected(Graph graph) {
        if (graph.directed) {
            throw new IllegalArgumentException("undirected graph required");
        }
    }
    private static void requireDirected(Graph graph) {
        if (!graph.directed) {
            throw new IllegalArgumentException("directed graph required");
        }
    }
    public static int compareLists(List<Integer> left, List<Integer> right) {
        int common = Math.min(left.size(), right.size());
        for (int i = 0; i < common; i++) {
            int comparison = Integer.compare(left.get(i), right.get(i));
            if (comparison != 0) {
                return comparison;
            }
        }
        return Integer.compare(left.size(), right.size());
    }
    private static List<List<Integer>> canonical(List<List<Integer>> groups) {
        for (List<Integer> group : groups) {
            Collections.sort(group);
        }
        groups.sort(Graphs::compareLists);
        return groups;
    }
    public static List<List<Integer>> components(Graph graph) {
        requireUndirected(graph);
        List<List<Arc>> adjacency = graph.adjacency();
        boolean[] seen = new boolean[graph.n];
        List<List<Integer>> groups = new ArrayList<>();
        for (int i = 0; i < graph.n; i++) {
            if (!seen[i]) {
                List<Integer> group = new ArrayList<>();
                visit(adjacency, i, seen, group);
                groups.add(group);
            }
        }
        return canonical(groups);
    }

    /** Returns a +/-1 color witness, or null when an odd cycle exists. O(V+E). */
    public static int[] bipartiteColors(Graph graph) {
        requireUndirected(graph);
        List<List<Arc>> adjacency = graph.adjacency();
        int[] colors = new int[graph.n];
        for (int start = 0; start < graph.n; start++) {
            if (colors[start] != 0) {
                continue;
            }
            colors[start] = 1;
            ArrayDeque<Integer> queue = new ArrayDeque<>();
            queue.add(start);
            while (!queue.isEmpty()) {
                int from = queue.remove();
                for (Arc arc : adjacency.get(from)) {
                    if (colors[arc.to] == colors[from]) {
                        return null;
                    }
                    if (colors[arc.to] == 0) {
                        colors[arc.to] = -colors[from];
                        queue.add(arc.to);
                    }
                }
            }
        }
        return colors;
    }
    public static boolean bipartite(Graph graph) {
        return bipartiteColors(graph) != null;
    }

    public static boolean hasCycle(Graph graph) {
        requireUndirected(graph);
        List<List<Arc>> adjacency = graph.adjacency();
        boolean[] seen = new boolean[graph.n];
        for (int i = 0; i < graph.n; i++) {
            if (!seen[i] && cycleVisit(adjacency, i, -1, seen)) {
                return true;
            }
        }
        return false;
    }
    private static boolean cycleVisit(List<List<Arc>> adjacency, int from, int parentEdge,
                                      boolean[] seen) {
        seen[from] = true;
        for (Arc arc : adjacency.get(from)) {
            if (arc.id == parentEdge) {
                continue;
            }
            if (seen[arc.to] || cycleVisit(adjacency, arc.to, arc.id, seen)) {
                return true;
            }
        }
        return false;
    }

    /** Low-link articulation points; edge IDs distinguish parallel edges. O(V+E). */
    public static List<Integer> articulation(Graph graph) {
        requireUndirected(graph);
        List<List<Arc>> adjacency = graph.adjacency();
        int[] discovery = new int[graph.n];
        int[] low = new int[graph.n];
        boolean[] cut = new boolean[graph.n];
        int[] clock = {0};
        for (int i = 0; i < graph.n; i++) {
            if (discovery[i] == 0) {
                articulationVisit(adjacency, i, -1, discovery, low, cut, clock);
            }
        }
        List<Integer> result = new ArrayList<>();
        for (int i = 0; i < graph.n; i++) {
            if (cut[i]) {
                result.add(i);
            }
        }
        return result;
    }
    private static void articulationVisit(List<List<Arc>> adjacency, int from, int parentEdge,
                                          int[] discovery, int[] low, boolean[] cut, int[] clock) {
        discovery[from] = low[from] = ++clock[0];
        int children = 0;
        for (Arc arc : adjacency.get(from)) {
            if (arc.id == parentEdge) {
                continue;
            }
            if (discovery[arc.to] == 0) {
                children++;
                articulationVisit(adjacency, arc.to, arc.id, discovery, low, cut, clock);
                low[from] = Math.min(low[from], low[arc.to]);
                if (parentEdge != -1 && low[arc.to] >= discovery[from]) {
                    cut[from] = true;
                }
            } else {
                low[from] = Math.min(low[from], discovery[arc.to]);
            }
        }
        if (parentEdge == -1 && children > 1) {
            cut[from] = true;
        }
    }

    public static List<List<Integer>> stronglyConnected(Graph graph, String method) {
        requireDirected(graph);
        return switch (method) {
            case "tarjan" -> tarjan(graph);
            case "kosaraju" -> kosaraju(graph);
            default -> throw new IllegalArgumentException("unknown SCC method");
        };
    }
    private static List<List<Integer>> tarjan(Graph graph) {
        List<List<Arc>> adjacency = graph.adjacency();
        int[] index = new int[graph.n];
        int[] low = new int[graph.n];
        boolean[] active = new boolean[graph.n];
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        List<List<Integer>> groups = new ArrayList<>();
        int[] clock = {0};
        for (int v = 0; v < graph.n; v++) {
            if (index[v] == 0) {
                tarjanVisit(adjacency, v, index, low, active, stack, groups, clock);
            }
        }
        return canonical(groups);
    }
    private static void tarjanVisit(List<List<Arc>> adjacency, int v, int[] index, int[] low,
                                    boolean[] active, ArrayDeque<Integer> stack,
                                    List<List<Integer>> groups, int[] clock) {
        index[v] = low[v] = ++clock[0];
        stack.push(v);
        active[v] = true;
        for (Arc arc : adjacency.get(v)) {
            int w = arc.to;
            if (index[w] == 0) {
                tarjanVisit(adjacency, w, index, low, active, stack, groups, clock);
                low[v] = Math.min(low[v], low[w]);
            } else if (active[w]) {
                low[v] = Math.min(low[v], index[w]);
            }
        }
        if (low[v] == index[v]) {
            List<Integer> group = new ArrayList<>();
            int w;
            do {
                w = stack.pop();
                active[w] = false;
                group.add(w);
            } while (w != v);
            groups.add(group);
        }
    }
    private static void finish(List<List<Arc>> adjacency, int v, boolean[] seen,
                               List<Integer> order) {
        seen[v] = true;
        for (Arc arc : adjacency.get(v)) {
            if (!seen[arc.to]) {
                finish(adjacency, arc.to, seen, order);
            }
        }
        order.add(v);
    }
    private static List<List<Integer>> kosaraju(Graph graph) {
        List<List<Arc>> adjacency = graph.adjacency();
        boolean[] seen = new boolean[graph.n];
        List<Integer> order = new ArrayList<>();
        for (int v = 0; v < graph.n; v++) {
            if (!seen[v]) {
                finish(adjacency, v, seen, order);
            }
        }
        Graph reverse = new Graph(graph.n, true);
        for (Edge edge : graph.edges) {
            reverse.add(edge.to, edge.from, edge.weight);
        }
        List<List<Arc>> reversed = reverse.adjacency();
        Arrays.fill(seen, false);
        List<List<Integer>> groups = new ArrayList<>();
        for (int i = order.size() - 1; i >= 0; i--) {
            int v = order.get(i);
            if (!seen[v]) {
                List<Integer> group = new ArrayList<>();
                visit(reversed, v, seen, group);
                groups.add(group);
            }
        }
        return canonical(groups);
    }

    public static List<Integer> topological(Graph graph, String method) {
        requireDirected(graph);
        List<List<Arc>> adjacency = graph.adjacency();
        List<Integer> result = new ArrayList<>();
        if (method.equals("kahn")) {
            int[] incoming = new int[graph.n];
            for (Edge edge : graph.edges) {
                incoming[edge.to]++;
            }
            ArrayDeque<Integer> ready = new ArrayDeque<>();
            for (int i = 0; i < graph.n; i++) {
                if (incoming[i] == 0) {
                    ready.add(i);
                }
            }
            while (!ready.isEmpty()) {
                int from = ready.remove();
                result.add(from);
                for (Arc arc : adjacency.get(from)) {
                    if (--incoming[arc.to] == 0) {
                        ready.add(arc.to);
                    }
                }
            }
            if (result.size() != graph.n) {
                throw new IllegalArgumentException("cycle prevents topological order");
            }
        } else if (method.equals("dfs")) {
            int[] state = new int[graph.n];
            for (int i = 0; i < graph.n; i++) {
                if (state[i] == 0) {
                    topoVisit(adjacency, i, state, result);
                }
            }
            Collections.reverse(result);
        } else {
            throw new IllegalArgumentException("unknown topological method");
        }
        return result;
    }
    private static void topoVisit(List<List<Arc>> adjacency, int v, int[] state,
                                  List<Integer> order) {
        state[v] = 1;
        for (Arc arc : adjacency.get(v)) {
            if (state[arc.to] == 1) {
                throw new IllegalArgumentException("cycle prevents topological order");
            }
            if (state[arc.to] == 0) {
                topoVisit(adjacency, arc.to, state, order);
            }
        }
        state[v] = 2;
        order.add(v);
    }

    public record Forest(long cost, List<long[]> edges) {}
    private record Candidate(int from, int to, long weight, int id) {}
    private static final Comparator<Candidate> BY_WEIGHT =
        Comparator.comparingLong(Candidate::weight)
            .thenComparingInt(Candidate::from)
            .thenComparingInt(Candidate::to)
            .thenComparingInt(Candidate::id);

    /** Minimum spanning FOREST, including disconnected/empty graphs. */
    public static Forest minimumSpanningForest(Graph graph, String method) {
        requireUndirected(graph);
        List<long[]> chosen = new ArrayList<>();
        long total = 0;
        if (method.equals("kruskal")) {
            List<Edge> edges = new ArrayList<>(graph.edges);
            edges.sort(Comparator.comparingLong(Edge::weight).thenComparingInt(Edge::id));
            Containers.DisjointSet sets = new Containers.DisjointSet(graph.n);
            for (Edge edge : edges) {
                if (sets.union(edge.from, edge.to)) {
                    chosen.add(new long[] {edge.from, edge.to, edge.weight});
                    total = Math.addExact(total, edge.weight);
                }
            }
        } else if (method.equals("prim")) {
            List<List<Arc>> adjacency = graph.adjacency();
            boolean[] seen = new boolean[graph.n];
            PriorityQueue<Candidate> candidates = new PriorityQueue<>(BY_WEIGHT);
            for (int root = 0; root < graph.n; root++) {
                if (seen[root]) {
                    continue;
                }
                seen[root] = true;
                for (Arc arc : adjacency.get(root)) {
                    candidates.add(new Candidate(root, arc.to, arc.weight, arc.id));
                }
                while (!candidates.isEmpty()) {
                    Candidate edge = candidates.remove();
                    if (seen[edge.to]) {
                        continue;
                    }
                    seen[edge.to] = true;
                    chosen.add(new long[] {edge.from, edge.to, edge.weight});
                    total = Math.addExact(total, edge.weight);
                    for (Arc arc : adjacency.get(edge.to)) {
                        if (!seen[arc.to]) {
                            candidates.add(new Candidate(edge.to, arc.to, arc.weight, arc.id));
                        }
                    }
                }
            }
        } else {
            throw new IllegalArgumentException("unknown spanning forest method");
        }
        return new Forest(total, chosen);
    }

    private record Distance(int vertex, long value) {}
    /** Nonnegative weights only. O((V+E) log(E+1)), checked long path additions. */
    public static Long[] dijkstra(Graph graph, int source) {
        return dijkstraPaths(graph, source).distances();
    }

    public record ShortestPaths(Long[] distances, int[] parents) {}

    /** Dijkstra distances and parent witness, with -1 for source/unreachable parents. */
    public static ShortestPaths dijkstraPaths(Graph graph, int source) {
        graph.vertex(source);
        for (Edge edge : graph.edges) {
            if (edge.weight < 0) {
                throw new IllegalArgumentException("negative Dijkstra edge");
            }
        }
        List<List<Arc>> adjacency = graph.adjacency();
        Long[] distance = new Long[graph.n];
        int[] parents = new int[graph.n];
        Arrays.fill(parents, -1);
        PriorityQueue<Distance> queue =
            new PriorityQueue<>(Comparator.comparingLong(Distance::value));
        distance[source] = 0L;
        queue.add(new Distance(source, 0));
        while (!queue.isEmpty()) {
            Distance current = queue.remove();
            if (distance[current.vertex] != current.value) {
                continue;
            }
            for (Arc arc : adjacency.get(current.vertex)) {
                long candidate = Math.addExact(current.value, arc.weight);
                if (distance[arc.to] == null || candidate < distance[arc.to]) {
                    distance[arc.to] = candidate;
                    parents[arc.to] = current.vertex;
                    queue.add(new Distance(arc.to, candidate));
                }
            }
        }
        return new ShortestPaths(distance, parents);
    }

    /** O(V^3), signed weights allowed; any negative cycle is an error. */
    public static Long[][] floyd(Graph graph) {
        Long[][] distances = new Long[graph.n][graph.n];
        for (int i = 0; i < graph.n; i++) {
            distances[i][i] = 0L;
        }
        for (Edge edge : graph.edges) {
            Long old = distances[edge.from][edge.to];
            if (old == null || edge.weight < old) {
                distances[edge.from][edge.to] = edge.weight;
            }
            if (!graph.directed) {
                old = distances[edge.to][edge.from];
                if (old == null || edge.weight < old) {
                    distances[edge.to][edge.from] = edge.weight;
                }
            }
        }
        for (int middle = 0; middle < graph.n; middle++) {
            for (int from = 0; from < graph.n; from++) {
                if (distances[from][middle] == null) {
                    continue;
                }
                for (int to = 0; to < graph.n; to++) {
                    if (distances[middle][to] == null) {
                        continue;
                    }
                    long candidate = Math.addExact(distances[from][middle], distances[middle][to]);
                    if (distances[from][to] == null || candidate < distances[from][to]) {
                        distances[from][to] = candidate;
                    }
                }
            }
        }
        for (int i = 0; i < graph.n; i++) {
            if (distances[i][i] < 0) {
                throw new IllegalArgumentException("negative cycle");
            }
        }
        return distances;
    }

    /** Net flow matrix is antisymmetric, including antiparallel input capacities. */
    public record Flow(long value, long[][] net) {}

    /** Matrix Edmonds-Karp, O(V^3 E) worst case and O(V^2) storage; nonnegative capacities. */
    public static Flow maximumFlow(Graph graph, int source, int sink) {
        requireDirected(graph);
        graph.vertex(source);
        graph.vertex(sink);
        if (source == sink) {
            throw new IllegalArgumentException("source equals sink");
        }
        long[][] residual = new long[graph.n][graph.n];
        long[][] net = new long[graph.n][graph.n];
        for (Edge edge : graph.edges) {
            if (edge.weight < 0) {
                throw new IllegalArgumentException("negative capacity");
            }
            if (edge.from != edge.to) {
                residual[edge.from][edge.to] =
                    Math.addExact(residual[edge.from][edge.to], edge.weight);
            }
        }
        long total = 0;
        while (true) {
            int[] parent = new int[graph.n];
            Arrays.fill(parent, -1);
            parent[source] = source;
            ArrayDeque<Integer> queue = new ArrayDeque<>();
            queue.add(source);
            while (!queue.isEmpty() && parent[sink] == -1) {
                int from = queue.remove();
                for (int to = 0; to < graph.n; to++) {
                    if (parent[to] == -1 && residual[from][to] > 0) {
                        parent[to] = from;
                        queue.add(to);
                    }
                }
            }
            if (parent[sink] == -1) {
                break;
            }
            long amount = Long.MAX_VALUE;
            for (int to = sink; to != source; to = parent[to]) {
                amount = Math.min(amount, residual[parent[to]][to]);
            }
            for (int to = sink; to != source; to = parent[to]) {
                int from = parent[to];
                residual[from][to] -= amount;
                residual[to][from] = Math.addExact(residual[to][from], amount);
                net[from][to] = Math.addExact(net[from][to], amount);
                net[to][from] = Math.subtractExact(net[to][from], amount);
            }
            total = Math.addExact(total, amount);
        }
        return new Flow(total, net);
    }

    /** Enumerates distinct simple VERTEX paths; parallel edges do not duplicate paths. */
    public static List<List<Integer>> simplePaths(Graph graph, int source, int target) {
        graph.vertex(source);
        graph.vertex(target);
        List<List<Integer>> result = new ArrayList<>();
        List<Integer> path = new ArrayList<>();
        path.add(source);
        pathsVisit(graph.adjacency(), source, target, new boolean[graph.n], path, result);
        result.sort(Graphs::compareLists);
        return result;
    }
    private static void pathsVisit(List<List<Arc>> adjacency, int current, int target,
                                   boolean[] used, List<Integer> path, List<List<Integer>> result) {
        if (current == target) {
            result.add(new ArrayList<>(path));
            return;
        }
        used[current] = true;
        boolean[] tried = new boolean[adjacency.size()];
        for (Arc arc : adjacency.get(current)) {
            if (!used[arc.to] && !tried[arc.to]) {
                tried[arc.to] = true;
                path.add(arc.to);
                pathsVisit(adjacency, arc.to, target, used, path, result);
                path.remove(path.size() - 1);
            }
        }
        used[current] = false;
    }
}
