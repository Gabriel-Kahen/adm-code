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

import java.util.List;

public final class Geometry {
    public static double finite(double x) {
        if (!Double.isFinite(x)) {
            throw new IllegalArgumentException("finite values required");
        }
        return x;
    }

    public static final double EPSILON = 1e-9;

    public record Point(double x, double y) {
        public Point {
            Geometry.finite(x);
            Geometry.finite(y);
            // Treat signed zeros as the same geometric coordinate.
            if (x == 0) {
                x = 0;
            }
            if (y == 0) {
                y = 0;
            }
        }
    }

    public record Circle(Point center, double radius) {
        public Circle {
            Geometry.finite(radius);
            if (radius <= 0) {
                throw new IllegalArgumentException("circle radius must be positive");
            }
        }
    }

    /** Normalized ax+by+c=0, with a consistent sign for line equality. */
    public record Line(double a, double b, double c) {
        public Line {
            Geometry.finite(a);
            Geometry.finite(b);
            Geometry.finite(c);
            double scale = Math.hypot(a, b);
            if (scale == 0 || !Double.isFinite(scale)) {
                throw new IllegalArgumentException("invalid line");
            }
            a /= scale;
            b /= scale;
            c /= scale;
            if (a < 0 || (a == 0 && b < 0)) {
                a = -a;
                b = -b;
                c = -c;
            }
            Geometry.finite(c);
        }
    }

    public static Line line(Point a, Point b) {
        if (a.equals(b)) {
            throw new IllegalArgumentException("two distinct line points required");
        }
        double xCoefficient = a.y - b.y;
        double yCoefficient = b.x - a.x;
        // Evaluate at an endpoint instead of subtracting two large cross-products.
        double constant = -(xCoefficient * a.x + yCoefficient * a.y);
        return new Line(xCoefficient, yCoefficient, constant);
    }

    public static Line pointAndSlope(Point point, double slope) {
        Geometry.finite(slope);
        return new Line(-slope, 1, slope * point.x - point.y);
    }

    public static boolean parallel(Line a, Line b) {
        return Math.abs(a.a * b.b - b.a * a.b) <= EPSILON;
    }

    public static boolean sameLine(Line a, Line b) {
        return parallel(a, b) && Math.abs(a.c - b.c) <= EPSILON;
    }

    /** Null means parallel/coincident lines have no unique intersection. */
    public static Point intersection(Line a, Line b) {
        double determinant = a.a * b.b - b.a * a.b;
        if (Math.abs(determinant) <= EPSILON) {
            return null;
        }
        return new Point((a.b * b.c - b.b * a.c) / determinant,
                         (a.c * b.a - b.c * a.a) / determinant);
    }

    public static Point projection(Point point, Line line) {
        double signedDistance = line.a * point.x + line.b * point.y + line.c;
        return new Point(point.x - signedDistance * line.a, point.y - signedDistance * line.b);
    }

    public static double distance(Point a, Point b) {
        return Geometry.finite(Math.hypot(a.x - b.x, a.y - b.y));
    }

    public static double cross(Point a, Point b, Point c) {
        return Geometry.finite((b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x));
    }

    public static double signedTriangleArea(Point a, Point b, Point c) {
        return cross(a, b, c) / 2;
    }

    public static double triangleArea(Point a, Point b, Point c) {
        return Math.abs(signedTriangleArea(a, b, c));
    }

    public static int orientation(Point a, Point b, Point c) {
        double value = cross(a, b, c);
        return value > EPSILON ? 1 : value < -EPSILON ? -1 : 0;
    }

    public static boolean pointInBox(Point p, Point a, Point b) {
        return p.x >= Math.min(a.x, b.x) - EPSILON && p.x <= Math.max(a.x, b.x) + EPSILON &&
            p.y >= Math.min(a.y, b.y) - EPSILON && p.y <= Math.max(a.y, b.y) + EPSILON;
    }

    public static boolean segmentsIntersect(Point a, Point b, Point c, Point d) {
        int abc = orientation(a, b, c);
        int abd = orientation(a, b, d);
        int cda = orientation(c, d, a);
        int cdb = orientation(c, d, b);
        if (abc * abd < 0 && cda * cdb < 0) {
            return true;
        }
        return (abc == 0 && pointInBox(c, a, b)) || (abd == 0 && pointInBox(d, a, b)) ||
            (cda == 0 && pointInBox(a, c, d)) || (cdb == 0 && pointInBox(b, c, d));
    }

    public static double signedArea(List<Point> polygon) {
        if (polygon.size() < 3) {
            return 0;
        }
        double twice = 0;
        Point origin = polygon.get(0);
        for (int i = 1; i + 1 < polygon.size(); i++) {
            twice = Geometry.finite(twice + cross(origin, polygon.get(i), polygon.get(i + 1)));
        }
        return twice / 2;
    }

    public static double area(List<Point> polygon) {
        return Math.abs(signedArea(polygon));
    }
}
