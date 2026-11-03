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
import java.util.Collections;
import java.util.List;

public final class Topsort1 {
    static void topoVisit(List<List<Graph.Arc>> adjacency, int v, int[] state,
                          List<Integer> order) {
        state[v] = 1;
        for (Graph.Arc arc : adjacency.get(v)) {
            if (state[arc.to()] == 1) {
                throw new IllegalArgumentException("cycle prevents topological order");
            }
            if (state[arc.to()] == 0) {
                topoVisit(adjacency, arc.to(), state, order);
            }
        }
        state[v] = 2;
        order.add(v);
    }

    public static List<Integer> topological(Graph graph) {
        Graph.requireDirected(graph);
        List<List<Graph.Arc>> adjacency = graph.adjacency();
        List<Integer> result = new ArrayList<>();

        int[] state = new int[graph.n];
        for (int i = 0; i < graph.n; i++) {
            if (state[i] == 0) {
                topoVisit(adjacency, i, state, result);
            }
        }
        Collections.reverse(result);
        return result;
    }

    public static void main(String[] args) {
        Graph graph = Graph.read(new java.util.Scanner(System.in), true, false);
        System.out.println(topological(graph));
    }
}
