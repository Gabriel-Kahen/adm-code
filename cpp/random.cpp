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
#include "random.hpp"

namespace adm {
Integer Random::integer(Integer low, Integer high) {
    require(low <= high, "invalid integer random interval");
    return std::uniform_int_distribution<Integer>(low, high)(engine_);
}

double Random::real(double low, double high) {
    require(std::isfinite(low) && std::isfinite(high) && low <= high,
            "invalid real random interval");
    if (low == high) {
        return low;
    }
    require(std::isfinite(high - low), "real random interval width overflow");
    return std::uniform_real_distribution<double>(low, high)(engine_);
}
} // namespace adm
