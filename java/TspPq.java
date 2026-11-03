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

import java.util.Comparator;

public final class TspPq<T> {

    private final java.util.PriorityQueue<T> values;
    private final int capacity;
    public TspPq(java.util.Comparator<T> compare, int capacity) {
        if (capacity < 1) {
            throw new IllegalArgumentException("capacity must be positive");
        }
        this.capacity = capacity;
        values = new java.util.PriorityQueue<>(compare);
    }
    public boolean isEmpty() {
        return values.isEmpty();
    }
    public int size() {
        return values.size();
    }
    public void add(T value) {
        if (size() >= capacity) {
            throw new IllegalStateException("TSP best-first frontier exhausted");
        }
        values.add(value);
    }
    public T remove() {
        return values.remove();
    }
}
