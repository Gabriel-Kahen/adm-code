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
Integer queens(int n) {
    require(n >= 0 && n <= 15, "queens count requires 0 <= n <= 15");
    using Mask = std::uint64_t;
    Mask all = (Mask(1) << n) - 1;
    std::function<Integer(Mask, Mask, Mask)> visit = [&](Mask columns, Mask left,
                                                         Mask right) -> Integer {
        if (columns == all) {
            return 1;
        }
        Mask choices = all & ~(columns | left | right);
        Integer count = 0;
        while (choices) {
            Mask next = choices & (~choices + 1);
            choices -= next;
            count = add(count, visit(columns | next, (left | next) << 1, (right | next) >> 1));
        }
        return count;
    };
    return visit(0, 0, 0);
}
} // namespace adm

#ifdef ADM_DEMO
int main() {
    using namespace adm;
    try {
        int n = 8;
        std::cin >> n;
        std::cout << queens(n) << "\n";
    } catch (const std::exception &error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
}
#endif
