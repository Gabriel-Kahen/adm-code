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
import java.util.Comparator;
import java.util.List;

public final class ConvexHull {
    /** Monotone chain, O(n log n). Duplicates and interior collinear points are removed. */
    public static List<Geometry.Point> convexHull(List<Geometry.Point> input) {
        List<Geometry.Point> points = new ArrayList<>(input);
        points.sort(
            Comparator.comparingDouble(Geometry.Point::x).thenComparingDouble(Geometry.Point::y));
        List<Geometry.Point> unique = new ArrayList<>();
        for (Geometry.Point point : points) {
            if (unique.isEmpty() || !point.equals(unique.get(unique.size() - 1))) {
                unique.add(point);
            }
        }
        if (unique.size() <= 1) {
            return unique;
        }
        List<Geometry.Point> lower = new ArrayList<>();
        for (Geometry.Point point : unique) {
            appendHull(lower, point);
        }
        List<Geometry.Point> upper = new ArrayList<>();
        for (int i = unique.size() - 1; i >= 0; i--) {
            appendHull(upper, unique.get(i));
        }
        lower.remove(lower.size() - 1);
        upper.remove(upper.size() - 1);
        lower.addAll(upper);
        return lower;
    }

    static void appendHull(List<Geometry.Point> hull, Geometry.Point point) {
        while (hull.size() >= 2 &&
               Geometry.cross(hull.get(hull.size() - 2), hull.get(hull.size() - 1), point) <=
                   Geometry.EPSILON) {
            hull.remove(hull.size() - 1);
        }
        hull.add(point);
    }

    public static void main(String[] args) {
        java.util.Scanner in = new java.util.Scanner(System.in);
        List<Geometry.Point> points = new ArrayList<>();
        if (in.hasNextInt()) {
            int n = in.nextInt();
            for (int i = 0; i < n; i++) {
                points.add(new Geometry.Point(in.nextDouble(), in.nextDouble()));
            }
        } else {
            points = List.of(new Geometry.Point(0, 0), new Geometry.Point(1, 0),
                             new Geometry.Point(1, 1), new Geometry.Point(0, 1));
        }
        System.out.println(convexHull(points));
    }
}
