/*    order.c

      Demonstrate traversal orders on a grid.
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

public class Order {
    public static final double PI = 3.1415926; /* ratio of circumference to diameter */
    public static final double EPSILON = 0.000001; /* a quantity small enough to be zero */
    public static final int DIMENSION = 2; /* dimension of points */
    public static final int X = 0; /* x-coordinate index */
    public static final int Y = 1; /* y-coordinate index */
    public static final int MAXPOLY = 200; /* maximum number of points in a polygon */

    public static void process(int i, int j) {
        C.printf("(%d,%d)\n", i, j);
    }

    public static void row_major(int n, int m) {
        int i = 0;
        int j = 0;
        for (i = 1; (i <= n); i++) {
            for (j = 1; (j <= m); j++) {
                process(i, j); /* counters */
            }
        }
    }

    public static void column_major(int n, int m) {
        int i = 0;
        int j = 0;
        for (j = 1; (j <= m); j++) {
            for (i = 1; (i <= n); i++) {
                process(i, j); /* counters */
            }
        }
    }

    public static void snake_order(int n, int m) {
        int i = 0; /* counters */
        int j = 0;
        for (i = 1; (i <= n); i++) {
            for (j = 1; (j <= m); j++) {
                process(i, (j + (((m + 1) - (2 * j)) * ((i + 1) % 2))));
            }
        }
    }

    public static void diagonal_order(int n, int m) {
        int d = 0;
        int row = 0;
        int first = 0;
        int last = 0;
        for (d = 1; (d <= ((n + m) - 1)); d++) {
            first = Math.max(1, ((d + 1) - m));
            last = Math.min(n, d);
            for (row = first; (row <= last); row++) {
                process(row, ((d + 1) - row));
            }
        }
    }

    public static int main() {
        C.printf("row_major\n");
        row_major(5, 5);
        C.printf("\ncolumn_major\n");
        column_major(3, 3);
        C.printf("\nsnake_order\n");
        snake_order(5, 5);
        C.printf("\ndiagonal_order\n");
        diagonal_order(3, 4);
        C.printf("\ndiagonal_order\n");
        diagonal_order(4, 3);
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
