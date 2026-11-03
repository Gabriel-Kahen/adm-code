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
BigInteger fibonacci(const std::string &method, int n) {
    require(n >= 0, "negative Fibonacci index");
    if (method == "recursive") {
        require(n <= 35, "recursive Fibonacci limited to index 35");
        if (n < 2) {
            return BigInteger(n);
        }
        return fibonacci(method, n - 1) + fibonacci(method, n - 2);
    }
    if (method == "memo") {
        std::vector<std::optional<BigInteger>> cache(static_cast<std::size_t>(n) + 2);
        cache[0] = BigInteger(0);
        cache[1] = BigInteger(1);
        std::function<BigInteger(int)> solve = [&](int index) {
            if (!cache[index]) {
                cache[index] = solve(index - 1) + solve(index - 2);
            }
            return *cache[index];
        };
        return solve(n);
    }
    if (method == "table") {
        std::vector<BigInteger> values(static_cast<std::size_t>(n) + 2);
        values[1] = BigInteger(1);
        for (int i = 2; i <= n; ++i) {
            values[i] = values[i - 1] + values[i - 2];
        }
        return values[n];
    }
    require(method == "constant", "unknown Fibonacci method");
    BigInteger previous(0), current(1);
    for (int i = 0; i < n; ++i) {
        BigInteger next = previous + current;
        previous = current;
        current = next;
    }
    return previous;
}
} // namespace adm

#ifdef ADM_DEMO
int main() {
    using namespace adm;
    try {
        int n = 10;
        std::cin >> n;
        std::cout << fibonacci("table", n).str() << "\n";
    } catch (const std::exception &error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
}
#endif
