/*    strong.c

    Identify strongly connected components in a graph
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

public class Strong {
    public static final int TREE = 0;
    public static final int BACK = 1;
    public static final int CROSS = 2;
    public static final int FORWARD = 3;
    public static final int MAXV = 100;
    public static final int STACKSIZE = 1000;
    public static int[] low = new int[(MAXV + 1)]; /* oldest vertex surely in component of v */
    public static int[] scc = new int[(MAXV + 1)]; /* strong component number for each vertex */
    public static Stack.stack active = new Stack.stack(); /* active vertices of unassigned component */
    public static int components_found = 0; /* number of strong components identified */

    public static void process_vertex_early(int v) {
        Stack.push(active, v);
    }

    public static void pop_component(int v) {
        int t = 0; /* vertex placeholder */
        components_found = (components_found + 1);
        System.out.printf(Locale.US, "%d is in component %d \n", v, components_found);
        scc[v] = components_found;
        while (((t = Stack.pop(active)) != v)) {
            scc[t] = components_found;
            System.out.printf(Locale.US, "%d is in component %d \n", t, components_found);
        }
    }

    public static void process_vertex_late(int v) {
        if ((low[v] == v)) {
            pop_component(v);
        }
        if (((BfsDfs.parent[v] != (-1)) && (BfsDfs.entry_time[low[v]] < BfsDfs.entry_time[low[BfsDfs.parent[v]]]))) {
            low[BfsDfs.parent[v]] = low[v];
        }
    }

    public static void process_edge(int x, int y) {
        int edge_class = 0;
        edge_class = BfsDfs.edge_classification(x, y);
        if ((edge_class == BACK)) {
            if ((BfsDfs.entry_time[y] < BfsDfs.entry_time[low[x]])) {
                low[x] = y;
            }
        }
        if ((edge_class == CROSS)) {
            if ((scc[y] == (-1))) { /* component not yet assigned */
                if ((BfsDfs.entry_time[y] < BfsDfs.entry_time[low[x]])) {
                    low[x] = y;
                }
            }
        }
    }

    public static void strong_components(Graph.graph g) {
        int i = 0; /* counter */
        for (i = 1; (i <= g.nvertices); i++) {
            low[i] = i;
            scc[i] = (-1);
        }
        components_found = 0;
        Stack.init_stack(active);
        BfsDfs.initialize_search(g);
        for (i = 1; (i <= g.nvertices); i++) {
            if (!(BfsDfs.discovered[i])) {
                BfsDfs.dfs(g, i);
            }
        }
    }

    public static int main() {
        BfsDfs.callbacks = new BfsDfs.Callbacks() {
            public void process_vertex_early(int v) { Strong.process_vertex_early(v); }
            public void process_vertex_late(int v) { Strong.process_vertex_late(v); }
            public void process_edge(int x, int y) { Strong.process_edge(x, y); }
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
