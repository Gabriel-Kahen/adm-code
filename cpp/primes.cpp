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
Integers prime_factors(Integer n) {
    require(n >= 1, "factorization requires positive integer");
    Integers factors;
    for (Integer divisor = 2; divisor <= n / divisor; divisor += divisor == 2 ? 1 : 2) {
        while (n % divisor == 0) {
            factors.push_back(divisor);
            n /= divisor;
        }
    }
    if (n > 1) {
        factors.push_back(n);
    }
    return factors;
}
} // namespace adm

#ifdef ADM_DEMO
int main() {
    using namespace adm;
    try {
        Integer n = 360;
        std::cin >> n;
        for (auto value : prime_factors(n)) {
            std::cout << value << " ";
        }
        std::cout << "\n";
    } catch (const std::exception &error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
}
#endif
