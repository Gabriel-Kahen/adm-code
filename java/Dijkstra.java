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
import java.util.Comparator;
import java.util.List;
import java.util.PriorityQueue;

public final class Dijkstra {
    record Distance(int vertex, long value) {}

    /** Nonnegative weights only. O((V+E) log(E+1)), checked long path additions. */
    public static Long[] dijkstra(Graph graph, int source) {
        return dijkstraPaths(graph, source).distances();
    }

    public record ShortestPaths(Long[] distances, int[] parents) {}

    /** Dijkstra distances and parent witness, with -1 for source/unreachable parents. */
    public static ShortestPaths dijkstraPaths(Graph graph, int source) {
        graph.vertex(source);
        for (Graph.Edge edge : graph.edges) {
            if (edge.weight() < 0) {
                throw new IllegalArgumentException("negative Dijkstra edge");
            }
        }
        List<List<Graph.Arc>> adjacency = graph.adjacency();
        Long[] distance = new Long[graph.n];
        int[] parents = new int[graph.n];
        Arrays.fill(parents, -1);
        PriorityQueue<Distance> queue =
            new PriorityQueue<>(Comparator.comparingLong(Distance::value));
        distance[source] = 0L;
        queue.add(new Distance(source, 0));
        while (!queue.isEmpty()) {
            Distance current = queue.remove();
            if (distance[current.vertex] != current.value) {
                continue;
            }
            for (Graph.Arc arc : adjacency.get(current.vertex)) {
                long candidate = Math.addExact(current.value, arc.weight());
                if (distance[arc.to()] == null || candidate < distance[arc.to()]) {
                    distance[arc.to()] = candidate;
                    parents[arc.to()] = current.vertex;
                    queue.add(new Distance(arc.to(), candidate));
                }
            }
        }
        return new ShortestPaths(distance, parents);
    }

    public static void main(String[] args) {
        Graph graph = Graph.read(new java.util.Scanner(System.in), false, true);
        System.out.println(Arrays.toString(dijkstra(graph, 0)));
    }
}
