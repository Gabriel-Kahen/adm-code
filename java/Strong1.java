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
import java.util.Arrays;
import java.util.List;

public final class Strong1 {
    static void finish(List<List<Graph.Arc>> adjacency, int v, boolean[] seen,
                       List<Integer> order) {
        seen[v] = true;
        for (Graph.Arc arc : adjacency.get(v)) {
            if (!seen[arc.to()]) {
                finish(adjacency, arc.to(), seen, order);
            }
        }
        order.add(v);
    }

    static List<List<Integer>> kosaraju(Graph graph) {
        List<List<Graph.Arc>> adjacency = graph.adjacency();
        boolean[] seen = new boolean[graph.n];
        List<Integer> order = new ArrayList<>();
        for (int v = 0; v < graph.n; v++) {
            if (!seen[v]) {
                finish(adjacency, v, seen, order);
            }
        }
        Graph reverse = new Graph(graph.n, true);
        for (Graph.Edge edge : graph.edges) {
            reverse.add(edge.to(), edge.from(), edge.weight());
        }
        List<List<Graph.Arc>> reversed = reverse.adjacency();
        Arrays.fill(seen, false);
        List<List<Integer>> groups = new ArrayList<>();
        for (int i = order.size() - 1; i >= 0; i--) {
            int v = order.get(i);
            if (!seen[v]) {
                List<Integer> group = new ArrayList<>();
                BfsDfs.visit(reversed, v, seen, group);
                groups.add(group);
            }
        }
        return Graph.canonical(groups);
    }

    public static void main(String[] args) {
        Graph graph = Graph.read(new java.util.Scanner(System.in), true, false);
        System.out.println(kosaraju(graph));
    }
}
