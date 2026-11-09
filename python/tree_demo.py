# Copyright 2003-2020 by Steven S. Skiena; all rights reserved.
# Permission is granted for use in non-commerical applications
# provided this copyright notice remains intact and unchanged.
#
# These programs appear in my books:
#
# "The Algorithm Design Manual" by Steven Skiena, second edition, Springer,
# London 2008.  See out website www.algorist.com for additional information
# or https://www.amazon.com/exec/obidos/ASIN/1848000693/thealgorith01-20
#
# "Programming Challenges: The Programming Contest Training Manual"
# by Steven Skiena and Miguel Revilla, Springer-Verlag, New York 2003.
# See our website www.programming-challenges.com for additional information,
# or https://www.amazon.com/exec/obidos/ASIN/0387001638/thealgorithmrepo/

"""Direct translation of tree-demo.c; data structures and indexing match C."""

if __name__ == "__main__" and not __package__:
    import sys
    from pathlib import Path
    sys.path[0] = str(Path(__file__).resolve().parent.parent)
    __package__ = "python"
    sys.modules[__package__ + "." + Path(__file__).stem] = sys.modules[__name__]

from ._c import EOF, address, printf, scanf

class tree:
    def __init__(self):
        # item: data item
        self.item = 0
        # parent: pointer to parent
        self.parent = None
        # left: pointer to left child
        self.left = None
        # right: pointer to right child
        self.right = None


# parent: last node visited
parent = None


def init_tree():
    return None


def empty_tree(t):
    if (t == None):
        return True
    return False


def search_tree(l, x):
    if (l == None):
        return None
    if (l.item == x):
        return l
    if (x < l.item):
        return search_tree(l.left, x)
    else:
        return search_tree(l.right, x)


def insert_tree(l, x, parent):
    # p: temporary pointer
    if (l[0] == None):
        p = tree()
        p.item = x
        p.right = None
        p.left = p.right
        p.parent = parent
        l[0] = p
        return
    if (x < l[0].item):
        insert_tree(address(l[0], 'left'), x, l[0])
    else:
        insert_tree(address(l[0], 'right'), x, l[0])


def print_tree(l):
    if (l != None):
        print_tree(l.left)
        printf("%d ", l.item)
        print_tree(l.right)


def successor_descendant(t):
    # succ: successor pointer
    if (t.right == None):
        return None
    succ = t.right
    while (succ.left != None):
        succ = succ.left
    return succ


def find_minimum(t):
    # min: pointer to minimum
    if (t == None):
        return None
    min = t
    while (min.left != None):
        min = min.left
    return min


def predecessor_descendant(t):
    # pred: predecessor pointer
    if (t.left == None):
        return None
    pred = t.left
    while (pred.right != None):
        pred = pred.right
    return pred


def delete_tree(t, x):
    target = search_tree(t, x)
    if (target == None):
        printf("Warning: key to be deleted %d is not in tree.\n", x)
        return t
    # Detach a node by identity: equal keys need not identify the same node.
    # The successor of a two-child node has at most one child.
    removed = (successor_descendant(target) if ((target.left != None) and (target.right != None)) else target)
    child = (removed.left if (removed.left != None) else removed.right)
    if (removed.parent == None):
        t = child
    else:
        if (removed.parent.left == removed):
            removed.parent.left = child
        else:
            removed.parent.right = child
    if (child != None):
        child.parent = removed.parent
    if (removed != target):
        target.item = removed.item
    # Python releases this node when its references disappear.
    return t


def process_item(x):
    printf("%d", x)


def traverse_tree(l):
    if (l != None):
        traverse_tree(l.left)
        process_item(l.item)
        traverse_tree(l.right)


def main():
    # c: input character
    c = [0]
    # d: input item
    d = [0]
    # l: tree under construction
    l = [None]
    # tmp: returned tree from search
    l[0] = init_tree()
    while (scanf("%c", c) != EOF):
        if (chr(c[0]).lower() == 'p'):
            print_tree(l[0])
            printf("\n")
        if (chr(c[0]).lower() == 'i'):
            scanf("%d", d)
            printf("new item: %d\n", d[0])
            insert_tree(l, d[0], None)
        if (chr(c[0]).lower() == 's'):
            scanf("%d", d)
            tmp = search_tree(l[0], d[0])
            if (tmp == None):
                printf("item %d not found\n", d[0])
            else:
                printf("item %d found\n", d[0])
        if (chr(c[0]).lower() == 'd'):
            scanf("%d", d)
            printf(" deleting item %d\n", d[0])
            l[0] = delete_tree(l[0], d[0])
            print_tree(l[0])
            printf("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
