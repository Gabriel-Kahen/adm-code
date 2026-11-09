/*	backtrack.c
	A generic backtracking implementation
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

public class Backtrack {
    public interface Callbacks {
        int is_a_solution(int[] a, int k, char[] input);
        void process_solution(int[] a, int k, char[] input);
        void construct_candidates(int[] a, int k, char[] input, int[] c, int[] nc);
        void make_move(int[] a, int k, char[] input);
        void unmake_move(int[] a, int k, char[] input);
    }
    public static Callbacks callbacks;

    public static final int MAXCANDIDATES = 100; /* maximum extensions of one prefix */
    public static final int NMAX = 100; /* maximum solution length */
    public static int finished = 0; /* found all solutions yet? */

    public static void backtrack(int[] a, int k, char[] input) {
        int[] c = new int[MAXCANDIDATES]; /* candidates for next position */
        int[] nc = new int[]{0}; /* next position candidate count */
        int i = 0; /* counter */
        if ((callbacks.is_a_solution(a, k, input) != 0)) {
            callbacks.process_solution(a, k, input);
        } else {
            k = (k + 1);
            callbacks.construct_candidates(a, k, input, c, nc);
            for (i = 0; (i < nc[0]); i++) {
                a[k] = c[i];
                callbacks.make_move(a, k, input);
                backtrack(a, k, input);
                callbacks.unmake_move(a, k, input);
                if ((finished != 0)) {
                    return; /* terminate early */
                }
            }
        }
    }

}
