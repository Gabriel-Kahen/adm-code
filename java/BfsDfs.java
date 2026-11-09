/*	bfs-dfs.c
	Generic implementation of graph traversal: breadth-first/depth-first search
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

public class BfsDfs {
    public interface Callbacks {
        void process_vertex_early(int v);
        void process_vertex_late(int v);
        void process_edge(int x, int y);
    }
    public static Callbacks callbacks;

    public static final int TREE = 0;
    public static final int BACK = 1;
    public static final int CROSS = 2;
    public static final int FORWARD = 3;
    public static final int MAXV = 100;
    public static final int QUEUESIZE = 1000;
    public static boolean[] processed = new boolean[(MAXV + 1)]; /* which vertices have been processed */
    public static boolean[] discovered = new boolean[(MAXV + 1)]; /* which vertices have been found */
    public static int[] parent = new int[(MAXV + 1)]; /* discovery relation */
    public static int[] entry_time = new int[(MAXV + 1)]; /* time of vertex entry */
    public static int[] exit_time = new int[(MAXV + 1)]; /* time of vertex exit */
    public static int time = 0; /* current event time */
    public static boolean finished = false; /* if true, cut off search immediately */

    public static void initialize_search(Graph.graph g) {
        int i = 0; /* counter */
        time = 0;
        for (i = 0; (i <= g.nvertices); i++) {
            processed[i] = false;
            discovered[i] = false;
            parent[i] = (-1);
        }
    }

    public static void bfs(Graph.graph g, int start) {
        Queue.queue q = new Queue.queue(); /* queue of vertices to visit */
        int v = 0; /* current vertex */
        int y = 0; /* successor vertex */
        Graph.edgenode p = null; /* temporary pointer */
        Queue.init_queue(q);
        Queue.enqueue(q, start);
        discovered[start] = true;
        while (!((Queue.empty_queue(q) != 0))) {
            v = Queue.dequeue(q);
            callbacks.process_vertex_early(v);
            processed[v] = true;
            p = g.edges[v];
            while ((p != null)) {
                y = p.y;
                if (((!(processed[y]) || (g.directed != 0)) || (y == v))) {
                    callbacks.process_edge(v, y);
                }
                if (!(discovered[y])) {
                    Queue.enqueue(q, y);
                    discovered[y] = true;
                    parent[y] = v;
                }
                p = p.next;
            }
            callbacks.process_vertex_late(v);
        }
    }

    public static int edge_classification(int x, int y) {
        if ((parent[y] == x)) {
            return TREE;
        }
        if ((discovered[y] && !(processed[y]))) {
            return BACK;
        }
        if ((processed[y] && (entry_time[y] > entry_time[x]))) {
            return FORWARD;
        }
        if ((processed[y] && (entry_time[y] < entry_time[x]))) {
            return CROSS;
        }
        C.printf("Warning: self loop (%d,%d)\n", x, y);
        return (-1);
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
        callbacks.process_vertex_early(v);
        p = g.edges[v];
        while ((p != null)) {
            y = p.y;
            if (!(discovered[y])) {
                parent[y] = v;
                callbacks.process_edge(v, y);
                dfs(g, y);
            } else {
                if ((!(processed[y]) || (g.directed != 0))) {
                    if (((y == v) && !((g.directed != 0)))) {
                        self_edge_seen = !(self_edge_seen);
                        if (self_edge_seen) {
                            callbacks.process_edge(v, y);
                        }
                    } else {
                        if ((((g.directed != 0) || (y != parent[v])) || parent_edge_seen)) {
                            callbacks.process_edge(v, y);
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
        callbacks.process_vertex_late(v);
        time = (time + 1);
        exit_time[v] = time;
        processed[v] = true;
    }

    public static int find_path(int start, int end, int[] parents) {
        if ((end == (-1))) {
            C.printf("\nNo path");
            return 0;
        }
        if ((start == end)) {
            C.printf("\n%d", start);
        } else {
            if (!((find_path(start, parents[end], parents) != 0))) {
                return 0;
            }
            C.printf(" %d", end);
        }
        return 1;
    }

}
