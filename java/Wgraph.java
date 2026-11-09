/*    wgraph.c

    A generic weighted graph data type
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

public class Wgraph {
    public static final int TREE = 0; /* tree edge */
    public static final int BACK = 1; /* back edge */
    public static final int CROSS = 2; /* cross edge */
    public static final int FORWARD = 3; /* forward edge */
    public static final int MAXV = 100; /* maximum number of vertices */
    public static boolean[] processed = new boolean[(MAXV + 1)]; /* which vertices have been processed */
    public static boolean[] discovered = new boolean[(MAXV + 1)]; /* which vertices have been found */
    public static int[] parent = new int[(MAXV + 1)]; /* discovery relation */
    public static int[] entry_time = new int[(MAXV + 1)]; /* time of vertex entry */
    public static int[] exit_time = new int[(MAXV + 1)]; /* time of vertex exit */
    public static int time = 0; /* current event time */
    public static boolean finished = false; /* if true, cut off search immediately */

    public static void initialize_graph(Graph.graph g, boolean directed) {
        int i = 0; /* counter */
        g.nvertices = 0;
        g.nedges = 0;
        g.directed = (directed ? 1 : 0);
        for (i = 1; (i <= MAXV); i++) {
            g.degree[i] = 0;
        }
        for (i = 1; (i <= MAXV); i++) {
            g.edges[i] = null;
        }
    }

    public static void insert_edge(Graph.graph g, int x, int y, boolean directed, int w) {
        Graph.edgenode p = null; /* temporary pointer */
        p = new Graph.edgenode();
        p.y = y;
        p.weight = w;
        p.next = g.edges[x];
        g.edges[x] = p;
        g.degree[x]++;
        if (!(directed)) {
            insert_edge(g, y, x, true, w);
        } else {
            g.nedges++;
        }
    }

    public static void read_graph(Graph.graph g, boolean directed) {
        int i = 0; /* counter */
        int m = 0; /* number of edges */
        int x = 0;
        int y = 0;
        int w = 0;
        initialize_graph(g, directed);
        int _read0 = C.scan("%d %d\n");
        if (_read0 > 0) g.nvertices = C.scanInt(0);
        if (_read0 > 1) m = C.scanInt(1);
        for (i = 1; (i <= m); i++) {
            int _read1 = C.scan("%d %d %d\n");
            if (_read1 > 0) x = C.scanInt(0);
            if (_read1 > 1) y = C.scanInt(1);
            if (_read1 > 2) w = C.scanInt(2);
            insert_edge(g, x, y, directed, w); /* placeholder for edge and weight */
        }
    }

    public static void delete_edge(Graph.graph g, int x, int y, boolean directed) {
        Graph.edgenode p = null; /* temporary pointers */
        Graph.edgenode p_back = null;
        p = g.edges[x];
        p_back = null;
        while ((p != null)) {
            if ((p.y == y)) {
                g.degree[x]--;
                if ((p_back != null)) {
                    p_back.next = p.next;
                } else {
                    g.edges[x] = p.next;
                }
                // Java garbage collection releases p;
                if (!(directed)) {
                    delete_edge(g, y, x, true);
                } else {
                    g.nedges--;
                }
                return;
            } else {
                p_back = p;
                p = p.next;
            }
        }
        System.out.printf(Locale.US, "Warning: deletion(%d,%d) not found in g.\n", x, y);
    }

    public static void print_graph(Graph.graph g) {
        int i = 0; /* counter */
        Graph.edgenode p = null; /* temporary pointer */
        for (i = 1; (i <= g.nvertices); i++) {
            System.out.printf(Locale.US, "%d: ", i);
            p = g.edges[i];
            while ((p != null)) {
                System.out.printf(Locale.US, " %d", p.y);
                p = p.next;
            }
            System.out.print("\n");
        }
    }

    public static void initialize_search(Graph.graph g) {
        int i = 0; /* counter */
        time = 0;
        for (i = 0; (i <= g.nvertices); i++) {
            processed[i] = (discovered[i] = false);
            parent[i] = (-1);
        }
    }

    public static void process_vertex_early(int v) { /* vertex to process */
        System.out.printf(Locale.US, " %d", v);
    }

    public static void process_vertex_late(int v) { /* vertex to process */
    }

    public static void process_edge(int x, int y) { /* edge to process */
    }

    public static void dfs(Graph.graph g, int v) {
        Graph.edgenode p = null; /* temporary pointer */
        int y = 0; /* successor vertex */
        boolean parent_edge_seen = false;
        boolean self_edge_seen = false;
        if (finished) {
            return; /* allow for search termination */
        }
        discovered[v] = true;
        time = (time + 1);
        entry_time[v] = time;
        process_vertex_early(v);
        p = g.edges[v];
        while ((p != null)) {
            y = p.y;
            if (!(discovered[y])) {
                parent[y] = v;
                process_edge(v, y);
                dfs(g, y);
            } else {
                if ((!(processed[y]) || (g.directed != 0))) {
                    if (((y == v) && !((g.directed != 0)))) {
                        self_edge_seen = !(self_edge_seen);
                        if (self_edge_seen) {
                            process_edge(v, y);
                        }
                    } else {
                        if ((((g.directed != 0) || (y != parent[v])) || parent_edge_seen)) {
                            process_edge(v, y);
                        }
                        if ((y == parent[v])) {
                            parent_edge_seen = true;
                        }
                    }
                }
            }
            if (finished) {
                return;
            }
            p = p.next;
        }
        process_vertex_late(v);
        time = (time + 1);
        exit_time[v] = time;
        processed[v] = true;
    }

    public static int find_path(int start, int end, int[] parents) {
        if ((end == (-1))) {
            System.out.print("\nNo path");
            return 0;
        }
        if ((start == end)) {
            System.out.printf(Locale.US, "\n%d", start);
        } else {
            if (!((find_path(start, parents[end], parents) != 0))) {
                return 0;
            }
            System.out.printf(Locale.US, " %d", end);
        }
        return 1;
    }

    public static void connected_components(Graph.graph g) { /* graph to analyze */
        int c = 0; /* component number */
        int i = 0; /* counter */
        initialize_search(g);
        c = 0;
        for (i = 1; (i <= g.nvertices); i++) {
            if (!(discovered[i])) {
                c = (c + 1);
                System.out.printf(Locale.US, "Component %d:", c);
                dfs(g, i);
                System.out.print("\n");
            }
        }
    }

}
