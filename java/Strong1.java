/*    strong1.c

    Identify strongly connected components in a graph (via Kosaraju-Sharir)
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

public class Strong1 {
    public static final int TREE = 0;
    public static final int BACK = 1;
    public static final int CROSS = 2;
    public static final int FORWARD = 3;
    public static final int MAXV = 100;
    public static final int STACKSIZE = 1000;
    public static int[] low = new int[(MAXV + 1)]; /* oldest vertex surely in component of v */
    public static int[] scc = new int[(MAXV + 1)]; /* strong component number for each vertex */
    public static Stack.stack dfs1order = new Stack.stack(); /* stack for reverse finishing order */
    public static Stack.stack active = new Stack.stack(); /* active vertices of unassigned component */
    public static int components_found = 0; /* number of strong components identified */

    /* replicate dfs call so it can use different process vertex functions */
    public static void dfs2(Graph.graph g, int v) {
        Graph.edgenode p = null; /* temporary pointer */
        int y = 0; /* successor vertex */
        if (BfsDfs.finished) {
            return; /* allow for search termination */
        }
        BfsDfs.discovered[v] = true;
        BfsDfs.time = (BfsDfs.time + 1);
        BfsDfs.entry_time[v] = BfsDfs.time;
        process_vertex_early2(v);
        p = g.edges[v];
        while ((p != null)) {
            y = p.y;
            if (!(BfsDfs.discovered[y])) {
                BfsDfs.parent[y] = v;
                process_edge2(v, y);
                dfs2(g, y);
            } else {
                if (((!(BfsDfs.processed[y]) && (BfsDfs.parent[v] != y)) || (g.directed != 0))) {
                    process_edge2(v, y);
                }
            }
            if (BfsDfs.finished) {
                return;
            }
            p = p.next;
        }
        process_vertex_late2(v);
        BfsDfs.time = (BfsDfs.time + 1);
        BfsDfs.exit_time[v] = BfsDfs.time;
        BfsDfs.processed[v] = true;
    }

    public static void process_vertex_early(int v) {
    }

    public static void process_vertex_late(int v) {
        Stack.push(dfs1order, v);
    }

    public static void process_edge(int x, int y) {
    }

    public static void process_vertex_early2(int v) {
        System.out.printf(Locale.US, " %d", v);
    }

    public static void process_vertex_late2(int v) {
    }

    public static void process_edge2(int x, int y) {
    }

    public static void strong_components(Graph.graph g) {
        Graph.graph gt = null; /* transpose of graph g */
        int i = 0; /* counter */
        int v = 0; /* vertex in component */
        Stack.init_stack(dfs1order);
        BfsDfs.initialize_search(g);
        for (i = 1; (i <= g.nvertices); i++) {
            if (!(BfsDfs.discovered[i])) {
                BfsDfs.dfs(g, i);
            }
        }
        gt = Graph.transpose(g);
        BfsDfs.initialize_search(gt);
        components_found = 0;
        while (!((Stack.empty_stack(dfs1order) != 0))) {
            v = Stack.pop(dfs1order);
            if (!(BfsDfs.discovered[v])) {
                components_found++;
                System.out.printf(Locale.US, "Component %d:", components_found);
                dfs2(gt, v);
                System.out.print("\n");
            }
        }
    }

    public static int main() {
        BfsDfs.callbacks = new BfsDfs.Callbacks() {
            public void process_vertex_early(int v) { Strong1.process_vertex_early(v); }
            public void process_vertex_late(int v) { Strong1.process_vertex_late(v); }
            public void process_edge(int x, int y) { Strong1.process_edge(x, y); }
        };
        Graph.graph g = new Graph.graph();
        Graph.read_graph(g, true);
        Graph.print_graph(g);
        strong_components(g);
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
