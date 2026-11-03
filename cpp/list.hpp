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

#pragma once

#include "item.hpp"

namespace adm {
class LinkedList {
    struct Node {
        Integer value;
        std::unique_ptr<Node> next;
        explicit Node(Integer value) : value(value) {}
    };
    std::unique_ptr<Node> head_;

  public:
    // Insert at head; duplicates allowed. Erase removes the first occurrence.
    void insert(Integer value);
    bool contains(Integer value) const;
    bool erase(Integer value);
    Integers values() const;
};
} // namespace adm
