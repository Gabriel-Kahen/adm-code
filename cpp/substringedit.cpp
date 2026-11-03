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
Integer substring_edit_distance(const std::string &pattern, const std::string &text) {
    // Every text prefix is free: the first row represents all possible starts.
    Integers previous(text.size() + 1), current(text.size() + 1);
    for (std::size_t i = 1; i <= pattern.size(); ++i) {
        current[0] = static_cast<Integer>(i);
        for (std::size_t j = 1; j <= text.size(); ++j) {
            current[j] = std::min({previous[j - 1] + (pattern[i - 1] != text[j - 1]),
                                   previous[j] + 1, current[j - 1] + 1});
        }
        previous.swap(current);
    }
    return *std::min_element(previous.begin(), previous.end());
}
} // namespace adm

#ifdef ADM_DEMO
int main() {
    using namespace adm;
    try {
        std::string a = "cat", b = "xxcatyy";
        std::cin >> a >> b;
        std::cout << substring_edit_distance(a, b) << "\n";
    } catch (const std::exception &error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
}
#endif
