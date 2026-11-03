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
import java.util.Comparator;
import java.util.List;

public final class TspAstar {
    static double[][] distances(List<Geometry.Point> points) {
        double[][] distance = new double[points.size()][points.size()];
        for (int i = 0; i < points.size(); i++) {
            for (int j = 0; j < points.size(); j++) {
                distance[i][j] = Geometry.distance(points.get(i), points.get(j));
            }
        }
        return distance;
    }

    record Partial(int[] path, boolean[] used, double cost, double bound) {}

    static Tsp.Tour exactTsp(List<Geometry.Point> points, boolean bestFirst) {
        int n = points.size();
        if (n > 12) {
            throw new IllegalArgumentException("exact TSP limited to 12 cities");
        }
        int[] incumbent = Tsp.identityTour(n);
        double upperBound = Tsp.cost(points, incumbent);
        if (n <= 1) {
            return new Tsp.Tour(upperBound, incumbent);
        }
        double[][] distance = distances(points);
        boolean[] used = new boolean[n];
        used[0] = true;
        Partial root = new Partial(new int[] {0}, used, 0, lowerBound(distance, used, 0, 0));
        if (!bestFirst) {
            Best best = new Best(upperBound, incumbent);
            exactVisit(distance, root, best);
            return new Tsp.Tour(best.cost, best.tour);
        }
        TspPq<Partial> frontier =
            new TspPq<>(Comparator.comparingDouble(Partial::bound)
                            .thenComparingInt(partial -> - partial.path.length),
                        1000000);
        frontier.add(root);
        while (!frontier.isEmpty()) {
            Partial partial = frontier.remove();
            if (partial.bound >= upperBound) {
                continue;
            }
            if (partial.path.length == n) {
                double complete = partial.cost + distance[partial.path[n - 1]][0];
                if (complete < upperBound) {
                    upperBound = complete;
                    incumbent = partial.path;
                }
                continue;
            }
            for (Partial child : children(distance, partial)) {
                if (child.bound < upperBound) {
                    if (frontier.size() >= 1000000) {
                        throw new IllegalStateException("exact TSP frontier exhausted");
                    }
                    frontier.add(child);
                }
            }
        }
        return new Tsp.Tour(upperBound, incumbent);
    }

    static final class Best {
        double cost;
        int[] tour;
        Best(double cost, int[] tour) {
            this.cost = cost;
            this.tour = tour;
        }
    }

    static void exactVisit(double[][] distance, Partial partial, Best best) {
        if (partial.bound >= best.cost) {
            return;
        }
        if (partial.path.length == distance.length) {
            double complete = partial.cost + distance[partial.path[partial.path.length - 1]][0];
            if (complete < best.cost) {
                best.cost = complete;
                best.tour = partial.path;
            }
            return;
        }
        List<Partial> children = children(distance, partial);
        children.sort(Comparator.comparingDouble(Partial::bound));
        for (Partial child : children) {
            exactVisit(distance, child, best);
        }
    }

    static List<Partial> children(double[][] distance, Partial parent) {
        List<Partial> result = new ArrayList<>();
        int last = parent.path[parent.path.length - 1];
        for (int next = 0; next < distance.length; next++) {
            if (parent.used[next]) {
                continue;
            }
            int[] path = Arrays.copyOf(parent.path, parent.path.length + 1);
            path[path.length - 1] = next;
            boolean[] used = parent.used.clone();
            used[next] = true;
            double accumulated = Geometry.finite(parent.cost + distance[last][next]);
            result.add(new Partial(path, used, accumulated,
                                   lowerBound(distance, used, next, accumulated)));
        }
        return result;
    }

    // Any completion contains a tree on remaining vertices and one link to each endpoint.
    static double lowerBound(double[][] distance, boolean[] used, int last, double accumulated) {
        int n = used.length;
        int firstRemaining = -1;
        double fromLast = Double.POSITIVE_INFINITY;
        double fromStart = Double.POSITIVE_INFINITY;
        for (int v = 0; v < n; v++) {
            if (!used[v]) {
                firstRemaining = v;
                fromLast = Math.min(fromLast, distance[last][v]);
                fromStart = Math.min(fromStart, distance[0][v]);
            }
        }
        if (firstRemaining == -1) {
            return accumulated + distance[last][0];
        }
        boolean[] included = used.clone();
        double[] key = new double[n];
        Arrays.fill(key, Double.POSITIVE_INFINITY);
        key[firstRemaining] = 0;
        double tree = 0;
        while (true) {
            int next = -1;
            for (int v = 0; v < n; v++) {
                if (!included[v] && (next == -1 || key[v] < key[next])) {
                    next = v;
                }
            }
            if (next == -1) {
                break;
            }
            included[next] = true;
            tree += key[next];
            for (int v = 0; v < n; v++) {
                if (!included[v]) {
                    key[v] = Math.min(key[v], distance[next][v]);
                }
            }
        }
        return Geometry.finite(accumulated + tree + fromLast + fromStart);
    }

    public static void main(String[] args) {
        System.out.println(exactTsp(List.of(new Geometry.Point(0, 0), new Geometry.Point(1, 0),
                                            new Geometry.Point(1, 1), new Geometry.Point(0, 1)),
                                    true)
                               .cost());
    }
}
