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
#include "backtrack.hpp"

namespace adm {
Groups permutations(int n) {
    require(n >= 0 && n <= 10, "permutation enumeration requires 0 <= n <= 10");
    Groups result;
    std::vector<int> prefix;
    std::vector<bool> used(n);
    backtrack(
        prefix, [n](const auto &path) { return static_cast<int>(path.size()) == n; },
        [&](const auto &) {
            std::vector<int> choices;
            for (int i = 0; i < n; ++i) {
                if (!used[i]) {
                    choices.push_back(i);
                }
            }
            return choices;
        },
        [&](int value) { used[value] = true; }, [&](int value) { used[value] = false; },
        [&](const auto &path) {
            result.push_back(path);
            return false;
        });
    return result;
}
} // namespace adm

#ifdef ADM_DEMO
int main() {
    using namespace adm;
    try {
        int n = 3;
        std::cin >> n;
        for (auto row : permutations(n)) {
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
