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
import java.util.PriorityQueue;

public final class Prim {
    record Candidate(int from, int to, long weight, int id) {}

    static final Comparator<Candidate> BY_WEIGHT = Comparator.comparingLong(Candidate::weight)
                                                       .thenComparingInt(Candidate::from)
                                                       .thenComparingInt(Candidate::to)
                                                       .thenComparingInt(Candidate::id);

    /** Minimum spanning FOREST, including disconnected/empty graphs. */
    public static Wgraph.Forest minimumSpanningForest(Graph graph) {
        Graph.requireUndirected(graph);
        List<long[]> chosen = new ArrayList<>();
        long total = 0;

        List<List<Graph.Arc>> adjacency = graph.adjacency();
        boolean[] seen = new boolean[graph.n];
        PriorityQueue<Candidate> candidates = new PriorityQueue<>(BY_WEIGHT);
        for (int root = 0; root < graph.n; root++) {
            if (seen[root]) {
                continue;
            }
            seen[root] = true;
            for (Graph.Arc arc : adjacency.get(root)) {
                candidates.add(new Candidate(root, arc.to(), arc.weight(), arc.id()));
            }
            while (!candidates.isEmpty()) {
                Candidate edge = candidates.remove();
                if (seen[edge.to()]) {
                    continue;
                }
                seen[edge.to()] = true;
                chosen.add(new long[] {edge.from(), edge.to(), edge.weight()});
                total = Math.addExact(total, edge.weight());
                for (Graph.Arc arc : adjacency.get(edge.to())) {
                    if (!seen[arc.to()]) {
                        candidates.add(new Candidate(edge.to(), arc.to(), arc.weight(), arc.id()));
                    }
                }
            }
        }
        return new Wgraph.Forest(total, chosen);
    }

    public static void main(String[] args) {
        Graph graph = Graph.read(new java.util.Scanner(System.in), false, true);
        System.out.println(minimumSpanningForest(graph));
    }
}
