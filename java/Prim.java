/*    prim.c

    Compute minimum spanning trees of graphs via Dijkstra/Prim's algorithm.
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
or https://www.amazon.com/exec/obidos/ASIN/0387001638/thealgorithmrepo/
*/

public class Prim {
    public static final int TREE = 0;
    public static final int BACK = 1;
    public static final int CROSS = 2;
    public static final int FORWARD = 3;
    public static final int MAXV = 100;
    public static final long MAXINT = (Long.MAX_VALUE / 4);

    public static long prim(Graph.graph g, int start) {
        int i = 0;
        Graph.edgenode edge = null;
        boolean[] in_tree = new boolean[(MAXV + 1)];
        long[] distance = new long[(MAXV + 1)]; /* cheapest known edge from the tree */
        int vertex = 0;
        int neighbor = 0;
        long next_distance = 0;
        long tree_weight = 0;
        for (i = 1; (i <= g.nvertices); i++) {
            in_tree[i] = false;
            distance[i] = MAXINT;
            Wgraph.parent[i] = (-1);
        }
        distance[start] = 0;
        vertex = start;
        /* Grow the tree in start's connected component; other parents remain -1. */
        while (!(in_tree[vertex])) {
            in_tree[vertex] = true;
            if ((vertex != start)) {
                C.printf("edge (%d,%d) in tree \n", Wgraph.parent[vertex], vertex);
                tree_weight = (tree_weight + next_distance);
            }
            edge = g.edges[vertex];
            while ((edge != null)) {
                neighbor = edge.y;
                if (((distance[neighbor] > edge.weight) && !(in_tree[neighbor]))) {
                    distance[neighbor] = edge.weight;
                    Wgraph.parent[neighbor] = vertex;
                }
                edge = edge.next;
            }
            next_distance = MAXINT;
            for (i = 1; (i <= g.nvertices); i++) {
                if ((!(in_tree[i]) && (next_distance > distance[i]))) {
                    next_distance = distance[i];
                    vertex = i;
                }
            }
        }
        return tree_weight;
    }

    public static int main() {
        Graph.graph g = new Graph.graph();
        long weight = 0;
        Wgraph.read_graph(g, false);
        weight = prim(g, 1);
        C.printf("Out of Prim: weight = %lld \n", weight);
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
