/*	matrix.c

	Multiply two matrices.
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

public class Matrix {
    public static final int MAXV = 100; /* maximum number of vertices */
    public static final int MAXDEGREE = 50; /* maximum outdegree of a vertex */
    public static final int MAXINT = 100007;
    public static class matrix {
        int[][] m = new int[(MAXV + 1)][(MAXV + 1)]; /* adjacency/weight info */
        int rows = 0; /* number of rows */
        int columns = 0; /* number of columns */
    }

    public static void initialize_matrix(Matrix.matrix m) {
        int i = 0; /* counters */
        int j = 0;
        for (i = 1; (i <= m.rows); i++) {
            for (j = 1; (j <= m.columns); j++) {
                m.m[i][j] = 0;
            }
        }
    }

    public static void read_matrix(Matrix.matrix m) {
        int i = 0; /* counters */
        int j = 0;
        int _read0 = C.scan("%d %d\n");
        if (_read0 > 0) m.rows = C.scanInt(0);
        if (_read0 > 1) m.columns = C.scanInt(1);
        for (i = 1; (i <= m.rows); i++) {
            for (j = 1; (j <= m.columns); j++) {
                int _read1 = C.scan("%d");
                if (_read1 > 0) m.m[i][j] = C.scanInt(0);
            }
        }
    }

    public static void print_matrix(Matrix.matrix g) {
        int i = 0; /* counters */
        int j = 0;
        for (i = 1; (i <= g.rows); i++) {
            for (j = 1; (j <= g.columns); j++) {
                C.printf(" %d", g.m[i][j]);
            }
            C.printf("\n");
        }
        C.printf("\n");
    }

    public static void multiply(Matrix.matrix a, Matrix.matrix b, Matrix.matrix c) {
        int i = 0; /* dimension counters */
        int j = 0;
        int k = 0;
        if ((a.columns != b.rows)) {
            C.printf("Error: bounds dont match!\n");
            return;
        }
        c.rows = a.rows;
        c.columns = b.columns;
        for (i = 1; (i <= a.rows); i++) {
            for (j = 1; (j <= b.columns); j++) {
                c.m[i][j] = 0;
                for (k = 1; (k <= b.rows); k++) {
                    c.m[i][j] += (a.m[i][k] * b.m[k][j]);
                }
            }
        }
    }

    public static int main() {
        Matrix.matrix a = new Matrix.matrix();
        Matrix.matrix b = new Matrix.matrix();
        Matrix.matrix c = new Matrix.matrix();
        read_matrix(a);
        print_matrix(a);
        read_matrix(b);
        print_matrix(b);
        multiply(a, b, c);
        print_matrix(c);
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
