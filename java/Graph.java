/*	graph.c

	A generic adjacency list graph data type.
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

public class Graph {
    public static final int QUEUESIZE = 1000;
    public static final int TREE = 0; /* tree edge */
    public static final int BACK = 1; /* back edge */
    public static final int CROSS = 2; /* cross edge */
    public static final int FORWARD = 3; /* forward edge */
    public static final int MAXV = 100; /* maximum number of vertices */
    public static class edgenode {
        int y = 0; /* adjacency info */
        int weight = 0; /* edge weight, if any */
        Graph.edgenode next = null; /* next edge in list */
    }
    public static class graph {
        Graph.edgenode[] edges = new Graph.edgenode[(MAXV + 1)]; /* adjacency info */
        int[] degree = new int[(MAXV + 1)]; /* outdegree of each vertex */
        int nvertices = 0; /* number of vertices in the graph */
        int nedges = 0; /* number of edges in the graph */
        int directed = 0; /* is the graph directed? */
    }

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

    public static void insert_edge(Graph.graph g, int x, int y, boolean directed) {
        Graph.edgenode p = null; /* temporary pointer */
        p = new Graph.edgenode(); /* allocate edgenode storage */
        p.weight = 0;
        p.y = y;
        p.next = g.edges[x];
        g.edges[x] = p; /* insert at head of list */
        g.degree[x]++;
        if (!directed) {
            insert_edge(g, y, x, true);
        } else {
            g.nedges++;
        }
    }

    public static void read_graph(Graph.graph g, boolean directed) {
        int i = 0; /* counter */
        int m = 0; /* number of edges */
        int x = 0; /* vertices in edge (x,y) */
        int y = 0;
        initialize_graph(g, directed);
        int _read0 = C.scan("%d %d");
        if (_read0 > 0) g.nvertices = C.scanInt(0);
        if (_read0 > 1) m = C.scanInt(1);
        for (i = 1; (i <= m); i++) {
            int _read1 = C.scan("%d %d");
            if (_read1 > 0) x = C.scanInt(0);
            if (_read1 > 1) y = C.scanInt(1);
            insert_edge(g, x, y, directed);
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
                if (!directed) {
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

    public static Graph.graph transpose(Graph.graph g) {
        Graph.graph gt = null; /* transpose of graph g */
        int x = 0; /* counter */
        Graph.edgenode p = null; /* temporary pointer */
        gt = new Graph.graph();
        initialize_graph(gt, true); /* initialize directed graph */
        gt.nvertices = g.nvertices;
        for (x = 1; (x <= g.nvertices); x++) {
            p = g.edges[x];
            while ((p != null)) {
                insert_edge(gt, p.y, x, true);
                p = p.next;
            }
        }
        return gt;
    }

}
