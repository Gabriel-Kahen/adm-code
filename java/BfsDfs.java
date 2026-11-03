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
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

public final class BfsDfs {
    public record BreadthFirst(Long[] distances, int[] parents) {}

    /** O(V+E), with null distances for unreachable vertices. */
    public static BreadthFirst breadthFirst(Graph graph, int source) {
        graph.vertex(source);
        List<List<Graph.Arc>> adjacency = graph.adjacency();
        Long[] distances = new Long[graph.n];
        int[] parents = new int[graph.n];
        Arrays.fill(parents, -1);
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        distances[source] = 0L;
        queue.add(source);
        while (!queue.isEmpty()) {
            int from = queue.remove();
            for (Graph.Arc arc : adjacency.get(from)) {
                if (distances[arc.to()] == null) {
                    distances[arc.to()] = distances[from] + 1;
                    parents[arc.to()] = from;
                    queue.add(arc.to());
                }
            }
        }
        return new BreadthFirst(distances, parents);
    }

    /** Reconstructs source..target, or [] when unreachable. Validates malformed parent chains. */
    public static List<Integer> path(int[] parents, int source, int target) {
        if (source < 0 || target < 0 || source >= parents.length || target >= parents.length) {
            throw new IllegalArgumentException("invalid path endpoint");
        }
        List<Integer> result = new ArrayList<>();
        boolean[] seen = new boolean[parents.length];
        for (int current = target; current != -1; current = parents[current]) {
            if (current < 0 || current >= parents.length || seen[current]) {
                throw new IllegalArgumentException("invalid parent chain");
            }
            seen[current] = true;
            result.add(current);
            if (current == source) {
                Collections.reverse(result);
                return result;
            }
        }
        return List.of();
    }

    /** Depth-first preorder in adjacency insertion order. O(V+E). */
    public static List<Integer> depthFirst(Graph graph, int source) {
        graph.vertex(source);
        List<Integer> result = new ArrayList<>();
        visit(graph.adjacency(), source, new boolean[graph.n], result);
        return result;
    }

    static void visit(List<List<Graph.Arc>> adjacency, int vertex, boolean[] seen,
                      List<Integer> result) {
        if (seen[vertex]) {
            return;
        }
        seen[vertex] = true;
        result.add(vertex);
        for (Graph.Arc arc : adjacency.get(vertex)) {
            visit(adjacency, arc.to(), seen, result);
        }
    }
}
