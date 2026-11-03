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
import java.util.Arrays;

public final class Netflow {
    /** Net flow matrix is antisymmetric, including antiparallel input capacities. */
    public record Flow(long value, long[][] net) {}

    /** Matrix Edmonds-Karp, O(V^3 E) worst case and O(V^2) storage; nonnegative capacities. */
    public static Flow maximumFlow(Graph graph, int source, int sink) {
        Graph.requireDirected(graph);
        graph.vertex(source);
        graph.vertex(sink);
        if (source == sink) {
            throw new IllegalArgumentException("source equals sink");
        }
        long[][] residual = new long[graph.n][graph.n];
        long[][] net = new long[graph.n][graph.n];
        for (Graph.Edge edge : graph.edges) {
            if (edge.weight() < 0) {
                throw new IllegalArgumentException("negative capacity");
            }
            if (edge.from() != edge.to()) {
                residual[edge.from()][edge.to()] =
                    Math.addExact(residual[edge.from()][edge.to()], edge.weight());
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

    public static void main(String[] args) {
        java.util.Scanner in = new java.util.Scanner(System.in);
        int source = in.nextInt() - 1, sink = in.nextInt() - 1;
        System.out.println(maximumFlow(Wgraph.read(in, true), source, sink).value());
    }
}
