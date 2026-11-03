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

public final class Partition {
    public record Result(long cost, List<List<Long>> groups) {}

    /** k nonempty contiguous groups minimizing the largest sum. O(k n^2), nonnegative values. */
    public static Result partition(long[] values, int k) {
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
        return new Result(cost[k][n], result);
    }

    public static void main(String[] args) {
        System.out.println(partition(new long[] {1, 2, 3}, 2));
    }
}
