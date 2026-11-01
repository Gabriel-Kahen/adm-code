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

package adm;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

/** Planar geometry with an explicit absolute predicate tolerance of 1e-9. */
public final class Geometry {
    private Geometry() {}
    public static final double EPSILON = 1e-9;
    public record Point(double x, double y) {
        public Point {
            Numeric.finite(x);
            Numeric.finite(y);
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
            Numeric.finite(radius);
            if (radius <= 0) {
                throw new IllegalArgumentException("circle radius must be positive");
            }
        }
    }
    /** Normalized ax+by+c=0, with a consistent sign for line equality. */
    public record Line(double a, double b, double c) {
        public Line {
            Numeric.finite(a);
            Numeric.finite(b);
            Numeric.finite(c);
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
            Numeric.finite(c);
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
        Numeric.finite(slope);
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
        return Numeric.finite(Math.hypot(a.x - b.x, a.y - b.y));
    }
    public static double cross(Point a, Point b, Point c) {
        return Numeric.finite((b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x));
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
            twice = Numeric.finite(twice + cross(origin, polygon.get(i), polygon.get(i + 1)));
        }
        return twice / 2;
    }
    public static double area(List<Point> polygon) {
        return Math.abs(signedArea(polygon));
    }

    /** Monotone chain, O(n log n). Duplicates and interior collinear points are removed. */
    public static List<Point> convexHull(List<Point> input) {
        List<Point> points = new ArrayList<>(input);
        points.sort(Comparator.comparingDouble(Point::x).thenComparingDouble(Point::y));
        List<Point> unique = new ArrayList<>();
        for (Point point : points) {
            if (unique.isEmpty() || !point.equals(unique.get(unique.size() - 1))) {
                unique.add(point);
            }
        }
        if (unique.size() <= 1) {
            return unique;
        }
        List<Point> lower = new ArrayList<>();
        for (Point point : unique) {
            appendHull(lower, point);
        }
        List<Point> upper = new ArrayList<>();
        for (int i = unique.size() - 1; i >= 0; i--) {
            appendHull(upper, unique.get(i));
        }
        lower.remove(lower.size() - 1);
        upper.remove(upper.size() - 1);
        lower.addAll(upper);
        return lower;
    }
    private static void appendHull(List<Point> hull, Point point) {
        while (hull.size() >= 2 &&
               cross(hull.get(hull.size() - 2), hull.get(hull.size() - 1), point) <= EPSILON) {
            hull.remove(hull.size() - 1);
        }
        hull.add(point);
    }

    private static double validatePolygon(List<Point> polygon) {
        int n = polygon.size();
        if (n < 3 || area(polygon) <= EPSILON) {
            throw new IllegalArgumentException("nondegenerate polygon required");
        }
        for (int i = 0; i < n; i++) {
            Point a = polygon.get(i);
            Point b = polygon.get((i + 1) % n);
            if (distance(a, b) <= EPSILON) {
                throw new IllegalArgumentException("duplicate adjacent vertex");
            }
            Point previous = polygon.get((i + n - 1) % n);
            if (orientation(previous, a, b) == 0) {
                double dot = (a.x - previous.x) * (b.x - a.x) + (a.y - previous.y) * (b.y - a.y);
                if (dot < 0) {
                    throw new IllegalArgumentException("overlapping boundary edges");
                }
            }
            for (int j = i + 1; j < n; j++) {
                if (j == i + 1 || (i == 0 && j == n - 1)) {
                    continue;
                }
                if (segmentsIntersect(a, b, polygon.get(j), polygon.get((j + 1) % n))) {
                    throw new IllegalArgumentException("self-intersecting polygon");
                }
            }
        }
        return Math.signum(signedArea(polygon));
    }
    private static boolean inTriangle(Point p, Point a, Point b, Point c, double direction) {
        return direction * cross(a, b, p) >= -EPSILON && direction * cross(b, c, p) >= -EPSILON &&
            direction * cross(c, a, p) >= -EPSILON;
    }

    /** Ear clipping, O(n^3) in this direct implementation. Either boundary orientation is accepted. */
    public static List<int[]> triangulate(List<Point> polygon) {
        double direction = validatePolygon(polygon);
        List<Integer> remaining = new ArrayList<>();
        for (int i = 0; i < polygon.size(); i++) {
            remaining.add(i);
        }
        List<int[]> triangles = new ArrayList<>();
        while (remaining.size() > 3) {
            boolean removed = false;
            for (int i = 0; i < remaining.size(); i++) {
                int a = remaining.get((i + remaining.size() - 1) % remaining.size());
                int b = remaining.get(i);
                int c = remaining.get((i + 1) % remaining.size());
                if (direction * cross(polygon.get(a), polygon.get(b), polygon.get(c)) <= EPSILON) {
                    continue;
                }
                boolean blocked = false;
                for (int other : remaining) {
                    if (other != a && other != b && other != c &&
                        inTriangle(polygon.get(other), polygon.get(a), polygon.get(b),
                                   polygon.get(c), direction)) {
                        blocked = true;
                        break;
                    }
                }
                if (!blocked) {
                    triangles.add(new int[] {a, b, c});
                    remaining.remove(i);
                    removed = true;
                    break;
                }
            }
            if (!removed) {
                throw new IllegalArgumentException("no nondegenerate ear within tolerance");
            }
        }
        int a = remaining.get(0);
        int b = remaining.get(1);
        int c = remaining.get(2);
        if (direction * cross(polygon.get(a), polygon.get(b), polygon.get(c)) <= EPSILON) {
            throw new IllegalArgumentException("degenerate final triangle");
        }
        triangles.add(new int[] {a, b, c});
        return triangles;
    }

    /** Minimum SUM OF TRIANGLE PERIMETERS for a strictly convex polygon, O(n^3). */
    public static double minimumWeightTriangulation(List<Point> polygon) {
        double direction = validatePolygon(polygon);
        int n = polygon.size();
        for (int i = 0; i < n; i++) {
            if (direction *
                    cross(polygon.get(i), polygon.get((i + 1) % n), polygon.get((i + 2) % n)) <=
                EPSILON) {
                throw new IllegalArgumentException("strictly convex polygon required");
            }
        }
        double[][] cost = new double[n][n];
        for (int gap = 2; gap < n; gap++) {
            for (int i = 0; i + gap < n; i++) {
                int j = i + gap;
                cost[i][j] = Double.POSITIVE_INFINITY;
                for (int k = i + 1; k < j; k++) {
                    double perimeter = distance(polygon.get(i), polygon.get(k)) +
                                       distance(polygon.get(k), polygon.get(j)) +
                                       distance(polygon.get(j), polygon.get(i));
                    cost[i][j] =
                        Math.min(cost[i][j], Numeric.finite(cost[i][k] + cost[k][j] + perimeter));
                }
            }
        }
        return cost[0][n - 1];
    }

    private static void packingDomain(double width, double height, double radius) {
        Numeric.finite(width);
        Numeric.finite(height);
        Numeric.finite(radius);
        if (width <= 0 || height <= 0 || radius <= 0 || !Double.isFinite(2 * radius)) {
            throw new IllegalArgumentException(
                "positive finite box dimensions and radius required");
        }
    }
    private static long count(double value) {
        if (!Double.isFinite(value) || value < 0 || value >= 0x1.0p63) {
            throw new ArithmeticException("packing count overflows long");
        }
        return (long)Math.floor(value);
    }
    public static long denseLayers(double width, double height, double radius) {
        packingDomain(width, height, radius);
        if (width < 2 * radius || height < 2 * radius) {
            return 0;
        }
        return Math.addExact(1, count((height - 2 * radius) / (Math.sqrt(3) * radius)));
    }
    public static long platesPerRow(long row, double width, double radius) {
        packingDomain(width, width, radius);
        if (row < 0) {
            throw new IllegalArgumentException("negative row");
        }
        if (width < 2 * radius) {
            return 0;
        }
        return count((width - (row % 2 == 0 ? 0 : radius)) / (2 * radius));
    }
    public static long densePlates(double width, double height, double radius) {
        long layers = denseLayers(width, height, radius);
        long even = Math.multiplyExact(layers / 2 + layers % 2, platesPerRow(0, width, radius));
        long odd = Math.multiplyExact(layers / 2, platesPerRow(1, width, radius));
        return Math.addExact(even, odd);
    }
    public static long gridPlates(double width, double height, double radius) {
        packingDomain(width, height, radius);
        return Math.multiplyExact(count(width / (2 * radius)), count(height / (2 * radius)));
    }
    public static long[] packing(double width, double height, double radius) {
        return new long[] {
            gridPlates(width, height, radius),
            Math.max(densePlates(width, height, radius), densePlates(height, width, radius))};
    }
    public static Point hexToGeo(double xh, double yh, double radius) {
        packingDomain(1, 1, radius);
        return new Point(radius * xh + 2 * radius * yh, Math.sqrt(3) * radius * xh);
    }
    public static Point geoToHex(Point point, double radius) {
        packingDomain(1, 1, radius);
        double xh = point.y / (Math.sqrt(3) * radius);
        return new Point(xh, (point.x - radius * xh) / (2 * radius));
    }
    public static int[] arrayToHex(int row, int column) {
        return new int[] {row, Math.subtractExact(column, Math.floorDiv(row, 2))};
    }
    public static int[] hexToArray(int row, int diagonal) {
        return new int[] {row, Math.addExact(diagonal, Math.floorDiv(row, 2))};
    }
    public static long platesOnTop(int row, int diagonal, double width, double height,
                                   double radius) {
        long layers = denseLayers(width, height, radius);
        int[] array = hexToArray(row, diagonal);
        if (row < 0 || row >= layers || array[1] < 0 ||
            array[1] >= platesPerRow(row, width, radius)) {
            throw new IllegalArgumentException("plate outside packing");
        }
        long total = 0;
        for (long current = row + 1L; current < layers; current++) {
            long left = Math.max(0, diagonal - (current - row) + Math.floorDiv(current, 2));
            long right = Math.min(platesPerRow(current, width, radius) - 1,
                                  diagonal + Math.floorDiv(current, 2));
            total = Math.addExact(total, Math.max(0, right - left + 1));
        }
        return total;
    }

    /** Original independent chord/arc model, not a general shortest-path solver. */
    public static double[] superman(Point source, Point target, List<Circle> circles) {
        for (int i = 0; i < circles.size(); i++) {
            Circle circle = circles.get(i);
            if (distance(source, circle.center) < circle.radius - EPSILON ||
                distance(target, circle.center) < circle.radius - EPSILON) {
                throw new IllegalArgumentException("endpoint inside obstacle");
            }
            for (int j = 0; j < i; j++) {
                Circle other = circles.get(j);
                if (distance(circle.center, other.center) <
                    circle.radius + other.radius - EPSILON) {
                    throw new IllegalArgumentException(
                        "overlapping obstacles are outside this model");
                }
            }
        }
        double length = distance(source, target);
        if (length == 0) {
            return new double[] {0, 0};
        }
        double dx = (target.x - source.x) / length;
        double dy = (target.y - source.y) / length;
        double through = 0;
        double around = 0;
        for (Circle circle : circles) {
            double along = (circle.center.x - source.x) * dx + (circle.center.y - source.y) * dy;
            double perpendicular =
                Math.abs((circle.center.x - source.x) * dy - (circle.center.y - source.y) * dx);
            if (along < 0 || along > length || perpendicular >= circle.radius) {
                continue;
            }
            double halfChord = Math.sqrt(
                Math.max(0, circle.radius * circle.radius - perpendicular * perpendicular));
            if (along - halfChord < -EPSILON || along + halfChord > length + EPSILON) {
                throw new IllegalArgumentException("partial obstacle crossing outside this model");
            }
            through += 2 * halfChord;
            around += 2 * circle.radius * Math.acos(Math.min(1, perpendicular / circle.radius));
        }
        return new double[] {Numeric.finite(through), Numeric.finite(length - through + around)};
    }
}
