/*	floyd.c

	Compute all-pairs shortest paths in weighted graphs.
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

import java.util.Locale;

public class Floyd {
    public static final int MAXV = 100; /* maximum number of vertices */
    public static final int MAXDEGREE = 50; /* maximum outdegree of a vertex */
    public static final long MAXINT = (Long.MAX_VALUE / 4);
    public static class edge {
        int v = 0; /* neighboring vertex */
        int weight = 0; /* edge weight */
        boolean in = false; /* is the edge "in" the solution? */
    }
    public static class graph {
        Floyd.edge[][] edges = new Floyd.edge[(MAXV + 1)][MAXDEGREE]; /* adjacency info */
        {
            for (int _i0 = 0; _i0 < (MAXV + 1); _i0++) {
                for (int _i1 = 0; _i1 < MAXDEGREE; _i1++) {
                    edges[_i0][_i1] = new Floyd.edge();
                }
            }
        }
        int[] degree = new int[(MAXV + 1)]; /* outdegree of each vertex */
        int nvertices = 0; /* number of vertices in graph */
        int nedges = 0; /* number of edges in the graph */
    }
    public static class adjacency_matrix {
        long[][] weight = new long[(MAXV + 1)][(MAXV + 1)]; /* adjacency/weight info */
        int nvertices = 0; /* number of vertices in graph */
    }

    public static void initialize_adjacency_matrix(Floyd.adjacency_matrix g) {
        int i = 0; /* counters */
        int j = 0;
        g.nvertices = 0;
        for (i = 1; (i <= MAXV); i++) {
            for (j = 1; (j <= MAXV); j++) {
                g.weight[i][j] = ((i == j) ? 0 : MAXINT);
            }
        }
    }

    public static void read_adjacency_matrix(Floyd.adjacency_matrix g, boolean directed) {
        int i = 0; /* counter */
        int m = 0; /* number of edges */
        int x = 0;
        int y = 0;
        int w = 0;
        initialize_adjacency_matrix(g);
        int _read0 = C.scan("%d %d\n");
        if (_read0 > 0) g.nvertices = C.scanInt(0);
        if (_read0 > 1) m = C.scanInt(1);
        for (i = 1; (i <= m); i++) {
            int _read1 = C.scan("%d %d %d\n");
            if (_read1 > 0) x = C.scanInt(0);
            if (_read1 > 1) y = C.scanInt(1);
            if (_read1 > 2) w = C.scanInt(2);
            if ((w < g.weight[x][y])) {
                g.weight[x][y] = w; /* placeholder for edge and weight */
            }
            if (!(directed)) {
                if ((w < g.weight[y][x])) {
                    g.weight[y][x] = w;
                }
            }
        }
    }

    public static void print_graph(Floyd.adjacency_matrix g) {
        int i = 0; /* counters */
        int j = 0;
        for (i = 1; (i <= g.nvertices); i++) {
            System.out.printf(Locale.US, "%d: ", i);
            for (j = 1; (j <= g.nvertices); j++) {
                if ((g.weight[i][j] < MAXINT)) {
                    System.out.printf(Locale.US, " %d", j);
                }
            }
            System.out.print("\n");
        }
    }

    public static void print_adjacency_matrix(Floyd.adjacency_matrix g) {
        int i = 0; /* counters */
        int j = 0;
        for (i = 1; (i <= g.nvertices); i++) {
            System.out.printf(Locale.US, "%3d: ", i);
            for (j = 1; (j <= g.nvertices); j++) {
                System.out.printf(Locale.US, " %3d", g.weight[i][j]);
            }
            System.out.print("\n");
        }
    }

    public static void floyd(Floyd.adjacency_matrix g) {
        int i = 0; /* dimension counters */
        int j = 0;
        int k = 0; /* intermediate vertex counter */
        long through_k = 0; /* distance through vertex k */
        /* Phase k permits intermediate vertices 1..k on each shortest path. */
        for (k = 1; (k <= g.nvertices); k++) {
            for (i = 1; (i <= g.nvertices); i++) {
                for (j = 1; (j <= g.nvertices); j++) {
                    /* The sentinel represents no path and must never participate in addition. */
                    if (((g.weight[i][k] == MAXINT) || (g.weight[k][j] == MAXINT))) {
                        continue;
                    }
                    through_k = (g.weight[i][k] + g.weight[k][j]);
                    if ((through_k < g.weight[i][j])) {
                        g.weight[i][j] = through_k;
                    }
                }
            }
        }
    }

    public static int main() {
        Floyd.adjacency_matrix g = new Floyd.adjacency_matrix();
        read_adjacency_matrix(g, false);
        print_graph(g);
        floyd(g);
        print_adjacency_matrix(g);
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
