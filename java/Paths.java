/*    paths.c

      Enumerate the paths in a graph via backtracking
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

public class Paths {
    public static final int TREE = 0; /* tree edge */
    public static final int BACK = 1; /* back edge */
    public static final int CROSS = 2; /* cross edge */
    public static final int FORWARD = 3; /* forward edge */
    public static final int MAXV = 100; /* maximum number of vertices */
    public static final int MAXCANDIDATES = 100; /* max possible next extensions */
    public static final int NMAX = 100; /* maximum solution size */
    public static class paths_data {
        int s = 0; /* source vertex */
        int t = 0; /* destination vertex */
        Graph.graph g = new Graph.graph(); /* graph to find paths in */
    }
    public static boolean finished = false;
    public static int solution_count = 0; /* how many solutions are there? */

    public static void process_solution(int[] a, int k, Paths.paths_data input) {
        int i = 0; /* counter */
        solution_count++;
        C.printf("{");
        for (i = 1; (i <= k); i++) {
            C.printf(" %d", a[i]);
        }
        C.printf(" }\n");
    }

    public static int is_a_solution(int[] a, int k, Paths.paths_data g) {
        return (((k > 0) && (a[k] == g.t)) ? 1 : 0);
    }

    public static void make_move(int[] a, int k, Paths.paths_data input) {
    }

    public static void unmake_move(int[] a, int k, Paths.paths_data input) {
    }

    /*
        What are possible elements of the next slot in the path
    */
    public static void construct_candidates(int[] a, int k, Paths.paths_data g, int[] c, int[] nc) {
        int i = 0; /* counters */
        boolean[] in_sol = new boolean[(NMAX + 1)]; /* what's already in the solution? */
        Graph.edgenode p = null; /* temporary pointer */
        int last = 0; /* last vertex on current path */
        for (i = 1; (i <= g.g.nvertices); i++) {
            in_sol[i] = false;
        }
        for (i = 1; (i < k); i++) {
            in_sol[a[i]] = true;
        }
        if ((k == 1)) {
            c[0] = g.s; /* always start from vertex s */
            nc[0] = 1;
        } else {
            nc[0] = 0;
            last = a[(k - 1)];
            p = g.g.edges[last];
            while ((p != null)) {
                if (!(in_sol[p.y])) {
                    c[nc[0]] = p.y;
                    nc[0] = (nc[0] + 1);
                }
                p = p.next;
            }
        }
    }

    public static void backtrack(int[] a, int k, Paths.paths_data input) {
        int[] c = new int[MAXCANDIDATES]; /* candidates for next position */
        int[] ncandidates = new int[]{0}; /* next position candidate count */
        int i = 0; /* counter */
        if ((is_a_solution(a, k, input) != 0)) {
            process_solution(a, k, input);
        } else {
            k = (k + 1);
            construct_candidates(a, k, input, c, ncandidates);
            for (i = 0; (i < ncandidates[0]); i++) {
                a[k] = c[i];
                make_move(a, k, input);
                backtrack(a, k, input);
                unmake_move(a, k, input);
                if (finished) {
                    return; /* terminate early */
                }
            }
        }
    }

    public static int main() {
        int[] a = new int[(NMAX + 1)]; /* solution vector */
        int i = 0; /* counter */
        Paths.paths_data g = null;
        g = new Paths.paths_data();
        Graph.read_graph(g.g, false);
        Graph.print_graph(g.g);
        for (i = 1; (i <= g.g.nvertices); i++) {
            g.s = 1;
            g.t = i;
            C.printf("\nPaths from 1 to %d:\n", i);
            backtrack(a, 0, g);
        }
        for (i = 1; (i <= g.g.nvertices); i++) {
            g.s = i;
            g.t = 1;
            C.printf("\nPaths from %d to 1:\n", i);
            backtrack(a, 0, g);
        }
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
