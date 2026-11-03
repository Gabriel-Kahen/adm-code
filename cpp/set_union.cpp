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

#include "item.hpp"
#include "set_union.hpp"

namespace adm {
DisjointSet::DisjointSet(int n) {
    require(n >= 0, "negative set count");
    parent_.resize(n);
    size_.assign(n, 1);
    std::iota(parent_.begin(), parent_.end(), 0);
}

int DisjointSet::find(int vertex) {
    require(vertex >= 0 && static_cast<std::size_t>(vertex) < parent_.size(), "invalid set index");
    int root = vertex;
    while (parent_[root] != root) {
        root = parent_[root];
    }
    while (vertex != root) {
        int next = parent_[vertex];
        parent_[vertex] = root;
        vertex = next;
    }
    return root;
}

bool DisjointSet::unite(int a, int b) {
    a = find(a);
    b = find(b);
    if (a == b) {
        return false;
    }
    if (size_[a] < size_[b]) {
        std::swap(a, b);
    }
    parent_[b] = a;
    size_[a] += size_[b];
    return true;
}
} // namespace adm
