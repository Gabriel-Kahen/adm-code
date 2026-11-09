/*	bipartite.c
	Two color a bipartite graph
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

public class Bipartite {
    public static final int TREE = 0;
    public static final int BACK = 1;
    public static final int CROSS = 2;
    public static final int FORWARD = 3;
    public static final int MAXV = 100;
    public static final int QUEUESIZE = 1000;
    public static final int UNCOLORED = 0; /* vertex not yet colored */
    public static final int WHITE = 1; /* white vertex */
    public static final int BLACK = 2; /* black vertex */
    public static int[] color = new int[(MAXV + 1)]; /* assigned color of v */
    public static boolean bipartite = false; /* is the graph bipartite? */

    public static void process_vertex_early(int v) {
    }

    public static void process_vertex_late(int v) {
    }

    public static int complement(int color) {
        if ((color == WHITE)) {
            return BLACK;
        }
        if ((color == BLACK)) {
            return WHITE;
        }
        return UNCOLORED;
    }

    public static void process_edge(int x, int y) {
        if ((color[x] == color[y])) {
            bipartite = false;
            System.out.printf(Locale.US, "Warning: not bipartite, due to (%d,%d)\n", x, y);
        }
        color[y] = complement(color[x]);
    }

    public static void twocolor(Graph.graph g) {
        int i = 0; /* counter */
        for (i = 1; (i <= g.nvertices); i++) {
            color[i] = UNCOLORED;
        }
        bipartite = true;
        BfsDfs.initialize_search(g);
        for (i = 1; (i <= g.nvertices); i++) {
            if (!(BfsDfs.discovered[i])) {
                color[i] = WHITE;
                BfsDfs.bfs(g, i);
            }
        }
    }

    public static int main() {
        BfsDfs.callbacks = new BfsDfs.Callbacks() {
            public void process_vertex_early(int v) { Bipartite.process_vertex_early(v); }
            public void process_vertex_late(int v) { Bipartite.process_vertex_late(v); }
            public void process_edge(int x, int y) { Bipartite.process_edge(x, y); }
        };
        Graph.graph g = new Graph.graph();
        int i = 0;
        Graph.read_graph(g, false);
        Graph.print_graph(g);
        twocolor(g);
        for (i = 1; (i <= g.nvertices); i++) {
            System.out.printf(Locale.US, " %d", color[i]);
        }
        System.out.print("\n");
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
