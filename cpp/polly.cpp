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
struct Suitor {
    std::string first, last;
    Integer height, weight;
};

std::vector<Suitor> rank_suitors(std::vector<Suitor> suitors) {
    auto key = [](const Suitor &suitor) {
        require(suitor.height >= 0 && suitor.weight >= 0, "negative suitor measurement");
        return std::make_tuple(std::abs(suitor.height - 180),
                               suitor.weight > 75 ? suitor.weight - 75 : -suitor.weight,
                               suitor.last, suitor.first);
    };
    for (const auto &suitor : suitors) {
        (void)key(suitor);
    }
    std::stable_sort(suitors.begin(), suitors.end(),
                     [&](const Suitor &a, const Suitor &b) { return key(a) < key(b); });
    return suitors;
}
} // namespace adm

#ifdef ADM_DEMO
int main() {
    using namespace adm;
    try {
        for (auto person : rank_suitors({{"Amy", "A", 180, 75}, {"Bob", "B", 181, 80}})) {
            std::cout << person.last << ", " << person.first << "\n";
        }
    } catch (const std::exception &error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
}
#endif
