/*    netflow.c

      Network flow implementation -- Ford-Fulkerson augmenting path algorithm.
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

public class Netflow {
    public static final double PI = 3.1415926; /* ratio of circumference to diameter */
    public static final double EPSILON = 0.000001; /* a quantity small enough to be zero */
    public static final int DIMENSION = 2; /* dimension of points */
    public static final int X = 0; /* x-coordinate index */
    public static final int Y = 1; /* y-coordinate index */
    public static final int MAXPOLY = 200; /* maximum number of points in a polygon */
    public static final int QUEUESIZE = 1000;
    public static final int MAXV = 100; /* maximum number of vertices */
    public static final int MAXDEGREE = 50; /* maximum outdegree of a vertex */
    public static class edgenode {
        int v = 0; /* neighboring vertex */
        long capacity = 0; /* capacity of edge */
        long flow = 0; /* signed net flow; reverse edge stores its negative */
        long residual = 0; /* residual capacity of edge */
        Netflow.edgenode next = null; /* next edge in list */
    }
    public static class flow_graph {
        Netflow.edgenode[] edges = new Netflow.edgenode[(MAXV + 1)]; /* adjacency info */
        int[] degree = new int[(MAXV + 1)]; /* outdegree of each vertex */
        int nvertices = 0; /* number of vertices in the graph */
        int nedges = 0; /* number of edges in the graph */
    }
    public static boolean[] processed = new boolean[(MAXV + 1)]; /* which vertices have been processed */
    public static boolean[] discovered = new boolean[(MAXV + 1)]; /* which vertices have been found */
    public static int[] parent = new int[(MAXV + 1)]; /* discovery relation */
    public static boolean finished = false; /* if true, cut off search immediately */

    public static void initialize_graph(Netflow.flow_graph g) { /* graph to initialize */
        int i = 0; /* counter */
        g.nvertices = 0;
        g.nedges = 0;
        for (i = 0; (i <= MAXV); i++) {
            g.degree[i] = 0;
        }
        for (i = 0; (i <= MAXV); i++) {
            g.edges[i] = null;
        }
    }

    public static void insert_flow_edge(Netflow.flow_graph g, int x, int y, boolean directed, int w) {
        Netflow.edgenode edge = null; /* temporary pointer */
        Netflow.edgenode parallel_edge = find_edge(g, x, y);
        /* Parallel arcs share a single residual-capacity entry. */
        if ((parallel_edge != null)) {
            parallel_edge.capacity += w;
            parallel_edge.residual += w;
            if (!(directed)) {
                insert_flow_edge(g, y, x, true, w);
            }
            return;
        }
        edge = new Netflow.edgenode(); /* allocate storage for edgenode */
        edge.v = y;
        edge.capacity = w;
        edge.flow = 0;
        edge.residual = w;
        edge.next = g.edges[x];
        g.edges[x] = edge; /* insert at head of list */
        g.degree[x]++;
        if (!(directed)) {
            insert_flow_edge(g, y, x, true, w);
        } else {
            g.nedges++;
        }
    }

    public static void read_flow_graph(Netflow.flow_graph g, boolean directed) {
        int i = 0; /* counter */
        int m = 0; /* number of edges */
        int x = 0;
        int y = 0;
        int w = 0;
        initialize_graph(g);
        int _read0 = C.scan("%d %d\n");
        if (_read0 > 0) g.nvertices = C.scanInt(0);
        if (_read0 > 1) m = C.scanInt(1);
        for (i = 1; (i <= m); i++) {
            int _read1 = C.scan("%d %d %d\n");
            if (_read1 > 0) x = C.scanInt(0);
            if (_read1 > 1) y = C.scanInt(1);
            if (_read1 > 2) w = C.scanInt(2);
            insert_flow_edge(g, x, y, directed, w); /* placeholder for edge and weight */
        }
    }

    public static Netflow.edgenode find_edge(Netflow.flow_graph g, int x, int y) {
        Netflow.edgenode p = null; /* temporary pointer */
        p = g.edges[x];
        while ((p != null)) {
            if ((p.v == y)) {
                return p;
            }
            p = p.next;
        }
        return null;
    }

    public static void add_residual_edges(Netflow.flow_graph g) {
        int i = 0; /* counter */
        Netflow.edgenode p = null; /* temporary pointer */
        for (i = 1; (i <= g.nvertices); i++) {
            p = g.edges[i];
            while ((p != null)) {
                if ((find_edge(g, p.v, i) == null)) {
                    insert_flow_edge(g, p.v, i, true, 0);
                }
                p = p.next;
            }
        }
    }

    public static void print_flow_graph(Netflow.flow_graph g) {
        int i = 0; /* counter */
        Netflow.edgenode p = null; /* temporary pointer */
        for (i = 1; (i <= g.nvertices); i++) {
            C.printf("%d: ", i);
            p = g.edges[i];
            while ((p != null)) {
                C.printf(" %d(%lld,%lld,%lld)", p.v, p.capacity, p.flow, p.residual);
                p = p.next;
            }
            C.printf("\n");
        }
    }

    public static void initialize_search(Netflow.flow_graph g) { /* graph to traverse */
        int i = 0; /* counter */
        for (i = 1; (i <= g.nvertices); i++) {
            processed[i] = false;
            discovered[i] = false;
            parent[i] = (-1);
        }
    }

    public static void process_vertex_early(int v) { /* vertex to process */
    }

    public static void process_vertex_late(int v) { /* vertex to process */
    }

    public static void process_edge(int x, int y) { /* edge to process */
    }

    public static boolean valid_edge(Netflow.edgenode e) {
        return (e.residual > 0);
    }

    public static void bfs(Netflow.flow_graph g, int start) {
        Queue.queue q = new Queue.queue(); /* queue of vertices to visit */
        int v = 0; /* current vertex */
        int y = 0; /* successor vertex */
        Netflow.edgenode p = null; /* temporary pointer */
        Queue.init_queue(q);
        Queue.enqueue(q, start);
        discovered[start] = true;
        while (!((Queue.empty_queue(q) != 0))) {
            v = Queue.dequeue(q);
            process_vertex_early(v);
            processed[v] = true;
            p = g.edges[v];
            while ((p != null)) {
                y = p.v;
                if (valid_edge(p)) {
                    if (!(processed[y])) {
                        process_edge(v, y);
                    }
                    if (!(discovered[y])) {
                        Queue.enqueue(q, y);
                        discovered[y] = true;
                        parent[y] = v;
                    }
                }
                p = p.next;
            }
            process_vertex_late(v);
        }
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

    public static long path_volume(Netflow.flow_graph g, int start, int end) {
        Netflow.edgenode e = null; /* edge in question */
        if ((parent[end] == (-1))) {
            return 0;
        }
        e = find_edge(g, parent[end], end);
        if ((start == parent[end])) {
            return e.residual;
        } else {
            return Math.min(path_volume(g, start, parent[end]), e.residual);
        }
    }

    public static void augment_path(Netflow.flow_graph g, int start, int end, long volume) {
        Netflow.edgenode forward = null;
        Netflow.edgenode reverse = null;
        if ((start == end)) {
            return;
        }
        forward = find_edge(g, parent[end], end);
        forward.flow += volume;
        forward.residual -= volume;
        /* Reverse residual capacity permits undoing an earlier routing decision.
               Each direction stores the negative of its partner's net flow. */
        reverse = find_edge(g, end, parent[end]);
        reverse.flow -= volume;
        reverse.residual += volume;
        augment_path(g, start, parent[end], volume);
    }

    public static void netflow(Netflow.flow_graph g, int source, int sink) {
        long volume = 0; /* weight of the augmenting path */
        /* Every arc needs a reverse entry before augmentations can cancel flow. */
        add_residual_edges(g);
        initialize_search(g);
        bfs(g, source);
        volume = path_volume(g, source, sink);
        while ((volume > 0)) {
            augment_path(g, source, sink, volume);
            initialize_search(g);
            bfs(g, source);
            volume = path_volume(g, source, sink);
        }
    }

    public static int main() {
        Netflow.flow_graph g = new Netflow.flow_graph(); /* graph to analyze */
        int source = 0; /* source and sink vertices */
        int sink = 0;
        long flow = 0; /* total flow */
        Netflow.edgenode p = null; /* temporary pointer */
        int _read2 = C.scan("%d %d");
        if (_read2 > 0) source = C.scanInt(0);
        if (_read2 > 1) sink = C.scanInt(1);
        read_flow_graph(g, true);
        netflow(g, source, sink);
        print_flow_graph(g);
        flow = 0;
        p = g.edges[source];
        while ((p != null)) {
            flow += p.flow;
            p = p.next;
        }
        C.printf("total flow = %lld\n", flow);
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
