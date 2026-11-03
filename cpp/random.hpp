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
class Random {
    std::mt19937_64 engine_;

  public:
    explicit Random(std::uint64_t seed) : engine_(seed) {}
    Integer integer(Integer low, Integer high);
    double real(double low, double high);
    template <class T> void shuffle(std::vector<T> &values) {
        for (std::size_t remaining = values.size(); remaining > 1; --remaining) {
            auto choice = static_cast<std::size_t>(integer(0, static_cast<Integer>(remaining - 1)));
            std::swap(values[remaining - 1], values[choice]);
        }
    }
};
} // namespace adm
