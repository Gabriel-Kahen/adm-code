/*    topsort1.c

    Topologically sort a directed acyclic graph by DFS numbering (DAG)
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

public class Topsort1 {
    public static final int TREE = 0;
    public static final int BACK = 1;
    public static final int CROSS = 2;
    public static final int FORWARD = 3;
    public static final int MAXV = 100;
    public static final int STACKSIZE = 1000;
    public static Stack.stack sorted = new Stack.stack(); /* topological ordering of vertices */

    /* time of vertex exit */
    public static void process_vertex_early(int v) {
    }

    public static void process_vertex_late(int v) {
        Stack.push(sorted, v);
    }

    public static void process_edge(int x, int y) {
        int edge_class = 0;
        edge_class = BfsDfs.edge_classification(x, y);
        if ((edge_class == BACK)) {
            C.printf("Warning: directed cycle found, not a DAG\n");
        }
    }

    public static void topsort(Graph.graph g) {
        int i = 0; /* counter */
        Stack.init_stack(sorted);
        for (i = 1; (i <= g.nvertices); i++) {
            if (!(BfsDfs.discovered[i])) {
                BfsDfs.dfs(g, i);
            }
        }
        Stack.print_stack(sorted); /* report topological order */
    }

    public static int main() {
        BfsDfs.callbacks = new BfsDfs.Callbacks() {
            public void process_vertex_early(int v) { Topsort1.process_vertex_early(v); }
            public void process_vertex_late(int v) { Topsort1.process_vertex_late(v); }
            public void process_edge(int x, int y) { Topsort1.process_edge(x, y); }
        };
        Graph.graph g = new Graph.graph();
        Graph.read_graph(g, true);
        Graph.print_graph(g);
        topsort(g);
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
