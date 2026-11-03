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
import java.util.Comparator;
import java.util.List;

public final class Kruskal {
    /** Minimum spanning FOREST, including disconnected/empty graphs. */
    public static Wgraph.Forest minimumSpanningForest(Graph graph) {
        Graph.requireUndirected(graph);
        List<long[]> chosen = new ArrayList<>();
        long total = 0;

        List<Graph.Edge> edges = new ArrayList<>(graph.edges);
        edges.sort(Comparator.comparingLong(Graph.Edge::weight).thenComparingInt(Graph.Edge::id));
        SetUnion sets = new SetUnion(graph.n);
        for (Graph.Edge edge : edges) {
            if (sets.union(edge.from(), edge.to())) {
                chosen.add(new long[] {edge.from(), edge.to(), edge.weight()});
                total = Math.addExact(total, edge.weight());
            }
        }
        return new Wgraph.Forest(total, chosen);
    }

    public static void main(String[] args) {
        Graph graph = Graph.read(new java.util.Scanner(System.in), false, true);
        System.out.println(minimumSpanningForest(graph));
    }
}
