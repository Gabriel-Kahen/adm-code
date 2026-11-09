/*	geometry.c

	Basic geometric primitives and data types -- Lines, Circles, Segments
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

import java.util.Locale;

public class Geometry {
    public static final double PI = 3.1415926; /* ratio of circumference to diameter */
    public static final double EPSILON = 0.000001; /* a quantity small enough to be zero */
    public static final int DIMENSION = 2; /* dimension of points */
    public static final int X = 0; /* x-coordinate index */
    public static final int Y = 1; /* y-coordinate index */
    public static final int MAXPOLY = 200; /* maximum number of points in a polygon */
    public static class line {
        double a = 0; /* x-coefficient */
        double b = 0; /* y-coefficient */
        double c = 0; /* constant term */
    }
    public static class polygon {
        int n = 0; /* number of points in polygon */
        double[][] p = new double[MAXPOLY][DIMENSION]; /* array of points in polygon */
    }
    public static class segment {
        double[] p1 = new double[DIMENSION]; /* endpoints of line segment */
        double[] p2 = new double[DIMENSION]; /* endpoints of line segment */
    }
    public static class triangulation {
        int n = 0; /* number of triangles in triangulation */
        int[][] t = new int[MAXPOLY][3]; /* indicies of vertices in triangulation */
    }
    public static class circle {
        double[] c = new double[DIMENSION]; /* center of circle */
        double r = 0; /* radius of circle */
    }

    public static void points_to_line(double[] p1, double[] p2, Geometry.line l) {
        if ((p1[X] == p2[X])) {
            l.a = 1;
            l.b = 0;
            l.c = (-p1[X]);
        } else {
            l.b = 1;
            l.a = ((-(p1[Y] - p2[Y])) / (p1[X] - p2[X]));
            l.c = ((-(l.a * p1[X])) - (l.b * p1[Y]));
        }
    }

    public static void point_and_slope_to_line(double[] p, double m, Geometry.line l) {
        l.a = (-m);
        l.b = 1;
        l.c = (-((l.a * p[X]) + (l.b * p[Y])));
    }

    public static boolean parallelQ(Geometry.line l1, Geometry.line l2) {
        return ((Math.abs((l1.a - l2.a)) <= EPSILON) && (Math.abs((l1.b - l2.b)) <= EPSILON));
    }

    public static boolean same_lineQ(Geometry.line l1, Geometry.line l2) {
        return (parallelQ(l1, l2) && (Math.abs((l1.c - l2.c)) <= EPSILON));
    }

    public static void intersection_point(Geometry.line l1, Geometry.line l2, double[] p) {
        if (same_lineQ(l1, l2)) {
            System.out.print("Warning: Identical lines, all points intersect.\n");
            p[X] = (p[Y] = 0.0);
            return;
        }
        if (parallelQ(l1, l2)) {
            System.out.print("Error: Distinct parallel lines do not intersect.\n");
            return;
        }
        p[X] = (((l2.b * l1.c) - (l1.b * l2.c)) / ((l2.a * l1.b) - (l1.a * l2.b)));
        if ((Math.abs(l1.b) > EPSILON)) { /* test for vertical line */
            p[Y] = ((-((l1.a * p[X]) + l1.c)) / l1.b);
        } else {
            p[Y] = ((-((l2.a * p[X]) + l2.c)) / l2.b);
        }
    }

    public static void closest_point(double[] p_in, Geometry.line l, double[] p_c) {
        Geometry.line perp = new Geometry.line(); /* perpendicular to l through (x,y) */
        if ((Math.abs(l.b) <= EPSILON)) { /* vertical line */
            p_c[X] = (-l.c);
            p_c[Y] = p_in[Y];
            return;
        }
        if ((Math.abs(l.a) <= EPSILON)) { /* horizontal line */
            p_c[X] = p_in[X];
            p_c[Y] = (-l.c);
            return;
        }
        point_and_slope_to_line(p_in, (1 / l.a), perp);
        intersection_point(l, perp, p_c);
    }

    public static double distance(double[] a, double[] b) {
        int i = 0; /* counter */
        double d = 0.0; /* accumulated distance */
        for (i = 0; (i < DIMENSION); i++) {
            d = (d + ((a[i] - b[i]) * (a[i] - b[i])));
        }
        return Math.sqrt(d);
    }

    public static void copy_point(double[] a, double[] b) {
        int i = 0; /* counter */
        for (i = 0; (i < DIMENSION); i++) {
            b[i] = a[i];
        }
    }

    public static void swap_point(double[] a, double[] b) {
        double[] c = new double[DIMENSION];
        copy_point(a, c);
        copy_point(b, a);
        copy_point(c, b);
    }

    public static void points_to_segment(double[] a, double[] b, Geometry.segment s) {
        copy_point(a, s.p1);
        copy_point(b, s.p2);
    }

    public static void segment_to_points(Geometry.segment s, double[] p1, double[] p2) {
        copy_point(s.p1, p1);
        copy_point(s.p2, p2);
    }

    public static boolean point_in_box(double[] p, double[] b1, double[] b2) {
        return ((((p[X] >= Math.min(b1[X], b2[X])) && (p[X] <= Math.max(b1[X], b2[X]))) && (p[Y] >= Math.min(b1[Y], b2[Y]))) && (p[Y] <= Math.max(b1[Y], b2[Y])));
    }

    public static boolean segments_intersect(Geometry.segment s1, Geometry.segment s2) {
        double signed_triangle_area = 0;
        /* Test the input endpoints directly; a rounded line intersection can
               fall just outside a segment that contains its shared endpoint. */
        double a = signed_triangle_area(s1.p1, s1.p2, s2.p1);
        double b = signed_triangle_area(s1.p1, s1.p2, s2.p2);
        double c = signed_triangle_area(s2.p1, s2.p2, s1.p1);
        double d = signed_triangle_area(s2.p1, s2.p2, s1.p2);
        if ((((((Math.abs(a) <= EPSILON) && point_in_box(s2.p1, s1.p1, s1.p2)) || ((Math.abs(b) <= EPSILON) && point_in_box(s2.p2, s1.p1, s1.p2))) || ((Math.abs(c) <= EPSILON) && point_in_box(s1.p1, s2.p1, s2.p2))) || ((Math.abs(d) <= EPSILON) && point_in_box(s1.p2, s2.p1, s2.p2)))) {
            return (1 != 0);
        }
        return ((((a > EPSILON) && (b < (-EPSILON))) || ((a < (-EPSILON)) && (b > EPSILON))) && (((c > EPSILON) && (d < (-EPSILON))) || ((c < (-EPSILON)) && (d > EPSILON))));
    }

    public static double signed_triangle_area(double[] a, double[] b, double[] c) {
        return (((((((a[X] * b[Y]) - (a[Y] * b[X])) + (a[Y] * c[X])) - (a[X] * c[Y])) + (b[X] * c[Y])) - (c[X] * b[Y])) / 2.0);
    }

    public static double triangle_area(double[] a, double[] b, double[] c) {
        return Math.abs(signed_triangle_area(a, b, c));
    }

    public static boolean ccw(double[] a, double[] b, double[] c) {
        return (signed_triangle_area(a, b, c) > EPSILON);
    }

    public static boolean cw(double[] a, double[] b, double[] c) {
        return (signed_triangle_area(a, b, c) < (-EPSILON));
    }

    public static boolean collinear(double[] a, double[] b, double[] c) {
        return (Math.abs(signed_triangle_area(a, b, c)) <= EPSILON);
    }

    public static void print_points(double[][] p, int n) {
        int i = 0; /* counter */
        for (i = 0; (i < n); i++) {
            System.out.printf(Locale.US, "(%f,%f)\n", p[i][X], p[i][Y]);
        }
    }

    public static void print_polygon(Geometry.polygon p) {
        int i = 0; /* counter */
        for (i = 0; (i < p.n); i++) {
            System.out.printf(Locale.US, "(%f,%f)\n", p.p[i][X], p.p[i][Y]);
        }
    }

    public static void print_point(double[] p) {
        System.out.printf(Locale.US, "%7.3f %7.3f\n", p[X], p[Y]);
    }

    public static void print_line(Geometry.line l) {
        System.out.printf(Locale.US, "(a=%7.3f,b=%7.3f,c=%7.3f)\n", l.a, l.b, l.c);
    }

    public static void print_segment(Geometry.segment s) {
        System.out.print("segment: ");
        print_point(s.p1);
        print_point(s.p2);
    }

}
