/* 	random.c

	Compute random numbers within given ranges
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

public class Random {
    /*      These functions generate random numbers in the designated ranges */
    public static void swap(int[] a, int i, int[] b, int j) {
        int t = a[i];
        a[i] = b[j];
        b[j] = t;
    }
    /*      Construct a random permutation of the $n$ elements of the
            given array.
    */
    public static void random_permutation(int[] a, int offset, int n) {
        for (int i = n; i > 1; i--) swap(a, offset + i - 1, a, offset + random_int(0, i - 1));
    }


    public static void swap(int[] a, int[] b) {
        int x = 0;
        x = a[0];
        a[0] = b[0];
        b[0] = x;
    }

    public static int random_int(int low, int high) { /* lower/upper bounds on numb*/
        int i = 0; /* random number*/
        int j = 0;
        int r = 0;
        i = (Integer.MAX_VALUE / ((high - low) + 1));
        i *= ((high - low) + 1);
        while (((j = C.rand()) >= i)) {
            continue;
        }
        r = ((j % ((high - low) + 1)) + low);
        if (((r < low) || (r > high))) {
            C.printf("Error: random integer %d out of range [%d,%d]\n", r, low, high);
        }
        return r;
    }

    public static void random_permutation(int[] a, int n) {
        int i = 0;
        for (i = n; (i > 1); i--) {
            Random.swap(a, (i - 1), a, random_int(0, (i - 1)));
        }
    }

    public static double random_float(int low, int high) { /*lower/upper bounds on numb*/
        double i = 0; /* avoid arithmetic trouble */
        double j = 0;
        double r = 0; /* random number*/
        i = (Integer.MAX_VALUE / (high - low));
        i *= (high - low);
        while (((j = C.rand()) >= i)) {
            continue;
        }
        r = (((j / i) * (high - low)) + low);
        if (((r < low) || (r > high))) {
            C.printf("ERROR: random real %f out of range [%d,%d]\n", r, low, high);
        }
        return r;
    }

}
