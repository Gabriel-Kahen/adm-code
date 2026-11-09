/*	findcycle.c

	Identify a cycle in a graph, if one exists.
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

public class Findcycle {
    public static final int TREE = 0;
    public static final int BACK = 1;
    public static final int CROSS = 2;
    public static final int FORWARD = 3;
    public static final int MAXV = 100;

    /* flag for early search cutoff */
    public static void process_vertex_early(int v) {
    }

    public static void process_vertex_late(int v) {
    }

    public static void process_edge(int x, int y) {
        if ((BfsDfs.parent[y] != x)) { /* found back edge! */
            C.printf("Cycle from %d to %d:", y, x);
            BfsDfs.find_path(y, x, BfsDfs.parent);
            BfsDfs.finished = true;
        }
    }

    public static int main() {
        BfsDfs.callbacks = new BfsDfs.Callbacks() {
            public void process_vertex_early(int v) { Findcycle.process_vertex_early(v); }
            public void process_vertex_late(int v) { Findcycle.process_vertex_late(v); }
            public void process_edge(int x, int y) { Findcycle.process_edge(x, y); }
        };
        Graph.graph g = new Graph.graph();
        Graph.read_graph(g, false);
        Graph.print_graph(g);
        BfsDfs.initialize_search(g);
        BfsDfs.dfs(g, 1);
        C.printf("\n");
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
