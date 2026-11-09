/*    topsort.c

    Topologically sort a directed acyclic graph (DAG) by indegre-zero deletion.
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

public class Topsort {
    public static final int TREE = 0;
    public static final int BACK = 1;
    public static final int CROSS = 2;
    public static final int FORWARD = 3;
    public static final int MAXV = 100;
    public static final int QUEUESIZE = 1000;

    public static void compute_indegrees(Graph.graph g, int[] in) {
        int i = 0; /* counter */
        Graph.edgenode p = null; /* temporary pointer */
        for (i = 1; (i <= g.nvertices); i++) {
            in[i] = 0;
        }
        for (i = 1; (i <= g.nvertices); i++) {
            p = g.edges[i];
            while ((p != null)) {
                in[p.y]++;
                p = p.next;
            }
        }
    }

    public static void topsort(Graph.graph g, int[] sorted) {
        int[] indegree = new int[(MAXV + 1)]; /* indegree of each vertex */
        Queue.queue zeroin = new Queue.queue(); /* vertices of indegree 0 */
        int x = 0; /* current and next vertex */
        int y = 0;
        int i = 0; /* counters */
        int j = 0;
        Graph.edgenode p = null; /* temporary pointer */
        compute_indegrees(g, indegree);
        Queue.init_queue(zeroin);
        for (i = 1; (i <= g.nvertices); i++) {
            if ((indegree[i] == 0)) {
                Queue.enqueue(zeroin, i);
            }
        }
        j = 0;
        while (Queue.empty_queue(zeroin) == 0) {
            j = (j + 1);
            x = Queue.dequeue(zeroin);
            sorted[j] = x;
            p = g.edges[x];
            while ((p != null)) {
                y = p.y;
                indegree[y]--;
                if ((indegree[y] == 0)) {
                    Queue.enqueue(zeroin, y);
                }
                p = p.next;
            }
        }
        if ((j != g.nvertices)) {
            System.out.printf(Locale.US, "Not a DAG -- only %d vertices found\n", j);
        }
    }

    public static int main() {
        Graph.graph g = new Graph.graph();
        int[] out = new int[(MAXV + 1)];
        int i = 0;
        Graph.read_graph(g, true);
        Graph.print_graph(g);
        topsort(g, out);
        for (i = 1; (i <= g.nvertices); i++) {
            System.out.printf(Locale.US, " %d", out[i]);
        }
        System.out.print("\n");
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
