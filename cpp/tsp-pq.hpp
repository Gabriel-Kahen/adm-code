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
template <class State, class Compare> class TourQueue {
    std::priority_queue<State, std::vector<State>, Compare> values_;

  public:
    explicit TourQueue(Compare compare) : values_(compare) {}
    bool empty() const {
        return values_.empty();
    }
    std::size_t size() const {
        return values_.size();
    }
    const State &top() const {
        require(!empty(), "empty tour queue");
        return values_.top();
    }
    void pop() {
        require(!empty(), "empty tour queue");
        values_.pop();
    }
    void push(State state) {
        require(size() < 1000000, "TSP best-first frontier exhausted");
        values_.push(std::move(state));
    }
};
} // namespace adm
