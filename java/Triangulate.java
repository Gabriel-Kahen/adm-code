/*    triangulate.c

    Triangulate a polygon via ear-clipping, and compute the area of a polygon.
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

public class Triangulate {
    public static final double PI = 3.1415926; /* ratio of circumference to diameter */
    public static final double EPSILON = 0.000001; /* a quantity small enough to be zero */
    public static final int DIMENSION = 2; /* dimension of points */
    public static final int X = 0; /* x-coordinate index */
    public static final int Y = 1; /* y-coordinate index */
    public static final int MAXPOLY = 200; /* maximum number of points in a polygon */

    public static void add_triangle(Geometry.triangulation t, int i, int j, int k, Geometry.polygon p) {
        int n = 0; /* number of triangles in t */
        n = t.n;
        t.t[n][0] = i;
        t.t[n][1] = j;
        t.t[n][2] = k;
        t.n = (n + 1);
    }

    public static boolean point_in_triangle(double[] p, double[][] t) {
        int i = 0; /* counter */
        for (i = 0; (i < 3); i++) {
            if (Geometry.cw(t[i], t[((i + 1) % 3)], p)) {
                return false;
            }
        }
        return true;
    }

    public static boolean ear_Q(int i, int j, int k, Geometry.polygon p) {
        double[][] t = new double[3][DIMENSION];
        int m = 0; /* counter */
        Geometry.copy_point(p.p[i], t[0]);
        Geometry.copy_point(p.p[j], t[1]);
        Geometry.copy_point(p.p[k], t[2]);
        if (Geometry.cw(t[0], t[1], t[2])) {
            return false;
        }
        for (m = 0; (m < p.n); m++) {
            if ((((m != i) && (m != j)) && (m != k))) {
                if (point_in_triangle(p.p[m], t)) {
                    return false;
                }
            }
        }
        return true;
    }

    public static void triangulate(Geometry.polygon p, Geometry.triangulation t) {
        int[] l = new int[MAXPOLY]; /* left/right neighbor indices */
        int[] r = new int[MAXPOLY];
        int i = 0; /* counter */
        for (i = 0; (i < p.n); i++) { /* initialization */
            l[i] = (((i - 1) + p.n) % p.n);
            r[i] = (((i + 1) + p.n) % p.n);
        }
        t.n = 0;
        i = (p.n - 1);
        while ((t.n < (p.n - 2))) {
            i = r[i];
            if (ear_Q(l[i], i, r[i], p)) {
                add_triangle(t, l[i], i, r[i], p);
                l[r[i]] = l[i];
                r[l[i]] = r[i];
            }
        }
    }

    public static double area_triangulation(Geometry.polygon p) {
        Geometry.triangulation t = new Geometry.triangulation(); /* output triangulation */
        double total = 0.0; /* total area so far */
        int i = 0; /* counter */
        triangulate(p, t);
        for (i = 0; (i < t.n); i++) {
            total += Geometry.triangle_area(p.p[t.t[i][0]], p.p[t.t[i][1]], p.p[t.t[i][2]]);
        }
        return total;
    }

    public static double area(Geometry.polygon p) {
        double total = 0.0; /* total area so far */
        int i = 0; /* counters */
        int j = 0;
        for (i = 0; (i < p.n); i++) {
            j = ((i + 1) % p.n);
            total += ((p.p[i][X] * p.p[j][Y]) - (p.p[j][X] * p.p[i][Y]));
        }
        return (total / 2.0);
    }

    public static int main() {
        Geometry.polygon p = new Geometry.polygon(); /* input polygon */
        int i = 0; /* counter */
        int _read0 = C.scan("%d");
        if (_read0 > 0) p.n = C.scanInt(0);
        for (i = 0; (i < p.n); i++) {
            int _read1 = C.scan("%lf %lf");
            if (_read1 > 0) p.p[i][X] = C.scanDouble(0);
            if (_read1 > 1) p.p[i][Y] = C.scanDouble(1);
        }
        C.printf(" area via triangulation = %f\n", area_triangulation(p));
        C.printf(" area slick = %f\n", area(p));
        return 0;
    }

    public static void print_triangulation(Geometry.triangulation t) {
        int i = 0; /* counters */
        int j = 0;
        for (i = 0; (i < t.n); i++) {
            for (j = 0; (j < 3); j++) {
                C.printf(" %d ", t.t[i][j]);
            }
            C.printf("\n");
        }
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
