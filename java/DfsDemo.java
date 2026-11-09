/*	dfs-demo.c

	Driver program demonstrating DFS numbering and edge labeling.
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

public class DfsDemo {
    public static final int TREE = 0;
    public static final int BACK = 1;
    public static final int CROSS = 2;
    public static final int FORWARD = 3;
    public static final int MAXV = 100;
    public static final int QUEUESIZE = 1000;

    /* discovery relation */
    public static void process_vertex_early(int v) {
        BfsDfs.time = (BfsDfs.time + 1);
        BfsDfs.entry_time[v] = BfsDfs.time;
        System.out.printf(Locale.US, "entered vertex %d at time %d\n", v, BfsDfs.entry_time[v]);
    }

    public static void process_vertex_late(int v) {
        BfsDfs.time = (BfsDfs.time + 1);
        BfsDfs.exit_time[v] = BfsDfs.time;
        System.out.printf(Locale.US, "exit vertex %d at time %d\n", v, BfsDfs.exit_time[v]);
    }

    public static void process_edge(int x, int y) {
        int edge_class = 0;
        edge_class = BfsDfs.edge_classification(x, y);
        if ((edge_class == BACK)) {
            System.out.printf(Locale.US, "back edge (%d,%d)\n", x, y);
        } else {
            if ((edge_class == TREE)) {
                System.out.printf(Locale.US, "tree edge (%d,%d)\n", x, y);
            } else {
                if ((edge_class == FORWARD)) {
                    System.out.printf(Locale.US, "forward edge (%d,%d)\n", x, y);
                } else {
                    if ((edge_class == CROSS)) {
                        System.out.printf(Locale.US, "cross edge (%d,%d)\n", x, y);
                    } else {
                        System.out.printf(Locale.US, "edge (%d,%d)\n not in valid class=%d", x, y, edge_class);
                    }
                }
            }
        }
    }

    public static int main() {
        BfsDfs.callbacks = new BfsDfs.Callbacks() {
            public void process_vertex_early(int v) { DfsDemo.process_vertex_early(v); }
            public void process_vertex_late(int v) { DfsDemo.process_vertex_late(v); }
            public void process_edge(int x, int y) { DfsDemo.process_edge(x, y); }
        };
        Graph.graph g = new Graph.graph();
        int i = 0;
        Graph.read_graph(g, false);
        Graph.print_graph(g);
        BfsDfs.initialize_search(g);
        BfsDfs.dfs(g, 1);
        for (i = 1; (i <= g.nvertices); i++) {
            BfsDfs.find_path(1, i, BfsDfs.parent);
        }
        System.out.print("\n");
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
