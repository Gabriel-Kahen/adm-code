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
import java.util.Collections;
import java.util.List;

public final class Elevator {
    public record Result(long cost, List<Integer> stops) {}

    /** At most budget stops on integer floors 1..maxFloor; floor 0 is always available. */
    public static Result elevator(int[] destinations, int budget, int maxFloor) {
        if (budget < 0 || maxFloor < 0 || maxFloor > 1000) {
            throw new IllegalArgumentException("invalid elevator budget or floor bound (0..1000)");
        }
        for (int floor : destinations) {
            if (floor < 0 || floor > maxFloor) {
                throw new IllegalArgumentException("destination outside building");
            }
        }
        int k = Math.min(budget, maxFloor);
        long[] above = new long[maxFloor + 1];
        long[][] between = new long[maxFloor + 1][maxFloor + 1];
        for (int previous = 0; previous <= maxFloor; previous++) {
            for (int floor : destinations) {
                if (floor > previous) {
                    above[previous] += floor - previous;
                }
            }
            for (int current = previous + 1; current <= maxFloor; current++) {
                for (int floor : destinations) {
                    if (floor > previous && floor <= current) {
                        between[previous][current] += Math.min(floor - previous, current - floor);
                    }
                }
            }
        }
        Long[][] cost = new Long[k + 1][maxFloor + 1];
        int[][] parent = new int[k + 1][maxFloor + 1];
        cost[0][0] = above[0];
        long best = above[0];
        int bestCount = 0;
        int bestFloor = 0;
        for (int used = 1; used <= k; used++) {
            for (int current = used; current <= maxFloor; current++) {
                for (int previous = 0; previous < current; previous++) {
                    if (cost[used - 1][previous] == null) {
                        continue;
                    }
                    long candidate = cost[used - 1][previous] - above[previous] +
                                     between[previous][current] + above[current];
                    if (cost[used][current] == null || candidate < cost[used][current]) {
                        cost[used][current] = candidate;
                        parent[used][current] = previous;
                    }
                }
                if (cost[used][current] != null && cost[used][current] < best) {
                    best = cost[used][current];
                    bestCount = used;
                    bestFloor = current;
                }
            }
        }
        List<Integer> stops = new ArrayList<>();
        for (int used = bestCount, floor = bestFloor; used > 0; used--) {
            stops.add(floor);
            floor = parent[used][floor];
        }
        Collections.reverse(stops);
        return new Result(best, stops);
    }

    public static void main(String[] args) {
        System.out.println(elevator(new int[] {1, 3, 6}, 2, 6));
    }
}
