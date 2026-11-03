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

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;

public final class Strong {
    public static List<List<Integer>> stronglyConnected(Graph graph, String method) {
        Graph.requireDirected(graph);
        return switch (method) {
            case "tarjan" -> tarjan(graph);
            case "kosaraju" -> Strong1.kosaraju(graph);
            default -> throw new IllegalArgumentException("unknown SCC method");
        };
    }

    static List<List<Integer>> tarjan(Graph graph) {
        List<List<Graph.Arc>> adjacency = graph.adjacency();
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
        return Graph.canonical(groups);
    }

    static void tarjanVisit(List<List<Graph.Arc>> adjacency, int v, int[] index, int[] low,
                            boolean[] active, ArrayDeque<Integer> stack, List<List<Integer>> groups,
                            int[] clock) {
        index[v] = low[v] = ++clock[0];
        stack.push(v);
        active[v] = true;
        for (Graph.Arc arc : adjacency.get(v)) {
            int w = arc.to();
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

    public static void main(String[] args) {
        Graph graph = Graph.read(new java.util.Scanner(System.in), true, false);
        System.out.println(tarjan(graph));
    }
}
