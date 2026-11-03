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

public final class EightQueens {
    /** Number of nonattacking queen placements, O(n!) search and O(n) auxiliary storage. */
    public static long queens(int n) {
        if (n < 0 || n > 15) {
            throw new IllegalArgumentException("queen size outside 0..15");
        }
        return queensVisit(0, n, new boolean[n], new boolean[2 * n + 1], new boolean[2 * n + 1]);
    }

    static long queensVisit(int row, int n, boolean[] columns, boolean[] rising,
                            boolean[] falling) {
        if (row == n) {
            return 1;
        }
        long count = 0;
        for (int column = 0; column < n; column++) {
            int up = row + column;
            int down = row - column + n;
            if (columns[column] || rising[up] || falling[down]) {
                continue;
            }
            columns[column] = rising[up] = falling[down] = true;
            count += queensVisit(row + 1, n, columns, rising, falling);
            columns[column] = rising[up] = falling[down] = false;
        }
        return count;
    }

    public static void main(String[] args) {
        java.util.Scanner in = new java.util.Scanner(System.in);
        System.out.println(queens(in.hasNextInt() ? in.nextInt() : 8));
    }
}
