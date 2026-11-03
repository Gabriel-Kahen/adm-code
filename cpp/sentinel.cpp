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

namespace adm {
Integers sentinel_insert(Integers sorted, Integer value) {
    require(std::is_sorted(sorted.begin(), sorted.end()), "insertion requires sorted input");
    // A boundary guard is safer than reserving a magic finite sentinel value.
    sorted.push_back(value);
    std::size_t position = sorted.size() - 1;
    while (position > 0 && sorted[position - 1] > value) {
        sorted[position] = sorted[position - 1];
        --position;
    }
    sorted[position] = value;
    return sorted;
}
} // namespace adm

#ifdef ADM_DEMO
int main() {
    using namespace adm;
    try {
        for (auto value : sentinel_insert({1, 2, 3}, -1)) {
            std::cout << value << " ";
        }
        std::cout << "\n";
    } catch (const std::exception &error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
}
#endif
