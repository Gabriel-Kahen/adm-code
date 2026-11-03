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
#include "priority_queue.hpp"

namespace adm {
void MinHeap::push(Integer value) {
    values_.push_back(value);
    std::size_t child = values_.size() - 1;
    while (child > 0) {
        std::size_t parent = (child - 1) / 2;
        if (values_[parent] <= values_[child]) {
            break;
        }
        std::swap(values_[parent], values_[child]);
        child = parent;
    }
}

Integer MinHeap::pop() {
    require(!empty(), "empty heap");
    Integer result = values_.front();
    values_.front() = values_.back();
    values_.pop_back();
    std::size_t parent = 0;
    while (2 * parent + 1 < values_.size()) {
        std::size_t child = 2 * parent + 1;
        if (child + 1 < values_.size() && values_[child + 1] < values_[child]) {
            ++child;
        }
        if (values_[parent] <= values_[child]) {
            break;
        }
        std::swap(values_[parent], values_[child]);
        parent = child;
    }
    return result;
}
} // namespace adm
