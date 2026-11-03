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
#include "list.hpp"

namespace adm {
void LinkedList::insert(Integer value) {
    auto node = std::make_unique<Node>(value);
    node->next = std::move(head_);
    head_ = std::move(node);
}

bool LinkedList::contains(Integer value) const {
    for (Node *node = head_.get(); node; node = node->next.get()) {
        if (node->value == value) {
            return true;
        }
    }
    return false;
}

bool LinkedList::erase(Integer value) {
    auto *link = &head_;
    while (*link && (*link)->value != value) {
        link = &(*link)->next;
    }
    if (!*link) {
        return false;
    }
    auto removed = std::move(*link);
    *link = std::move(removed->next);
    return true;
}

Integers LinkedList::values() const {
    Integers result;
    for (Node *node = head_.get(); node; node = node->next.get()) {
        result.push_back(node->value);
    }
    return result;
}
} // namespace adm

#ifdef ADM_DEMO
int main() {
    using namespace adm;
    try {
        LinkedList list;
        list.insert(2);
        list.insert(1);
        list.erase(2);
        for (auto value : list.values()) {
            std::cout << value << " ";
        }
        std::cout << "\n";
    } catch (const std::exception &error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
}
#endif
