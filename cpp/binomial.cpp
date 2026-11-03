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
#include "bignum.hpp"

namespace adm {
BigInteger binomial(int n, int k) {
    require(n >= 0 && k >= 0 && k <= n, "invalid binomial indices");
    k = std::min(k, n - k);
    if (k == 0) {
        return BigInteger(1);
    }
    std::vector<BigInteger> row(static_cast<std::size_t>(k) + 1);
    row[0] = BigInteger(1);
    for (Integer level = 1; level <= n; ++level) {
        for (int column = std::min(static_cast<int>(level), k); column > 0; --column) {
            row[column] = row[column] + row[column - 1];
        }
    }
    return row[k];
}
} // namespace adm

#ifdef ADM_DEMO
int main() {
    using namespace adm;
    try {
        int n = 10, k = 5;
        std::cin >> n >> k;
        std::cout << binomial(n, k).str() << "\n";
    } catch (const std::exception &error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
}
#endif
