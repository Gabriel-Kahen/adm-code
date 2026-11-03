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
#include "graph.hpp"

namespace adm {
Groups subsets(int n) {
    require(n >= 0 && n <= 20, "subset enumeration requires 0 <= n <= 20");
    Groups result{{}};
    for (int value = 0; value < n; ++value) {
        auto size = result.size();
        for (std::size_t i = 0; i < size; ++i) {
            auto next = result[i];
            next.push_back(value);
            result.push_back(std::move(next));
        }
    }
    std::sort(result.begin(), result.end());
    return result;
}
} // namespace adm

#ifdef ADM_DEMO
int main() {
    using namespace adm;
    try {
        int n = 3;
        std::cin >> n;
        for (auto row : subsets(n)) {
            for (auto value : row) {
                std::cout << value << " ";
            }
            std::cout << "\n";
        }
    } catch (const std::exception &error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
}
#endif
