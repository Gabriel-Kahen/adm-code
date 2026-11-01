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
import java.util.List;
import java.util.NoSuchElementException;

/** Small, unbounded containers. Empty removals throw NoSuchElementException. */
public final class Containers {
    private Containers() {}

    private static final class Link<T> {
        final T value;
        Link<T> next;
        Link(T value) {
            this.value = value;
        }
    }

    /** FIFO with O(1) enqueue/dequeue. Null values are permitted. */
    public static final class Queue<T> {
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

    /** LIFO with amortized O(1) push/pop. */
    public static final class Stack<T> {
        private final List<T> values = new ArrayList<>();
        public int size() {
            return values.size();
        }
        public boolean isEmpty() {
            return values.isEmpty();
        }
        public void push(T value) {
            values.add(value);
        }
        public T pop() {
            if (values.isEmpty()) {
                throw new NoSuchElementException("empty stack");
            }
            return values.remove(values.size() - 1);
        }
    }

    /** Binary minimum heap: O(log n) add/remove, O(1) minimum. */
    public static final class MinHeap {
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

    /** Union by size and path compression, amortized inverse-Ackermann operations. */
    public static final class DisjointSet {
        private final int[] parent;
        private final int[] size;
        public DisjointSet(int n) {
            if (n < 0) {
                throw new IllegalArgumentException("negative set size");
            }
            parent = new int[n];
            size = new int[n];
            for (int i = 0; i < n; i++) {
                parent[i] = i;
                size[i] = 1;
            }
        }
        public int find(int x) {
            if (x < 0 || x >= parent.length) {
                throw new IllegalArgumentException("invalid element");
            }
            int root = x;
            while (root != parent[root]) {
                root = parent[root];
            }
            while (x != root) {
                int next = parent[x];
                parent[x] = root;
                x = next;
            }
            return root;
        }
        public boolean union(int a, int b) {
            a = find(a);
            b = find(b);
            if (a == b) {
                return false;
            }
            if (size[a] < size[b]) {
                int swap = a;
                a = b;
                b = swap;
            }
            parent[b] = a;
            size[a] += size[b];
            return true;
        }
        public int size(int x) {
            return size[find(x)];
        }
    }

    /** Singly linked list; insertion at front, deletion removes the first equal value. */
    public static final class LinkedList {
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
    }

    /** Unbalanced binary search SET; duplicate insertions have no effect. O(height) updates. */
    public static final class BinarySearchTree {
        private static final class Node {
            long value;
            Node left;
            Node right;
            Node(long value) {
                this.value = value;
            }
        }
        private Node root;
        public boolean contains(long value) {
            Node node = root;
            while (node != null) {
                if (value == node.value) {
                    return true;
                }
                node = value < node.value ? node.left : node.right;
            }
            return false;
        }
        public void insert(long value) {
            root = insert(root, value);
        }
        private Node insert(Node node, long value) {
            if (node == null) {
                return new Node(value);
            }
            if (value < node.value) {
                node.left = insert(node.left, value);
            } else if (value > node.value) {
                node.right = insert(node.right, value);
            }
            return node;
        }
        public void delete(long value) {
            root = delete(root, value);
        }
        private Node delete(Node node, long value) {
            if (node == null) {
                return null;
            }
            if (value < node.value) {
                node.left = delete(node.left, value);
            } else if (value > node.value) {
                node.right = delete(node.right, value);
            } else {
                if (node.left == null) {
                    return node.right;
                }
                if (node.right == null) {
                    return node.left;
                }
                Node successor = node.right;
                while (successor.left != null) {
                    successor = successor.left;
                }
                node.value = successor.value;
                node.right = delete(node.right, successor.value);
            }
            return node;
        }
        public List<Long> values() {
            List<Long> result = new ArrayList<>();
            inorder(root, result);
            return result;
        }
        private void inorder(Node node, List<Long> result) {
            if (node == null) {
                return;
            }
            inorder(node.left, result);
            result.add(node.value);
            inorder(node.right, result);
        }
    }
}
