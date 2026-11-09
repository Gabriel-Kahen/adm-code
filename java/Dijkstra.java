/*	dijkstra.c

	Compute shortest paths in weighted graphs using Dijkstra's algorithm
*/

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
or http://www.amazon.com/exec/obidos/ASIN/0387001638/thealgorithmrepo/
*/

import java.util.Locale;

public class Dijkstra {
    public static final int TREE = 0;
    public static final int BACK = 1;
    public static final int CROSS = 2;
    public static final int FORWARD = 3;
    public static final int MAXV = 100;
    public static final long MAXINT = (Long.MAX_VALUE / 4);

    /* Dijkstra requires nonnegative edge weights. Unreachable vertices keep parent -1. */
    public static long dijkstra(Graph.graph g, int start) {
        int i = 0;
        Graph.edgenode edge = null;
        boolean[] settled = new boolean[(MAXV + 1)];
        long[] distance = new long[(MAXV + 1)]; /* shortest known distance from start */
        int vertex = 0;
        int neighbor = 0;
        long next_distance = 0;
        long tree_weight = 0;
        for (i = 1; (i <= g.nvertices); i++) {
            settled[i] = false;
            distance[i] = MAXINT;
            Wgraph.parent[i] = (-1);
        }
        distance[start] = 0;
        vertex = start;
        while (!(settled[vertex])) {
            settled[vertex] = true;
            if ((vertex != start)) {
                System.out.printf(Locale.US, "edge (%d,%d) in tree \n", Wgraph.parent[vertex], vertex);
                /* The distance difference is this parent edge's weight, not a full path length. */
                tree_weight += (distance[vertex] - distance[Wgraph.parent[vertex]]);
            }
            edge = g.edges[vertex];
            while ((edge != null)) {
                neighbor = edge.y;
                if ((distance[neighbor] > (distance[vertex] + edge.weight))) {
                    distance[neighbor] = (distance[vertex] + edge.weight);
                    Wgraph.parent[neighbor] = vertex;
                }
                edge = edge.next;
            }
            /* If none is reachable, vertex stays settled and the outer loop stops. */
            next_distance = MAXINT;
            for (i = 1; (i <= g.nvertices); i++) {
                if ((!(settled[i]) && (next_distance > distance[i]))) {
                    next_distance = distance[i];
                    vertex = i;
                }
            }
        }
        return tree_weight;
    }

    public static int main() {
        Graph.graph g = new Graph.graph();
        int i = 0;
        long weight = 0;
        Wgraph.read_graph(g, false);
        weight = dijkstra(g, 1);
        System.out.printf(Locale.US, "Total SPST edgeweight = %d \n", weight);
        for (i = 1; (i <= g.nvertices); i++) {
            Wgraph.find_path(1, i, Wgraph.parent);
        }
        System.out.print("\n");
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
