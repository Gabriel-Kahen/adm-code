/*	convex-hull.c

	Compute convex hulls of points in the plane by the Gries/Graham scan.
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

public class ConvexHull {
    public static final double PI = 3.1415926; /* ratio of circumference to diameter */
    public static final double EPSILON = 0.000001; /* a quantity small enough to be zero */
    public static final int DIMENSION = 2; /* dimension of points */
    public static final int X = 0; /* x-coordinate index */
    public static final int Y = 1; /* y-coordinate index */
    public static final int MAXPOLY = 200; /* maximum number of points in a polygon */
    public static double[] first_point = new double[DIMENSION]; /* first hull point */

    public static void sort_and_remove_duplicates(double[][] in, int[] n) {
        int i = 0; /* counter */
        int input_count = 0; /* number of points before deletion */
        int unique_count = 0; /* index marked for potential deletion */
        java.util.Arrays.sort(in, 0, (0 + n[0]), ConvexHull::leftlower);
        input_count = n[0];
        /* in[0..unique_count-1] is the compacted distinct prefix. */
        unique_count = 1;
        for (i = 1; (i < input_count); i++) {
            if (((in[(unique_count - 1)][X] == in[i][X]) && (in[(unique_count - 1)][Y] == in[i][Y]))) {
                n[0]--;
            } else {
                Geometry.copy_point(in[i], in[unique_count]);
                unique_count = (unique_count + 1);
            }
        }
    }

    public static void convex_hull(double[][] in, int n_value, Geometry.polygon hull) {
        int[] n = {n_value};
        int i = 0; /* input counter */
        int top = 0; /* current hull size */
        if ((n[0] <= 0)) {
            hull.n = 0;
            return;
        }
        sort_and_remove_duplicates(in, n);
        /* A collinear hull is a segment, not a closed scan with a sentinel. */
        for (i = 1; ((i + 1) < n[0]); i++) {
            if (!(Geometry.collinear(in[0], in[(n[0] - 1)], in[i]))) {
                break;
            }
        }
        if (((n[0] <= 2) || ((i + 1) == n[0]))) {
            Geometry.copy_point(in[0], hull.p[0]);
            hull.n = 1;
            if ((n[0] > 1)) {
                Geometry.copy_point(in[(n[0] - 1)], hull.p[1]);
                hull.n = 2;
            }
            return;
        }
        Geometry.copy_point(in[0], first_point);
        java.util.Arrays.sort(in, 1, (1 + (n[0] - 1)), ConvexHull::smaller_angle);
        Geometry.copy_point(first_point, hull.p[0]);
        Geometry.copy_point(in[1], hull.p[1]);
        top = 1;
        i = 2;
        while ((i < n[0])) {
            if (Geometry.cw(hull.p[(top - 1)], hull.p[top], in[i])) {
                top = (top - 1); /* top not on hull */
            } else {
                if (!(Geometry.collinear(hull.p[(top - 1)], hull.p[top], in[i]))) {
                    top = (top + 1);
                }
                Geometry.copy_point(in[i], hull.p[top]);
                i = (i + 1);
            }
        }
        hull.n = (top + 1);
    }

    public static int leftlower(Object left, Object right) {
        double[] p1 = (double[])left;
        double[] p2 = (double[])right;
        if ((p1[X] < p2[X])) {
            return (-1);
        }
        if ((p1[X] > p2[X])) {
            return 1;
        }
        if ((p1[Y] < p2[Y])) {
            return (-1);
        }
        if ((p1[Y] > p2[Y])) {
            return 1;
        }
        return 0;
    }

    public static int smaller_angle(Object left, Object right) {
        /* The legacy geometry predicates accept mutable pointers but only read them. */
        double[] p1 = ((double[])left);
        double[] p2 = ((double[])right);
        if (Geometry.collinear(first_point, p1, p2)) {
            if ((Geometry.distance(first_point, p1) <= Geometry.distance(first_point, p2))) {
                return (-1);
            } else {
                return 1;
            }
        }
        if (Geometry.ccw(first_point, p1, p2)) {
            return (-1);
        } else {
            return 1;
        }
    }

    public static int main() {
        double[][] in = new double[MAXPOLY][DIMENSION]; /* input points */
        Geometry.polygon hull = new Geometry.polygon(); /* convex hull */
        int n = 0; /* number of points */
        int i = 0; /* counter */
        int _read0 = C.scan("%d");
        if (_read0 > 0) n = C.scanInt(0);
        for (i = 0; (i < n); i++) {
            int _read1 = C.scan("%lf %lf");
            if (_read1 > 0) in[i][X] = C.scanDouble(0);
            if (_read1 > 1) in[i][Y] = C.scanDouble(1);
        }
        convex_hull(in, n, hull);
        Geometry.print_polygon(hull);
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
