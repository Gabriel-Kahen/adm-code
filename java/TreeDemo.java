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

public final class TreeDemo {

    static final class Node {
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

    public static void main(String[] args) {
        TreeDemo tree = new TreeDemo();
        tree.insert(3);
        tree.insert(1);
        tree.insert(2);
        tree.delete(3);
        System.out.println(tree.values());
    }
}
