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
std::array<Integer, 3> extended_gcd(Integer a, Integer b) {
    require(a != std::numeric_limits<Integer>::min() && b != std::numeric_limits<Integer>::min(),
            "GCD magnitude exceeds signed64");
    Integer old_r = std::abs(a), r = std::abs(b), old_x = 1, x = 0, old_y = 0, y = 1;
    while (r != 0) {
        Integer q = old_r / r;
        Integer next_r = old_r % r;
        Integer next_x = subtract(old_x, multiply(q, x));
        Integer next_y = subtract(old_y, multiply(q, y));
        old_r = r;
        r = next_r;
        old_x = x;
        x = next_x;
        old_y = y;
        y = next_y;
    }
    return {old_r, a < 0 ? -old_x : old_x, b < 0 ? -old_y : old_y};
}
} // namespace adm

#ifdef ADM_DEMO
int main() {
    using namespace adm;
    try {
        Integer a = 252, b = 198;
        std::cin >> a >> b;
        for (auto value : extended_gcd(a, b)) {
            std::cout << value << " ";
        }
        std::cout << "\n";
    } catch (const std::exception &error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
}
#endif
