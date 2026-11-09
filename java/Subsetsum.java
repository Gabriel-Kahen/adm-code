/*	subsetsum.c

	Solve the subset sum problem by dynamic programming

	Note: the first dimension of the table will denote the rank of the integer
	being considered, with the second dimension denoting the realizable sums.
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

public class Subsetsum {
    public static final int MAXN = 100; /* largest n */
    public static final int MAXSUM = 10000; /* largest sum we will consider */
    public static final int NIL = -1;
    public static boolean[][] sum = new boolean[(MAXN + 1)][(MAXSUM + 1)]; /* table of realizable sums */
    public static int[][] parent = new int[(MAXN + 1)][(MAXSUM + 1)]; /* table of parent pointers */

    public static boolean subset_sum(int[] s, int n, int k) {
        int i = 0; /* counters */
        int j = 0;
        sum[0][0] = true;
        parent[0][0] = NIL;
        for (i = 1; (i <= k); i++) {
            sum[0][i] = false;
            parent[0][i] = NIL;
        }
        for (i = 1; (i <= n); i++) { /* build table */
            for (j = 0; (j <= k); j++) {
                sum[i][j] = sum[(i - 1)][j];
                parent[i][j] = NIL;
                if (((j >= s[(i - 1)]) && (sum[(i - 1)][(j - s[(i - 1)])] == true))) {
                    sum[i][j] = true;
                    parent[i][j] = (j - s[(i - 1)]);
                }
            }
        }
        return sum[n][k];
    }

    public static void report_subset(int n, int k) {
        if ((k == 0)) {
            return;
        }
        if ((parent[n][k] == NIL)) {
            report_subset((n - 1), k);
        } else {
            report_subset((n - 1), parent[n][k]);
            C.printf(" %d ", (k - parent[n][k]));
        }
    }

    public static int main() {
        int r = 0;
        int n = 0;
        int k = 0;
        int i = 0;
        int[] s = new int[(MAXN + 1)];
        int m = 0;
        int j = 0;
        int _read0 = C.scan("%d");
        if (_read0 > 0) m = C.scanInt(0);
        for (j = 0; (j < m); j++) {
            int _read1 = C.scan("%d %d");
            if (_read1 > 0) n = C.scanInt(0);
            if (_read1 > 1) k = C.scanInt(1);
            C.printf("n=%d  k=%d \n", n, k);
            for (i = 0; (i < n); i++) {
                int _read2 = C.scan("%d");
                if (_read2 > 0) s[i] = C.scanInt(0);
                C.printf(" %d ", s[i]);
            }
            C.printf("\n Is %d realizable: %d\n", k, (r = (subset_sum(s, n, k) ? 1 : 0)));
            if ((r != 0)) {
                report_subset(n, k);
            }
            C.printf("\n\n");
        }
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
