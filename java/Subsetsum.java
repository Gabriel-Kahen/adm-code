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
import java.util.Collections;
import java.util.List;

public final class Subsetsum {
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

    public static void main(String[] args) {
        System.out.println(subsetSum(new long[] {1, 3, 4}, 7));
    }
}
