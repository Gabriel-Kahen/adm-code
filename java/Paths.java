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

public final class Paths {
    /** Enumerates distinct simple VERTEX paths; parallel edges do not duplicate paths. */
    public static List<List<Integer>> simplePaths(Graph graph, int source, int target) {
        graph.vertex(source);
        graph.vertex(target);
        List<List<Integer>> result = new ArrayList<>();
        List<Integer> path = new ArrayList<>();
        path.add(source);
        pathsVisit(graph.adjacency(), source, target, new boolean[graph.n], path, result);
        result.sort(Graph::compareLists);
        return result;
    }

    static void pathsVisit(List<List<Graph.Arc>> adjacency, int current, int target, boolean[] used,
                           List<Integer> path, List<List<Integer>> result) {
        if (current == target) {
            result.add(new ArrayList<>(path));
            return;
        }
        used[current] = true;
        boolean[] tried = new boolean[adjacency.size()];
        for (Graph.Arc arc : adjacency.get(current)) {
            if (!used[arc.to()] && !tried[arc.to()]) {
                tried[arc.to()] = true;
                path.add(arc.to());
                pathsVisit(adjacency, arc.to(), target, used, path, result);
                path.remove(path.size() - 1);
            }
        }
        used[current] = false;
    }

    public static void main(String[] args) {
        Graph graph = Graph.read(new java.util.Scanner(System.in), false, false);
        System.out.println(simplePaths(graph, 0, graph.n - 1));
    }
}
