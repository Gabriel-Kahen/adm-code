/*	connected.c
	Compute the connected components of a graph.
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

public class Connected {
    public static final int TREE = 0;
    public static final int BACK = 1;
    public static final int CROSS = 2;
    public static final int FORWARD = 3;
    public static final int MAXV = 100;

    /* discovery relation */
    public static void process_vertex(int v) {
        System.out.printf(Locale.US, " %d", v);
    }

    public static void process_vertex_early(int v) {
        System.out.printf(Locale.US, " %d", v);
    }

    public static void process_vertex_late(int v) {
    }

    public static void process_edge(int x, int y) {
    }

    public static void connected_components(Graph.graph g) {
        int c = 0; /* component number */
        int i = 0; /* counter */
        BfsDfs.initialize_search(g);
        c = 0;
        for (i = 1; (i <= g.nvertices); i++) {
            if (!BfsDfs.discovered[i]) {
                c = (c + 1);
                System.out.printf(Locale.US, "Component %d:", c);
                BfsDfs.bfs(g, i);
                System.out.print("\n");
            }
        }
    }

    public static int main() {
        BfsDfs.callbacks = new BfsDfs.Callbacks() {
            public void process_vertex_early(int v) { Connected.process_vertex_early(v); }
            public void process_vertex_late(int v) { Connected.process_vertex_late(v); }
            public void process_edge(int x, int y) { Connected.process_edge(x, y); }
        };
        Graph.graph g = new Graph.graph();
        Graph.read_graph(g, false);
        Graph.print_graph(g);
        connected_components(g);
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
