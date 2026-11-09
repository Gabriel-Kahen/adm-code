/*	8-queens.c
	Solve the eight queens problem using backtracking
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

public class EightQueens {
    public static final int MAXCANDIDATES = 100; /* max possible next extensions */
    public static final int NMAX = 100; /* maximum solution size */
    public static boolean finished = false;
    public static int solution_count = 0; /* how many solutions are there? */

    public static void process_solution(int[] a, int k, int input) {
        solution_count++;
    }

    public static int is_a_solution(int[] a, int k, int n) {
        return ((k == n) ? 1 : 0);
    }

    public static void make_move(int[] a, int k, int n) {
    }

    public static void unmake_move(int[] a, int k, int n) {
    }

    /*  What are possible elements of the next slot in the 8-queens
        problem?
    */
    public static void construct_candidates(int[] a, int k, int n, int[] c, int[] ncandidates) {
        int i = 0; /* counters */
        int j = 0;
        boolean legal_move = false;
        ncandidates[0] = 0;
        for (i = 1; (i <= n); i++) {
            legal_move = true;
            for (j = 1; (j < k); j++) {
                if ((Math.abs((k - j)) == Math.abs((i - a[j])))) { /* diagonal threat */
                    legal_move = false;
                }
                if ((i == a[j])) { /* column threat */
                    legal_move = false;
                }
            }
            if (legal_move) { /* might the move be legal? */
                c[ncandidates[0]] = i;
                ncandidates[0] = (ncandidates[0] + 1);
            }
        }
    }

    public static void backtrack(int[] a, int k, int input) {
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
        for (i = 1; (i <= 10); i++) {
            solution_count = 0;
            backtrack(a, 0, i);
            C.printf("n=%d  solution_count=%d\n", i, solution_count);
        }
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
