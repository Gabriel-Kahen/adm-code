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

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Graph {
    public record Edge(int from, int to, long weight, int id) {}

    record Arc(int to, long weight, int id) {}

    public final int n;
    public final boolean directed;
    final List<Edge> edges = new ArrayList<>();
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
            if ((edge.from() == from && edge.to() == to) ||
                (!directed && edge.from() == to && edge.to() == from)) {
                edges.remove(i);
                return true;
            }
        }
        return false;
    }
    public List<Edge> edges() {
        return List.copyOf(edges);
    }
    List<List<Arc>> adjacency() {
        List<List<Arc>> result = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            result.add(new ArrayList<>());
        }
        for (Edge edge : edges) {
            result.get(edge.from()).add(new Arc(edge.to(), edge.weight(), edge.id()));
            if (!directed) {
                result.get(edge.to()).add(new Arc(edge.from(), edge.weight(), edge.id()));
            }
        }
        return result;
    }

    static void requireUndirected(Graph graph) {
        if (graph.directed) {
            throw new IllegalArgumentException("undirected graph required");
        }
    }

    static void requireDirected(Graph graph) {
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

    static List<List<Integer>> canonical(List<List<Integer>> groups) {
        for (List<Integer> group : groups) {
            Collections.sort(group);
        }
        groups.sort(Graph::compareLists);
        return groups;
    }
    public static Graph read(java.util.Scanner input, boolean directed, boolean weighted) {
        int n = input.nextInt();
        int count = input.nextInt();
        if (count < 0) {
            throw new IllegalArgumentException("negative edge count");
        }
        Graph graph = new Graph(n, directed);
        for (int i = 0; i < count; i++) {
            int from = input.nextInt() - 1;
            int to = input.nextInt() - 1;
            graph.add(from, to, weighted ? input.nextLong() : 1);
        }
        return graph;
    }
}
