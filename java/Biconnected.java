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
import java.util.List;

public final class Biconnected {
    /** Low-link articulation points; edge IDs distinguish parallel edges. O(V+E). */
    public static List<Integer> articulation(Graph graph) {
        Graph.requireUndirected(graph);
        List<List<Graph.Arc>> adjacency = graph.adjacency();
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

    static void articulationVisit(List<List<Graph.Arc>> adjacency, int from, int parentEdge,
                                  int[] discovery, int[] low, boolean[] cut, int[] clock) {
        discovery[from] = low[from] = ++clock[0];
        int children = 0;
        for (Graph.Arc arc : adjacency.get(from)) {
            if (arc.id() == parentEdge) {
                continue;
            }
            if (discovery[arc.to()] == 0) {
                children++;
                articulationVisit(adjacency, arc.to(), arc.id(), discovery, low, cut, clock);
                low[from] = Math.min(low[from], low[arc.to()]);
                if (parentEdge != -1 && low[arc.to()] >= discovery[from]) {
                    cut[from] = true;
                }
            } else {
                low[from] = Math.min(low[from], discovery[arc.to()]);
            }
        }
        if (parentEdge == -1 && children > 1) {
            cut[from] = true;
        }
    }

    public static void main(String[] args) {
        Graph graph = Graph.read(new java.util.Scanner(System.in), false, false);
        System.out.println(articulation(graph));
    }
}
