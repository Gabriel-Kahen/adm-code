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

import java.util.Arrays;

public final class Floyd {
    /** O(V^3), signed weights allowed; any negative cycle is an error. */
    public static Long[][] floyd(Graph graph) {
        Long[][] distances = new Long[graph.n][graph.n];
        for (int i = 0; i < graph.n; i++) {
            distances[i][i] = 0L;
        }
        for (Graph.Edge edge : graph.edges) {
            Long old = distances[edge.from()][edge.to()];
            if (old == null || edge.weight() < old) {
                distances[edge.from()][edge.to()] = edge.weight();
            }
            if (!graph.directed) {
                old = distances[edge.to()][edge.from()];
                if (old == null || edge.weight() < old) {
                    distances[edge.to()][edge.from()] = edge.weight();
                }
            }
        }
        for (int middle = 0; middle < graph.n; middle++) {
            for (int from = 0; from < graph.n; from++) {
                if (distances[from][middle] == null) {
                    continue;
                }
                for (int to = 0; to < graph.n; to++) {
                    if (distances[middle][to] == null) {
                        continue;
                    }
                    long candidate = Math.addExact(distances[from][middle], distances[middle][to]);
                    if (distances[from][to] == null || candidate < distances[from][to]) {
                        distances[from][to] = candidate;
                    }
                }
            }
        }
        for (int i = 0; i < graph.n; i++) {
            if (distances[i][i] < 0) {
                throw new IllegalArgumentException("negative cycle");
            }
        }
        return distances;
    }

    public static void main(String[] args) {
        Graph graph = Graph.read(new java.util.Scanner(System.in), false, true);
        System.out.println(Arrays.deepToString(floyd(graph)));
    }
}
