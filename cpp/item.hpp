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

#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <deque>
#include <functional>
#include <iomanip>
#include <iostream>
#include <limits>
#include <memory>
#include <numeric>
#include <optional>
#include <queue>
#include <random>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

namespace adm {
using Integer = long long;
using Integers = std::vector<Integer>;
using Matrix = std::vector<Integers>;
inline void require(bool condition, const std::string &message) {
    if (!condition) {
        throw std::invalid_argument(message);
    }
}
inline Integer add(Integer a, Integer b) {
    Integer result;
    if (__builtin_add_overflow(a, b, &result)) {
        throw std::overflow_error("integer addition overflow");
    }
    return result;
}
inline Integer subtract(Integer a, Integer b) {
    Integer result;
    if (__builtin_sub_overflow(a, b, &result)) {
        throw std::overflow_error("integer subtraction overflow");
    }
    return result;
}
inline Integer multiply(Integer a, Integer b) {
    Integer result;
    if (__builtin_mul_overflow(a, b, &result)) {
        throw std::overflow_error("integer multiplication overflow");
    }
    return result;
}
} // namespace adm
