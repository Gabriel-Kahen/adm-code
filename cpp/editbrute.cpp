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
#include "editbrute.hpp"
#include "distance.hpp"

namespace adm {
Integer brute_edit_distance(const std::string &a, const std::string &b) {
    require(a.size() + b.size() <= 16, "brute-force edit distance limited to combined length 16");
    std::function<Integer(std::size_t, std::size_t)> solve = [&](std::size_t i,
                                                                 std::size_t j) -> Integer {
        if (i == 0) {
            return static_cast<Integer>(j);
        }
        if (j == 0) {
            return static_cast<Integer>(i);
        }
        return std::min({solve(i - 1, j - 1) + (a[i - 1] != b[j - 1]), solve(i - 1, j) + 1,
                         solve(i, j - 1) + 1});
    };
    return solve(a.size(), b.size());
}
} // namespace adm

#ifdef ADM_DEMO
int main() {
    using namespace adm;
    try {
        std::string a = "cat", b = "cut";
        std::cin >> a >> b;
        std::cout << brute_edit_distance(a, b) << "\n";
    } catch (const std::exception &error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
}
#endif
