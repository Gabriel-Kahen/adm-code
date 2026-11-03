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

import java.util.List;

public final class Findcycle {
    public static boolean hasCycle(Graph graph) {
        Graph.requireUndirected(graph);
        List<List<Graph.Arc>> adjacency = graph.adjacency();
        boolean[] seen = new boolean[graph.n];
        for (int i = 0; i < graph.n; i++) {
            if (!seen[i] && cycleVisit(adjacency, i, -1, seen)) {
                return true;
            }
        }
        return false;
    }

    static boolean cycleVisit(List<List<Graph.Arc>> adjacency, int from, int parentEdge,
                              boolean[] seen) {
        seen[from] = true;
        for (Graph.Arc arc : adjacency.get(from)) {
            if (arc.id() == parentEdge) {
                continue;
            }
            if (seen[arc.to()] || cycleVisit(adjacency, arc.to(), arc.id(), seen)) {
                return true;
            }
        }
        return false;
    }

    public static void main(String[] args) {
        Graph graph = Graph.read(new java.util.Scanner(System.in), false, false);
        System.out.println(hasCycle(graph));
    }
}
