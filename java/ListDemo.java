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

public final class ListDemo {
    static final class Link<T> {
        final T value;
        Link<T> next;
        Link(T value) {
            this.value = value;
        }
    }

    private Link<Long> head;
    public void insert(long value) {
        Link<Long> node = new Link<>(value);
        node.next = head;
        head = node;
    }
    public boolean contains(long value) {
        for (Link<Long> node = head; node != null; node = node.next) {
            if (node.value == value) {
                return true;
            }
        }
        return false;
    }
    public boolean delete(long value) {
        Link<Long> previous = null;
        for (Link<Long> node = head; node != null; node = node.next) {
            if (node.value == value) {
                if (previous == null) {
                    head = node.next;
                } else {
                    previous.next = node.next;
                }
                return true;
            }
            previous = node;
        }
        return false;
    }
    public List<Long> values() {
        List<Long> result = new ArrayList<>();
        for (Link<Long> node = head; node != null; node = node.next) {
            result.add(node.value);
        }
        return result;
    }

    public static void main(String[] args) {
        ListDemo list = new ListDemo();
        list.insert(2);
        list.insert(1);
        list.delete(2);
        System.out.println(list.values());
    }
}
