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
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

/** Dynamic programming with explicit witnesses. String positions are UTF-16 code units. */
public final class Dynamic {
    private Dynamic() {}
    public record Edit(int cost, String operations) {}

    /** Unit-cost Levenshtein distance and an executable M/S/I/D alignment. O(mn). */
    public static Edit edit(String source, String target) {
        int[][] cost = editTable(source, target, false);
        int i = source.length();
        int j = target.length();
        StringBuilder reversed = new StringBuilder();
        while (i > 0 || j > 0) {
            if (i > 0 && j > 0 &&
                cost[i][j] ==
                    cost[i - 1][j - 1] + (source.charAt(i - 1) == target.charAt(j - 1) ? 0 : 1)) {
                reversed.append(source.charAt(i - 1) == target.charAt(j - 1) ? 'M' : 'S');
                i--;
                j--;
            } else if (i > 0 && cost[i][j] == cost[i - 1][j] + 1) {
                reversed.append('D');
                i--;
            } else {
                reversed.append('I');
                j--;
            }
        }
        return new Edit(cost[source.length()][target.length()], reversed.reverse().toString());
    }
    private static int[][] editTable(String source, String target, boolean freePrefix) {
        int[][] cost = new int[source.length() + 1][target.length() + 1];
        for (int i = 0; i <= source.length(); i++) {
            cost[i][0] = i;
        }
        for (int j = 0; j <= target.length(); j++) {
            cost[0][j] = freePrefix ? 0 : j;
        }
        for (int i = 1; i <= source.length(); i++) {
            for (int j = 1; j <= target.length(); j++) {
                int diagonal =
                    cost[i - 1][j - 1] + (source.charAt(i - 1) == target.charAt(j - 1) ? 0 : 1);
                cost[i][j] = Math.min(diagonal, 1 + Math.min(cost[i - 1][j], cost[i][j - 1]));
            }
        }
        return cost;
    }

    /** Deliberately exponential recursive reference for source.length+target.length <= 18. */
    public static int editBrute(String source, String target) {
        if (source.length() + target.length() > 18) {
            throw new IllegalArgumentException("brute edit input too long");
        }
        return brute(source, target, source.length(), target.length());
    }
    private static int brute(String source, String target, int i, int j) {
        if (i == 0) {
            return j;
        }
        if (j == 0) {
            return i;
        }
        return Math.min(
            brute(source, target, i - 1, j - 1) +
                (source.charAt(i - 1) == target.charAt(j - 1) ? 0 : 1),
            1 + Math.min(brute(source, target, i - 1, j), brute(source, target, i, j - 1)));
    }

    /** Longest common subsequence, O(mn) time and memory. */
    public static String lcs(String source, String target) {
        int[][] length = new int[source.length() + 1][target.length() + 1];
        for (int i = 1; i <= source.length(); i++) {
            for (int j = 1; j <= target.length(); j++) {
                if (source.charAt(i - 1) == target.charAt(j - 1)) {
                    length[i][j] = length[i - 1][j - 1] + 1;
                } else {
                    length[i][j] = Math.max(length[i - 1][j], length[i][j - 1]);
                }
            }
        }
        StringBuilder result = new StringBuilder();
        int i = source.length();
        int j = target.length();
        while (i > 0 && j > 0) {
            if (source.charAt(i - 1) == target.charAt(j - 1)) {
                result.append(source.charAt(i - 1));
                i--;
                j--;
            } else if (length[i - 1][j] >= length[i][j - 1]) {
                i--;
            } else {
                j--;
            }
        }
        return result.reverse().toString();
    }

    /** Minimum edit distance from pattern to ANY substring of text, including empty. */
    public static int substring(String pattern, String text) {
        int[][] cost = editTable(pattern, text, true);
        int result = pattern.length();
        for (int value : cost[pattern.length()]) {
            result = Math.min(result, value);
        }
        return result;
    }

    public record Partition(long cost, List<List<Long>> groups) {}

    /** k nonempty contiguous groups minimizing the largest sum. O(k n^2), nonnegative values. */
    public static Partition partition(long[] values, int k) {
        int n = values.length;
        if (k < 1 || k > n) {
            throw new IllegalArgumentException("require 1 <= groups <= item count");
        }
        long[] prefix = new long[n + 1];
        for (int i = 0; i < n; i++) {
            if (values[i] < 0) {
                throw new IllegalArgumentException("negative partition value");
            }
            prefix[i + 1] = Math.addExact(prefix[i], values[i]);
        }
        Long[][] cost = new Long[k + 1][n + 1];
        int[][] parent = new int[k + 1][n + 1];
        cost[0][0] = 0L;
        for (int groups = 1; groups <= k; groups++) {
            for (int end = groups; end <= n; end++) {
                for (int split = groups - 1; split < end; split++) {
                    if (cost[groups - 1][split] == null) {
                        continue;
                    }
                    long candidate = Math.max(cost[groups - 1][split], prefix[end] - prefix[split]);
                    if (cost[groups][end] == null || candidate < cost[groups][end]) {
                        cost[groups][end] = candidate;
                        parent[groups][end] = split;
                    }
                }
            }
        }
        List<List<Long>> result = new ArrayList<>();
        int end = n;
        for (int groups = k; groups > 0; groups--) {
            int start = parent[groups][end];
            List<Long> group = new ArrayList<>();
            for (int i = start; i < end; i++) {
                group.add(values[i]);
            }
            result.add(group);
            end = start;
        }
        Collections.reverse(result);
        return new Partition(cost[k][n], result);
    }

    /** 0/1 subset sum witness as increasing original indices. O(n target), target <= 1,000,000. */
    public static List<Integer> subsetSum(long[] values, int target) {
        if (target < 0 || target > 1000000) {
            throw new IllegalArgumentException("target outside 0..1000000");
        }
        int[] item = new int[target + 1];
        int[] previous = new int[target + 1];
        Arrays.fill(item, -1);
        item[0] = -2;
        for (int index = 0; index < values.length; index++) {
            if (values[index] < 0) {
                throw new IllegalArgumentException("negative subset sum value");
            }
            if (values[index] == 0 || values[index] > target) {
                continue;
            }
            int value = (int)values[index];
            for (int sum = target; sum >= value; sum--) {
                if (item[sum] == -1 && item[sum - value] != -1) {
                    item[sum] = index;
                    previous[sum] = sum - value;
                }
            }
        }
        if (item[target] == -1) {
            return null;
        }
        List<Integer> result = new ArrayList<>();
        for (int sum = target; sum != 0; sum = previous[sum]) {
            result.add(item[sum]);
        }
        Collections.reverse(result);
        return result;
    }

    public record Elevator(long cost, List<Integer> stops) {}

    /** At most budget stops on integer floors 1..maxFloor; floor 0 is always available. */
    public static Elevator elevator(int[] destinations, int budget, int maxFloor) {
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
        return new Elevator(best, stops);
    }
}
