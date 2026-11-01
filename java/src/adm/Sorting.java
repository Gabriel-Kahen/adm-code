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

import java.util.Arrays;

/** Comparison sorting without modifying the caller's array. */
public final class Sorting {
    private Sorting() {}

    public static long[] sort(String method, long[] input) {
        long[] a = input.clone();
        switch (method) {
        case "insertion" -> insertion(a);
        case "selection" -> selection(a);
        case "quick" -> quick(a, 0, a.length - 1);
        case "heap" -> heap(a);
        case "merge" -> merge(a, new long[a.length], 0, a.length);
        default -> throw new IllegalArgumentException("unknown sorting method");
        }
        return a;
    }
    private static void insertion(long[] a) {
        for (int i = 1; i < a.length; i++) {
            long value = a[i];
            int j = i;
            while (j > 0 && a[j - 1] > value) {
                a[j] = a[j - 1];
                j--;
            }
            a[j] = value;
        }
    }
    private static void selection(long[] a) {
        for (int i = 0; i < a.length; i++) {
            int minimum = i;
            for (int j = i + 1; j < a.length; j++) {
                if (a[j] < a[minimum]) {
                    minimum = j;
                }
            }
            swap(a, i, minimum);
        }
    }
    // Recurse into the smaller partition only, keeping call depth O(log n).
    private static void quick(long[] a, int low, int high) {
        while (low < high) {
            long pivot = a[low + (high - low) / 2];
            int left = low;
            int right = high;
            while (left <= right) {
                while (a[left] < pivot) {
                    left++;
                }
                while (a[right] > pivot) {
                    right--;
                }
                if (left <= right) {
                    swap(a, left, right);
                    left++;
                    right--;
                }
            }
            if (right - low < high - left) {
                quick(a, low, right);
                low = left;
            } else {
                quick(a, left, high);
                high = right;
            }
        }
    }
    private static void heap(long[] a) {
        for (int i = a.length / 2 - 1; i >= 0; i--) {
            sift(a, i, a.length);
        }
        for (int end = a.length - 1; end > 0; end--) {
            swap(a, 0, end);
            sift(a, 0, end);
        }
    }
    private static void sift(long[] a, int root, int size) {
        while (2L * root + 1 < size) {
            int child = 2 * root + 1;
            if (child + 1 < size && a[child] < a[child + 1]) {
                child++;
            }
            if (a[root] >= a[child]) {
                return;
            }
            swap(a, root, child);
            root = child;
        }
    }
    private static void merge(long[] a, long[] buffer, int low, int high) {
        if (high - low <= 1) {
            return;
        }
        int middle = low + (high - low) / 2;
        merge(a, buffer, low, middle);
        merge(a, buffer, middle, high);
        int left = low;
        int right = middle;
        for (int i = low; i < high; i++) {
            if (right == high || (left < middle && a[left] <= a[right])) {
                buffer[i] = a[left++];
            } else {
                buffer[i] = a[right++];
            }
        }
        System.arraycopy(buffer, low, a, low, high - low);
    }
    private static void swap(long[] a, int i, int j) {
        long value = a[i];
        a[i] = a[j];
        a[j] = value;
    }

    /** Lower-bound binary search; first matching position, or -1. O(log n). */
    public static int binarySearch(long[] sorted, long target) {
        int low = 0;
        int high = sorted.length;
        while (low < high) {
            int middle = low + (high - low) / 2;
            if (sorted[middle] < target) {
                low = middle + 1;
            } else {
                high = middle;
            }
        }
        return low < sorted.length && sorted[low] == target ? low : -1;
    }

    /** Sentinel insertion expressed without an out-of-domain numeric sentinel. O(n). */
    public static long[] insert(long[] sorted, long value) {
        for (int i = 1; i < sorted.length; i++) {
            if (sorted[i] < sorted[i - 1]) {
                throw new IllegalArgumentException("array must be sorted");
            }
        }
        long[] result = Arrays.copyOf(sorted, sorted.length + 1);
        int i = sorted.length;
        while (i > 0 && result[i - 1] > value) {
            result[i] = result[i - 1];
            i--;
        }
        result[i] = value;
        return result;
    }
}
