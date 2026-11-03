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
import java.util.List;

public final class Bipartite {
    /** Returns a +/-1 color witness, or null when an odd cycle exists. O(V+E). */
    public static int[] bipartiteColors(Graph graph) {
        Graph.requireUndirected(graph);
        List<List<Graph.Arc>> adjacency = graph.adjacency();
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
                for (Graph.Arc arc : adjacency.get(from)) {
                    if (colors[arc.to()] == colors[from]) {
                        return null;
                    }
                    if (colors[arc.to()] == 0) {
                        colors[arc.to()] = -colors[from];
                        queue.add(arc.to());
                    }
                }
            }
        }
        return colors;
    }

    public static boolean bipartite(Graph graph) {
        return bipartiteColors(graph) != null;
    }

    public static void main(String[] args) {
        Graph graph = Graph.read(new java.util.Scanner(System.in), false, false);
        System.out.println(bipartite(graph));
    }
}
