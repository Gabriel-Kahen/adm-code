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

public final class Tsp {
    public record Tour(double cost, int[] tour) {}

    public static int[] identityTour(int n) {
        if (n < 0) {
            throw new IllegalArgumentException("negative tour size");
        }
        int[] result = new int[n];
        for (int i = 0; i < n; i++) {
            result[i] = i;
        }
        return result;
    }

    public static double tourCost(List<Geometry.Point> points, int[] tour) {
        validateTour(points, tour);
        return cost(points, tour);
    }

    static void validateTour(List<Geometry.Point> points, int[] tour) {
        if (tour.length != points.size()) {
            throw new IllegalArgumentException("tour must visit every city");
        }
        boolean[] seen = new boolean[tour.length];
        for (int city : tour) {
            if (city < 0 || city >= tour.length || seen[city]) {
                throw new IllegalArgumentException("invalid tour permutation");
            }
            seen[city] = true;
        }
    }

    static double cost(List<Geometry.Point> points, int[] tour) {
        double result = 0;
        for (int i = 0; i < tour.length; i++) {
            result = Geometry.finite(
                result +
                Geometry.distance(points.get(tour[i]), points.get(tour[(i + 1) % tour.length])));
        }
        return result;
    }

    /** Recomputed O(n) swap delta handles neighbors, closing edge and very small tours. */
    public static double swapDelta(List<Geometry.Point> points, int[] tour, int i, int j) {
        validateTour(points, tour);
        if (i < 0 || j < 0 || i >= tour.length || j >= tour.length) {
            throw new IllegalArgumentException("invalid swap position");
        }
        double before = cost(points, tour);
        int[] changed = tour.clone();
        swap(changed, i, j);
        return cost(points, changed) - before;
    }

    static void swap(int[] a, int i, int j) {
        int value = a[i];
        a[i] = a[j];
        a[j] = value;
    }

    public static Tour tsp(List<Geometry.Point> points, String method, long seed, int iterations) {
        if (iterations < 0) {
            throw new IllegalArgumentException("negative search budget");
        }
        return switch (method) {
            case "exact" -> TspAstar.exactTsp(points, false);
            case "best" -> TspAstar.exactTsp(points, true);
            case "sample", "hill", "anneal" ->
                Annealing.heuristicTsp(points, method, seed, iterations);
            default -> throw new IllegalArgumentException("unknown TSP method");
        };
    }

    public static void main(String[] args) {
        System.out.println(tsp(List.of(new Geometry.Point(0, 0), new Geometry.Point(1, 0),
                                       new Geometry.Point(1, 1), new Geometry.Point(0, 1)),
                               "hill", 0, 100)
                               .cost());
    }
}
