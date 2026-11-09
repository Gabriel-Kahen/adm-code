/*    tree-demo.c

    Driver for a binary search tree container implementation.
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

public class TreeDemo {
    public static class tree {
        int item = 0; /* data item */
        TreeDemo.tree parent = null; /* pointer to parent */
        TreeDemo.tree left = null; /* pointer to left child */
        TreeDemo.tree right = null; /* pointer to right child */
    }
    public static TreeDemo.tree parent = null; /* last node visited */

    public static TreeDemo.tree init_tree() {
        return null;
    }

    public static boolean empty_tree(TreeDemo.tree t) {
        if ((t == null)) {
            return true;
        }
        return false;
    }

    public static TreeDemo.tree search_tree(TreeDemo.tree l, int x) {
        if ((l == null)) {
            return null;
        }
        if ((l.item == x)) {
            return l;
        }
        if ((x < l.item)) {
            return search_tree(l.left, x);
        } else {
            return search_tree(l.right, x);
        }
    }

    public static tree insert_tree(tree l, int x, tree parent) {
        tree p; /* temporary pointer */
        if (l == null) {
            p = new tree();
            p.item = x;
            p.left = p.right = null;
            p.parent = parent;
            return p;
        }
        if (x < l.item) {
            l.left = insert_tree(l.left, x, l);
        } else {
            l.right = insert_tree(l.right, x, l);
        }
        return l;
    }

    public static void print_tree(TreeDemo.tree l) {
        if ((l != null)) {
            print_tree(l.left);
            System.out.printf(Locale.US, "%d ", l.item);
            print_tree(l.right);
        }
    }

    public static TreeDemo.tree successor_descendant(TreeDemo.tree t) {
        TreeDemo.tree succ = null; /* successor pointer */
        if ((t.right == null)) {
            return null;
        }
        succ = t.right;
        while ((succ.left != null)) {
            succ = succ.left;
        }
        return succ;
    }

    public static TreeDemo.tree find_minimum(TreeDemo.tree t) {
        TreeDemo.tree min = null; /* pointer to minimum */
        if ((t == null)) {
            return null;
        }
        min = t;
        while ((min.left != null)) {
            min = min.left;
        }
        return min;
    }

    public static TreeDemo.tree predecessor_descendant(TreeDemo.tree t) {
        TreeDemo.tree pred = null; /* predecessor pointer */
        if ((t.left == null)) {
            return null;
        }
        pred = t.left;
        while ((pred.right != null)) {
            pred = pred.right;
        }
        return pred;
    }

    public static TreeDemo.tree delete_tree(TreeDemo.tree t, int x) {
        TreeDemo.tree target = search_tree(t, x);
        /* Detach a node by identity: equal keys need not identify the same node.
               The successor of a two-child node has at most one child. */
        TreeDemo.tree removed = null;
        TreeDemo.tree child = null;
        if ((target == null)) {
            System.out.printf(Locale.US, "Warning: key to be deleted %d is not in tree.\n", x);
            return t;
        }
        removed = (((target.left != null) && (target.right != null)) ? successor_descendant(target) : target);
        child = ((removed.left != null) ? removed.left : removed.right);
        if ((removed.parent == null)) {
            t = child;
        } else {
            if ((removed.parent.left == removed)) {
                removed.parent.left = child;
            } else {
                removed.parent.right = child;
            }
        }
        if ((child != null)) {
            child.parent = removed.parent;
        }
        if ((removed != target)) {
            target.item = removed.item;
        }
        // Java garbage collection releases removed;
        return t;
    }

    public static void process_item(int x) {
        System.out.printf(Locale.US, "%d", x);
    }

    public static void traverse_tree(TreeDemo.tree l) {
        if ((l != null)) {
            traverse_tree(l.left);
            process_item(l.item);
            traverse_tree(l.right);
        }
    }

    public static int main() {
        char c = '\000'; /* input character */
        int d = 0; /* input item */
        TreeDemo.tree l = null; /* tree under construction */
        TreeDemo.tree tmp = null; /* returned tree from search */
        l = init_tree();
        while (true) {
            int _read0 = C.scan("%c");
            if (_read0 > 0) c = (char)C.scanInt(0);
            if (_read0 == -1) break;
            if ((Character.toLowerCase(c) == 'p')) {
                print_tree(l);
                System.out.print("\n");
            }
            if ((Character.toLowerCase(c) == 'i')) {
                int _read1 = C.scan("%d");
                if (_read1 > 0) d = C.scanInt(0);
                System.out.printf(Locale.US, "new item: %d\n", d);
                l = insert_tree(l, d, null);
            }
            if ((Character.toLowerCase(c) == 's')) {
                int _read2 = C.scan("%d");
                if (_read2 > 0) d = C.scanInt(0);
                tmp = search_tree(l, d);
                if ((tmp == null)) {
                    System.out.printf(Locale.US, "item %d not found\n", d);
                } else {
                    System.out.printf(Locale.US, "item %d found\n", d);
                }
            }
            if ((Character.toLowerCase(c) == 'd')) {
                int _read3 = C.scan("%d");
                if (_read3 > 0) d = C.scanInt(0);
                System.out.printf(Locale.US, " deleting item %d\n", d);
                l = delete_tree(l, d);
                print_tree(l);
                System.out.print("\n");
            }
        }
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
