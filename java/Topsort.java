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

public final class Topsort {
    public static List<Integer> topological(Graph graph) {
        Graph.requireDirected(graph);
        List<List<Graph.Arc>> adjacency = graph.adjacency();
        List<Integer> result = new ArrayList<>();

        int[] incoming = new int[graph.n];
        for (Graph.Edge edge : graph.edges) {
            incoming[edge.to()]++;
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
            for (Graph.Arc arc : adjacency.get(from)) {
                if (--incoming[arc.to()] == 0) {
                    ready.add(arc.to());
                }
            }
        }
        if (result.size() != graph.n) {
            throw new IllegalArgumentException("cycle prevents topological order");
        }
        return result;
    }

    public static void main(String[] args) {
        Graph graph = Graph.read(new java.util.Scanner(System.in), true, false);
        System.out.println(topological(graph));
    }
}
