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

import java.util.NoSuchElementException;

public final class Queue<T> {
    static final class Link<T> {
        final T value;
        Link<T> next;
        Link(T value) {
            this.value = value;
        }
    }

    private Link<T> first;
    private Link<T> last;
    private int size;
    public int size() {
        return size;
    }
    public boolean isEmpty() {
        return size == 0;
    }
    public void add(T value) {
        Link<T> node = new Link<>(value);
        if (last == null) {
            first = node;
        } else {
            last.next = node;
        }
        last = node;
        size++;
    }
    public T remove() {
        if (first == null) {
            throw new NoSuchElementException("empty queue");
        }
        T value = first.value;
        first = first.next;
        if (first == null) {
            last = null;
        }
        size--;
        return value;
    }
}
