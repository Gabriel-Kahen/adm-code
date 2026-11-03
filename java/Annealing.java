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

public final class Annealing {
    /** Repeated independent heuristic runs; returns the best of the documented seed sequence. */
    public static Tsp.Tour repeatedTsp(List<Geometry.Point> points, String method, long seed,
                                       int iterations, int runs) {
        if (runs < 1) {
            throw new IllegalArgumentException("restart count must be positive");
        }
        if (!method.equals("sample") && !method.equals("hill") && !method.equals("anneal")) {
            throw new IllegalArgumentException("restarts require a heuristic TSP method");
        }
        Tsp.Tour best = Tsp.tsp(points, method, seed, iterations);
        for (int run = 1; run < runs; run++) {
            Tsp.Tour candidate = Tsp.tsp(points, method, seed + run, iterations);
            if (candidate.cost() < best.cost()) {
                best = candidate;
            }
        }
        return best;
    }

    static Tsp.Tour heuristicTsp(List<Geometry.Point> points, String method, long seed,
                                 int iterations) {
        int[] current = Tsp.identityTour(points.size());
        int[] best = current.clone();
        double currentCost = Tsp.cost(points, current);
        double bestCost = currentCost;
        if (points.size() < 2) {
            return new Tsp.Tour(bestCost, best);
        }
        Random random = new Random(seed);
        double initialTemperature = Math.max(1, currentCost / points.size());
        for (int iteration = 0; iteration < iterations; iteration++) {
            if (method.equals("sample")) {
                random.shuffle(current);
                currentCost = Tsp.cost(points, current);
            } else {
                int i = random.integer(0, current.length - 1);
                int j = random.integer(0, current.length - 1);
                Tsp.swap(current, i, j);
                double candidate = Tsp.cost(points, current);
                double temperature = initialTemperature *
                                     Math.pow(0.001, (double)iteration / Math.max(1, iterations));
                boolean accept = candidate < currentCost;
                if (method.equals("anneal") && !accept) {
                    accept = random.real(0, 1) < Math.exp((currentCost - candidate) / temperature);
                }
                if (accept) {
                    currentCost = candidate;
                } else {
                    Tsp.swap(current, i, j);
                }
            }
            if (currentCost < bestCost) {
                bestCost = currentCost;
                best = current.clone();
            }
        }
        return new Tsp.Tour(bestCost, best);
    }
}
