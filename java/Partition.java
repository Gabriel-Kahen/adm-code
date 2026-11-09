/*  partition.c

    Optimally balance partitions using dynamic programming
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

public class Partition {
    public static final int MAXN = 45; /* largest number of books */
    public static final int MAXK = 10; /* largest number of dividers */

    /* largest number of dividers */
    public static long max(long a, long b) {
        return ((a > b) ? a : b);
    }

    public static void read_partition(int[] s, int[] n, int[] k) {
        int i = 0; /* counter */
        int _read0 = C.scan("%d %d\n");
        if (_read0 > 0) n[0] = C.scanInt(0);
        if (_read0 > 1) k[0] = C.scanInt(1);
        for (i = 1; (i <= n[0]); i++) {
            int _read1 = C.scan("%d\n");
            if (_read1 > 0) s[i] = C.scanInt(0);
        }
    }

    public static void print_books(int[] s, int start, int end) {
        int i = 0; /* counter */
        C.printf("{");
        for (i = start; (i <= end); i++) {
            C.printf(" %d ", s[i]);
        }
        C.printf("}\n");
    }

    public static void print_matrix(long[][] m, int n, int k) {
        int i = 0; /* counters */
        int j = 0;
        C.printf("\n");
        for (i = 1; (i <= n); i++) {
            for (j = 1; (j <= k); j++) {
                C.printf(" %lld ", m[i][j]);
            }
            C.printf("\n");
        }
    }

    public static void reconstruct_partition(int[] s, int[][] d, int n, int k) {
        if ((k == 1)) {
            print_books(s, 1, n);
        } else {
            reconstruct_partition(s, d, d[n][k], (k - 1));
            print_books(s, (d[n][k] + 1), n);
        }
    }

    public static void partition(int[] s, int n, int k) {
        long[] prefix_sum = new long[(MAXN + 1)];
        long[][] best_cost = new long[(MAXN + 1)][(MAXK + 1)];
        int[][] divider = new int[(MAXN + 1)][(MAXK + 1)];
        long split_cost = 0;
        int i = 0;
        int j = 0;
        int x = 0;
        if ((((((n < 1) || (n > MAXN)) || (k < 1)) || (k > MAXK)) || (k > n))) {
            C.fprintf("invalid partition dimensions\n");
            return;
        }
        prefix_sum[0] = 0; /* construct prefix sums */
        for (i = 1; (i <= n); i++) {
            prefix_sum[i] = (prefix_sum[(i - 1)] + s[i]);
        }
        for (i = 1; (i <= n); i++) {
            best_cost[i][1] = prefix_sum[i]; /* initialize boundaries */
        }
        /* best_cost[i][j] balances the first i books into j nonempty groups.
               A split after x leaves j - 1 nonempty groups on its left. */
        for (i = 2; (i <= n); i++) {
            for (j = 2; ((j <= k) && (j <= i)); j++) {
                for (x = (j - 1); (x <= (i - 1)); x++) {
                    split_cost = max(best_cost[x][(j - 1)], (prefix_sum[i] - prefix_sum[x]));
                    /* The first feasible split initializes the cell without an infinity sentinel. */
                    if (((x == (j - 1)) || (best_cost[i][j] > split_cost))) {
                        best_cost[i][j] = split_cost;
                        divider[i][j] = x;
                    }
                }
            }
        }
        reconstruct_partition(s, divider, n, k); /* print book partition */
    }

    public static int main() {
        int[] s = new int[(MAXN + 1)]; /* book thicknesses to partition */
        int[] n = new int[]{0}; /* how many books? */
        int[] k = new int[]{0}; /* how many partitions? */
        read_partition(s, n, k);
        partition(s, n[0], k[0]);
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
