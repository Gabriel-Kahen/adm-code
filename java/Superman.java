/*    superman.c

    Compute Superman's flight path -- geometry example
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

public class Superman {
    public static final int MAXN = 100; /* maximum number of circles */
    public static final double PI = 3.1415926; /* ratio of circumference to diameter */
    public static final double EPSILON = 0.000001; /* a quantity small enough to be zero */
    public static final int DIMENSION = 2; /* dimension of points */
    public static final int X = 0; /* x-coordinate index */
    public static final int Y = 1; /* y-coordinate index */
    public static final int MAXPOLY = 200; /* maximum number of points in a polygon */
    public static double[] s = new double[DIMENSION]; /* Superman's initial position */
    public static double[] t = new double[DIMENSION]; /* target position */
    public static int ncircles = 0; /* number of circles */
    public static Geometry.circle[] c = new Geometry.circle[(MAXN + 1)]; /* circles data structure */
    static {
        for (int _i0 = 0; _i0 < (MAXN + 1); _i0++) {
            c[_i0] = new Geometry.circle();
        }
    }

    public static void superman() {
        Geometry.line l = new Geometry.line(); /* line from start to target position */
        double[] close = new double[DIMENSION];
        double d = 0; /* distance from circle-center */
        double xray = 0.0; /* length of intersection with circles */
        double around = 0.0; /* length around circular arcs */
        double angle = 0; /* angle subtended by arc */
        double travel = 0; /* total travel distance */
        int i = 0; /* counter */
        Geometry.points_to_line(s, t, l);
        for (i = 1; (i <= ncircles); i++) {
            Geometry.closest_point(c[i].c, l, close);
            d = Geometry.distance(c[i].c, close);
            if ((((d >= 0) && (d < c[i].r)) && Geometry.point_in_box(close, s, t))) {
                xray += (2 * Math.sqrt(((c[i].r * c[i].r) - (d * d))));
                angle = Math.acos((d / c[i].r));
                around += (((2 * angle) / (2 * PI)) * ((2 * PI) * c[i].r));
                C.printf("circle %d (%7.3lf,%7.3lf,%7.3lf) is %7.3lf away from l, xray=%7.3lf around=%7.3lf angle=%7.3lf.\n", i, c[i].c[X], c[i].c[Y], c[i].r, d, xray, around, angle);
            }
        }
        travel = ((Geometry.distance(s, t) - xray) + around);
        C.printf("Superman sees through %7.3lf units, and flies %7.3lf units\n", xray, travel);
    }

    public static int main() {
        int i = 0; /* counter */
        int _read0 = C.scan("%lf %lf");
        if (_read0 > 0) s[X] = C.scanDouble(0);
        if (_read0 > 1) s[Y] = C.scanDouble(1);
        int _read1 = C.scan("%lf %lf");
        if (_read1 > 0) t[X] = C.scanDouble(0);
        if (_read1 > 1) t[Y] = C.scanDouble(1);
        int _read2 = C.scan("%d");
        if (_read2 > 0) ncircles = C.scanInt(0);
        if (((ncircles < 0) || (ncircles > MAXN))) {
            C.fprintf("circle count exceeds capacity\n");
            return 1;
        }
        for (i = 1; (i <= ncircles); i++) {
            int _read3 = C.scan("%lf %lf %lf");
            if (_read3 > 0) c[i].c[X] = C.scanDouble(0);
            if (_read3 > 1) c[i].c[Y] = C.scanDouble(1);
            if (_read3 > 2) c[i].r = C.scanDouble(2);
        }
        C.printf("%7.3lf %7.3lf\n", s[X], s[Y]);
        C.printf("%7.3lf %7.3lf\n", t[X], t[Y]);
        C.printf("%d\n", ncircles);
        for (i = 1; (i <= ncircles); i++) {
            C.printf("%7.3lf %7.3lf %7.3lf\n", c[i].c[X], c[i].c[Y], c[i].r);
        }
        superman();
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
