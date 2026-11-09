/*	biconnected.c
	Identify articulation vertices in a graph
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

public class Biconnected {
    public static final int TREE = 0;
    public static final int BACK = 1;
    public static final int CROSS = 2;
    public static final int FORWARD = 3;
    public static final int MAXV = 100;
    public static final int QUEUESIZE = 1000;
    public static int[] reachable_ancestor = new int[(MAXV + 1)]; /* earliest reachable ancestor of v */
    public static int[] tree_out_degree = new int[(MAXV + 1)]; /* DFS tree outdegree of v */

    public static void process_vertex_early(int v) {
        reachable_ancestor[v] = v;
    }

    public static void process_vertex_late(int v) {
        boolean root = false; /* is parent[v] the root of the DFS tree? */
        int time_v = 0; /* earliest reachable time for v */
        int time_parent = 0; /* earliest reachable time for parent[v] */
        if ((BfsDfs.parent[v] == (-1))) { /* test if v is the root */
            if ((tree_out_degree[v] > 1)) {
                System.out.printf(Locale.US, "root articulation vertex: %d \n", v);
            }
            return;
        }
        root = (BfsDfs.parent[BfsDfs.parent[v]] == (-1)); /* is parent[v] the root? */
        if (!root) {
            if ((reachable_ancestor[v] == BfsDfs.parent[v])) {
                System.out.printf(Locale.US, "parent articulation vertex: %d \n", BfsDfs.parent[v]);
            }
            if ((reachable_ancestor[v] == v)) {
                System.out.printf(Locale.US, "bridge articulation vertex: %d \n", BfsDfs.parent[v]);
                if ((tree_out_degree[v] > 0)) { /* is v is not a leaf? */
                    System.out.printf(Locale.US, "bridge articulation vertex: %d \n", v);
                }
            }
        }
        time_v = BfsDfs.entry_time[reachable_ancestor[v]];
        time_parent = BfsDfs.entry_time[reachable_ancestor[BfsDfs.parent[v]]];
        if ((time_v < time_parent)) {
            reachable_ancestor[BfsDfs.parent[v]] = reachable_ancestor[v];
        }
    }

    public static void process_edge(int x, int y) {
        int edge_class = 0;
        edge_class = BfsDfs.edge_classification(x, y);
        if ((edge_class == TREE)) {
            tree_out_degree[x] = (tree_out_degree[x] + 1);
        }
        if (((edge_class == BACK) && (BfsDfs.parent[x] != y))) {
            if ((BfsDfs.entry_time[y] < BfsDfs.entry_time[reachable_ancestor[x]])) {
                reachable_ancestor[x] = y;
            }
        }
    }

    public static void articulation_vertices(Graph.graph g) {
        int i = 0; /* counter */
        for (i = 1; (i <= g.nvertices); i++) {
            tree_out_degree[i] = 0;
        }
        BfsDfs.initialize_search(g);
        for (i = 1; (i <= g.nvertices); i++) {
            if (!BfsDfs.discovered[i]) {
                BfsDfs.dfs(g, i);
            }
        }
    }

    public static int main() {
        BfsDfs.callbacks = new BfsDfs.Callbacks() {
            public void process_vertex_early(int v) { Biconnected.process_vertex_early(v); }
            public void process_vertex_late(int v) { Biconnected.process_vertex_late(v); }
            public void process_edge(int x, int y) { Biconnected.process_edge(x, y); }
        };
        Graph.graph g = new Graph.graph();
        Graph.read_graph(g, false);
        Graph.print_graph(g);
        articulation_vertices(g);
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
