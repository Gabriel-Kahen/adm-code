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
template <class T> class Queue {
    std::deque<T> values_;

  public:
    void push(T value) {
        values_.push_back(std::move(value));
    }
    T pop() {
        require(!empty(), "empty queue");
        T value = std::move(values_.front());
        values_.pop_front();
        return value;
    }
    bool empty() const {
        return values_.empty();
    }
    std::size_t size() const {
        return values_.size();
    }
};
} // namespace adm
