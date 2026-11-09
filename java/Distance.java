/*	distance.c

	Compute Euclidian distances
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

public class Distance {
    public static final int DIMENSION = 3;

    public static double distance(int[] a, int[] b) {
        int i = 0;
        double d = 0.0;
        double delta = 0;
        for (i = 0; (i < DIMENSION); i++) {
            delta = (((double)a[i]) - ((double)b[i]));
            d += (delta * delta);
        }
        return Math.sqrt(d);
    }

    public static int main() {
        int[] a = new int[]{6, 2, 3};
        int[] b = new int[]{6, 3, 4};
        C.printf("distance = %f\n", distance(a, b));
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
