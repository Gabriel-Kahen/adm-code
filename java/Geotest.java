/*	geotest.c

	Driver program for geometry routines
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

public class Geotest {
    public static final double PI = 3.1415926; /* ratio of circumference to diameter */
    public static final double EPSILON = 0.000001; /* a quantity small enough to be zero */
    public static final int DIMENSION = 2; /* dimension of points */
    public static final int X = 0; /* x-coordinate index */
    public static final int Y = 1; /* y-coordinate index */
    public static final int MAXPOLY = 200; /* maximum number of points in a polygon */

    public static int main() {
        double[] p1 = new double[DIMENSION];
        double[] p2 = new double[DIMENSION];
        double[] q1 = new double[DIMENSION];
        double[] q2 = new double[DIMENSION];
        double[] i = new double[DIMENSION];
        Geometry.line l1 = new Geometry.line();
        Geometry.line l2 = new Geometry.line();
        Geometry.line l3 = new Geometry.line();
        while (true) {
            int _read0 = C.scan("%lf %lf");
            if (_read0 > 0) p1[X] = C.scanDouble(0);
            if (_read0 > 1) p1[Y] = C.scanDouble(1);
            if (!((_read0 != -1))) break;
            int _read1 = C.scan("%lf %lf");
            if (_read1 > 0) p2[X] = C.scanDouble(0);
            if (_read1 > 1) p2[Y] = C.scanDouble(1);
            int _read2 = C.scan("%lf %lf");
            if (_read2 > 0) q1[X] = C.scanDouble(0);
            if (_read2 > 1) q1[Y] = C.scanDouble(1);
            int _read3 = C.scan("%lf %lf");
            if (_read3 > 0) q2[X] = C.scanDouble(0);
            if (_read3 > 1) q2[Y] = C.scanDouble(1);
            Geometry.print_point(p1);
            Geometry.print_point(p2);
            Geometry.print_point(q1);
            Geometry.print_point(q2);
            Geometry.points_to_line(p1, p2, l1);
            Geometry.points_to_line(q1, q2, l2);
            Geometry.print_line(l1);
            Geometry.print_line(l2);
            System.out.print("slope and line tests\n");
            Geometry.point_and_slope_to_line(p1, (-l1.a), l3);
            Geometry.print_line(l3);
            Geometry.point_and_slope_to_line(p2, (-l1.a), l3);
            Geometry.print_line(l3);
            Geometry.point_and_slope_to_line(q1, (-l2.a), l3);
            Geometry.print_line(l3);
            Geometry.point_and_slope_to_line(q2, (-l2.a), l3);
            Geometry.print_line(l3);
            System.out.print("parallel lines test\n");
            C.printf("%d\n", Geometry.parallelQ(l1, l2));
            System.out.print("intersection point\n");
            Geometry.intersection_point(l1, l2, i);
            Geometry.print_point(i);
            System.out.print("closest point\n");
            Geometry.closest_point(p1, l1, i);
            Geometry.print_point(i);
            Geometry.closest_point(p2, l1, i);
            Geometry.print_point(i);
            Geometry.closest_point(q1, l1, i);
            Geometry.print_point(i);
            Geometry.closest_point(q2, l1, i);
            Geometry.print_point(i);
            Geometry.closest_point(p1, l2, i);
            Geometry.print_point(i);
            Geometry.closest_point(p2, l2, i);
            Geometry.print_point(i);
            Geometry.closest_point(q1, l2, i);
            Geometry.print_point(i);
            Geometry.closest_point(q2, l2, i);
            Geometry.print_point(i);
            System.out.print("--------------------------------\n");
        }
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
