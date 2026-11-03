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

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public final class Triangulate {
    static double validatePolygon(List<Geometry.Point> polygon) {
        int n = polygon.size();
        if (n < 3 || Geometry.area(polygon) <= Geometry.EPSILON) {
            throw new IllegalArgumentException("nondegenerate polygon required");
        }
        for (int i = 0; i < n; i++) {
            Geometry.Point a = polygon.get(i);
            Geometry.Point b = polygon.get((i + 1) % n);
            if (Geometry.distance(a, b) <= Geometry.EPSILON) {
                throw new IllegalArgumentException("duplicate adjacent vertex");
            }
            Geometry.Point previous = polygon.get((i + n - 1) % n);
            if (Geometry.orientation(previous, a, b) == 0) {
                double dot = (a.x() - previous.x()) * (b.x() - a.x()) +
                             (a.y() - previous.y()) * (b.y() - a.y());
                if (dot < 0) {
                    throw new IllegalArgumentException("overlapping boundary edges");
                }
            }
            for (int j = i + 1; j < n; j++) {
                if (j == i + 1 || (i == 0 && j == n - 1)) {
                    continue;
                }
                if (Geometry.segmentsIntersect(a, b, polygon.get(j), polygon.get((j + 1) % n))) {
                    throw new IllegalArgumentException("self-intersecting polygon");
                }
            }
        }
        return Math.signum(Geometry.signedArea(polygon));
    }

    static boolean inTriangle(Geometry.Point p, Geometry.Point a, Geometry.Point b,
                              Geometry.Point c, double direction) {
        return direction * Geometry.cross(a, b, p) >= -Geometry.EPSILON &&
            direction * Geometry.cross(b, c, p) >= -Geometry.EPSILON &&
            direction * Geometry.cross(c, a, p) >= -Geometry.EPSILON;
    }

    /** Ear clipping, O(n^3) in this direct implementation. Either boundary orientation is accepted. */
    public static List<int[]> triangulate(List<Geometry.Point> polygon) {
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
                if (direction * Geometry.cross(polygon.get(a), polygon.get(b), polygon.get(c)) <=
                    Geometry.EPSILON) {
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
        if (direction * Geometry.cross(polygon.get(a), polygon.get(b), polygon.get(c)) <=
            Geometry.EPSILON) {
            throw new IllegalArgumentException("degenerate final triangle");
        }
        triangles.add(new int[] {a, b, c});
        return triangles;
    }

    /** Minimum SUM OF TRIANGLE PERIMETERS for a strictly convex polygon, O(n^3). */
    public static double minimumWeightTriangulation(List<Geometry.Point> polygon) {
        double direction = validatePolygon(polygon);
        int n = polygon.size();
        for (int i = 0; i < n; i++) {
            if (direction * Geometry.cross(polygon.get(i), polygon.get((i + 1) % n),
                                           polygon.get((i + 2) % n)) <=
                Geometry.EPSILON) {
                throw new IllegalArgumentException("strictly convex polygon required");
            }
        }
        double[][] cost = new double[n][n];
        for (int gap = 2; gap < n; gap++) {
            for (int i = 0; i + gap < n; i++) {
                int j = i + gap;
                cost[i][j] = Double.POSITIVE_INFINITY;
                for (int k = i + 1; k < j; k++) {
                    double perimeter = Geometry.distance(polygon.get(i), polygon.get(k)) +
                                       Geometry.distance(polygon.get(k), polygon.get(j)) +
                                       Geometry.distance(polygon.get(j), polygon.get(i));
                    cost[i][j] =
                        Math.min(cost[i][j], Geometry.finite(cost[i][k] + cost[k][j] + perimeter));
                }
            }
        }
        return cost[0][n - 1];
    }

    public static void main(String[] args) {
        for (int[] triangle :
             triangulate(List.of(new Geometry.Point(0, 0), new Geometry.Point(1, 0),
                                 new Geometry.Point(1, 1), new Geometry.Point(0, 1))))
            System.out.println(Arrays.toString(triangle));
    }
}
