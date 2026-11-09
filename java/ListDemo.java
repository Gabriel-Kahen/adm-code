/*	list-demo.c

	Driver for a linked list-based container implementation.
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

public class ListDemo {
    public static class list {
        int item = 0; /* data item */
        ListDemo.list next = null; /* point to successor */
    }

    public static ListDemo.list init_list() {
        return null;
    }

    public static boolean empty_list(ListDemo.list l) {
        if ((l == null)) {
            return true;
        } else {
            return false;
        }
    }

    public static ListDemo.list search_list(ListDemo.list l, int x) {
        if ((l == null)) {
            return null;
        }
        if ((l.item == x)) {
            return l;
        } else {
            return search_list(l.next, x);
        }
    }

    public static ListDemo.list item_ahead(ListDemo.list l, ListDemo.list x) {
        if (((l == null) || (l.next == null))) {
            return null;
        }
        if ((l.next == x)) {
            return l;
        } else {
            return item_ahead(l.next, x);
        }
    }

    public static list insert_list(list l, int x) {
        list p = new list(); /* temporary pointer */
        p.item = x;
        p.next = l;
        return p;
    }

    public static void print_list(ListDemo.list l) {
        while ((l != null)) {
            C.printf("%d ", l.item);
            l = l.next;
        }
        C.printf("\n");
    }

    public static list delete_list(list l, list x) {
        list p = l; /* item pointer */
        list pred = item_ahead(l, x); /* predecessor pointer */
        if (pred == null) { /* splice out of list */
            l = p.next;
        } else {
            pred.next = x.next;
        }
        return l;
    }

    public static int main() {
        char c = '\000'; /* input character */
        int d = 0; /* input item */
        ListDemo.list l = null; /* list under construction */
        ListDemo.list tmp = null; /* returned list from search */
        l = init_list();
        while (true) {
            int _read0 = C.scan("%c");
            if (_read0 > 0) c = (char)C.scanInt(0);
            if (!((_read0 != -1))) break;
            if ((Character.toLowerCase(c) == 'p')) {
                print_list(l);
            }
            if ((Character.toLowerCase(c) == 'i')) {
                int _read1 = C.scan("%d");
                if (_read1 > 0) d = C.scanInt(0);
                C.printf("new item: %d\n", d);
                l = insert_list(l, d);
            }
            if ((Character.toLowerCase(c) == 's')) {
                int _read2 = C.scan("%d");
                if (_read2 > 0) d = C.scanInt(0);
                tmp = search_list(l, d);
                if ((tmp == null)) {
                    C.printf("item %d not found\n", d);
                } else {
                    C.printf("item %d found\n", d);
                }
            }
            if ((Character.toLowerCase(c) == 'd')) {
                int _read3 = C.scan("%d");
                if (_read3 > 0) d = C.scanInt(0);
                tmp = search_list(l, d);
                if ((tmp == null)) {
                    C.printf("item to delete %d not found\n", d);
                } else {
                    l = delete_list(l, tmp);
                    C.printf("item %d deleted\n", d);
                }
            }
        }
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
