/*    sorting.c

    Implementations of primary sorting algorithms
*/

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

import java.util.Locale;

public class Sorting {
    public static final int PQ_SIZE = 1000;
    public static final int QUEUESIZE = 1000;
    public static final int NELEM = 100; /* size of test arrays */
    public static final int LESS_THAN = -1;
    public static final int EQUAL_TO = 0;
    public static final int GREATER_THAN = 1;

    public static int compare(int a, int b) {
        if ((a < b)) {
            return LESS_THAN;
        }
        if ((a > b)) {
            return GREATER_THAN;
        }
        return EQUAL_TO;
    }

    /*    Swap the ith and jth elements of array s.    */
    public static void newswap(int[] s, int i, int j) {
        int tmp = 0; /* placeholder */
        tmp = s[i];
        s[i] = s[j];
        s[j] = tmp;
    }

    public static void insertion_sort(int[] s, int n) {
        int i = 0; /* counters */
        int j = 0;
        for (i = 1; (i < n); i++) {
            j = i;
            while (((j > 0) && (s[j] < s[(j - 1)]))) {
                Random.swap(s, j, s, (j - 1));
                j = (j - 1);
            }
        }
    }

    public static void selection_sort(int[] s, int n) {
        int i = 0; /* counters */
        int j = 0;
        int min = 0; /* index of minimum */
        for (i = 0; (i < n); i++) {
            min = i;
            for (j = (i + 1); (j < n); j++) {
                if ((s[j] < s[min])) {
                    min = j;
                }
            }
            Random.swap(s, i, s, min);
        }
    }

    public static int partition(int[] s, int l, int h) {
        int i = 0; /* counter */
        int p = 0; /* pivot element index */
        int firsthigh = 0; /* divider position for pivot element */
        p = h; /* select last element as pivot */
        firsthigh = l;
        for (i = l; (i < h); i++) {
            if ((s[i] < s[p])) {
                Random.swap(s, i, s, firsthigh);
                firsthigh++;
            }
        }
        Random.swap(s, p, s, firsthigh);
        return firsthigh;
    }

    /*    quicksort array s from the index l to index h.    */
    public static void quicksort(int[] s, int l, int h) {
        int p = 0; /* index of partition */
        if ((l < h)) {
            p = partition(s, l, h);
            quicksort(s, l, (p - 1));
            quicksort(s, (p + 1), h);
        }
    }

    public static void heapsort_(int[] s, int n) {
        int i = 0; /* counters */
        PriorityQueue.priority_queue q = new PriorityQueue.priority_queue(); /* heap for heapsort */
        PriorityQueue.make_heap(q, s, n);
        for (i = 0; (i < n); i++) {
            s[i] = PriorityQueue.extract_min(q);
        }
    }

    public static int binary_search(int[] s, int key, int low, int high) {
        int middle = 0; /* index of middle element */
        if ((low > high)) {
            return (-1); /* key not found */
        }
        middle = ((low + high) / 2);
        if ((s[middle] == key)) {
            return middle;
        }
        if ((s[middle] > key)) {
            return binary_search(s, key, low, (middle - 1));
        } else {
            return binary_search(s, key, (middle + 1), high);
        }
    }

    public static void merge(int[] s, int low, int middle, int high) {
        int i = 0; /* counter */
        Queue.queue buffer1 = new Queue.queue(); /* buffers to hold elements for merging */
        Queue.queue buffer2 = new Queue.queue();
        Queue.init_queue(buffer1);
        Queue.init_queue(buffer2);
        for (i = low; (i <= middle); i++) {
            Queue.enqueue(buffer1, s[i]);
        }
        for (i = (middle + 1); (i <= high); i++) {
            Queue.enqueue(buffer2, s[i]);
        }
        i = low;
        while (!(((Queue.empty_queue(buffer1) != 0) || (Queue.empty_queue(buffer2) != 0)))) {
            if ((Queue.headq(buffer1) <= Queue.headq(buffer2))) {
                s[i++] = Queue.dequeue(buffer1);
            } else {
                s[i++] = Queue.dequeue(buffer2);
            }
        }
        while (!((Queue.empty_queue(buffer1) != 0))) {
            s[i++] = Queue.dequeue(buffer1);
        }
        while (!((Queue.empty_queue(buffer2) != 0))) {
            s[i++] = Queue.dequeue(buffer2);
        }
    }

    public static void merge_sort(int[] s, int low, int high) {
        int middle = 0; /* index of middle element */
        if ((low < high)) {
            middle = ((low + high) / 2);
            merge_sort(s, low, middle);
            merge_sort(s, (middle + 1), high);
            merge(s, low, middle, high);
        }
    }

    public static int main() {
        int[] s = new int[(NELEM + 2)];
        int i = 0; /* counter */
        for (i = 0; (i < NELEM); i++) {
            s[i] = (NELEM - i);
        }
        Random.random_permutation(s, NELEM);
        insertion_sort(s, NELEM);
        System.out.print("\n\nInsertion sort: \n");
        for (i = 0; (i < NELEM); i++) {
            System.out.printf(Locale.US, "%d ", s[i]);
        }
        for (i = 0; (i < NELEM); i++) {
            s[i] = (NELEM - i);
        }
        Random.random_permutation(s, NELEM);
        selection_sort(s, NELEM);
        System.out.print("\n\nSelection sort: \n");
        for (i = 0; (i < NELEM); i++) {
            System.out.printf(Locale.US, "%d ", s[i]);
        }
        for (i = 0; (i < NELEM); i++) {
            s[i] = (NELEM - i);
        }
        Random.random_permutation(s, NELEM);
        quicksort(s, 0, (NELEM - 1));
        System.out.print("\n\nQuicksort: \n");
        for (i = 0; (i < NELEM); i++) {
            System.out.printf(Locale.US, "%d ", s[i]);
        }
        for (i = 0; (i < NELEM); i++) {
            s[i] = (NELEM - i);
        }
        Random.random_permutation(s, NELEM);
        heapsort_(s, NELEM);
        System.out.print("\n\nHeapsort sort: \n");
        for (i = 0; (i < NELEM); i++) {
            System.out.printf(Locale.US, "%d ", s[i]);
        }
        for (i = 0; (i < NELEM); i++) {
            s[i] = (NELEM - i);
        }
        Random.random_permutation(s, NELEM);
        merge_sort(s, 0, (NELEM - 1));
        System.out.print("\n\nMergesort: \n");
        for (i = 0; (i < NELEM); i++) {
            System.out.printf(Locale.US, "%d ", s[i]);
        }
        System.out.print("\n");
        System.out.print("\n");
        /* test binary search */
        System.out.print("Binary Search: \n");
        for (i = 0; (i < NELEM); i++) {
            s[i] = (2 * (NELEM - i));
        }
        Random.random_permutation(s, NELEM);
        heapsort_(s, NELEM);
        for (i = 2; (i < ((2 * NELEM) + 1)); i += 2) {
            System.out.printf(Locale.US, "%d found in %d\n", i, binary_search(s, i, 0, (NELEM - 1)));
        }
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
