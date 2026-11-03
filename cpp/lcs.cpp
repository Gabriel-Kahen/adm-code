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
std::string longest_common_subsequence(const std::string &a, const std::string &b) {
    Matrix length(a.size() + 1, Integers(b.size() + 1));
    for (std::size_t i = 1; i <= a.size(); ++i) {
        for (std::size_t j = 1; j <= b.size(); ++j) {
            length[i][j] = a[i - 1] == b[j - 1] ? length[i - 1][j - 1] + 1
                                                : std::max(length[i - 1][j], length[i][j - 1]);
        }
    }
    std::string result;
    std::size_t i = a.size(), j = b.size();
    while (i && j) {
        if (a[i - 1] == b[j - 1]) {
            result.push_back(a[--i]);
            --j;
        } else if (length[i - 1][j] >= length[i][j - 1]) {
            --i;
        } else {
            --j;
        }
    }
    std::reverse(result.begin(), result.end());
    return result;
}
} // namespace adm

#ifdef ADM_DEMO
int main() {
    using namespace adm;
    try {
        std::string a = "banana", b = "ananas";
        std::cin >> a >> b;
        std::cout << longest_common_subsequence(a, b) << "\n";
    } catch (const std::exception &error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
}
#endif
