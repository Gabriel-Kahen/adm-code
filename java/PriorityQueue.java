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
import java.util.List;
import java.util.NoSuchElementException;

public final class PriorityQueue {

    private final List<Long> values = new ArrayList<>();
    public int size() {
        return values.size();
    }
    public boolean isEmpty() {
        return values.isEmpty();
    }
    public long minimum() {
        if (values.isEmpty()) {
            throw new NoSuchElementException("empty heap");
        }
        return values.get(0);
    }
    public void add(long value) {
        values.add(value);
        int child = values.size() - 1;
        while (child > 0) {
            int parent = (child - 1) / 2;
            if (values.get(parent) <= value) {
                break;
            }
            values.set(child, values.get(parent));
            child = parent;
        }
        values.set(child, value);
    }
    public long remove() {
        long result = minimum();
        long last = values.remove(values.size() - 1);
        if (values.isEmpty()) {
            return result;
        }
        int parent = 0;
        while (2L * parent + 1 < values.size()) {
            int child = 2 * parent + 1;
            if (child + 1 < values.size() && values.get(child + 1) < values.get(child)) {
                child++;
            }
            if (last <= values.get(child)) {
                break;
            }
            values.set(parent, values.get(child));
            parent = child;
        }
        values.set(parent, last);
        return result;
    }
}
