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
std::optional<std::vector<int>> subset_sum(const Integers &values, Integer target) {
    require(target >= 0, "negative subset-sum target");
    // Pseudopolynomial storage; explicitly reject requests beyond practical memory.
    require(target <= 10000000, "subset-sum target exceeds memory budget 10000000");
    std::vector<int> chosen(static_cast<std::size_t>(target) + 1, -1);
    chosen[0] = -2;
    for (std::size_t i = 0; i < values.size(); ++i) {
        require(values[i] >= 0, "negative subset-sum value");
        if (values[i] == 0 || values[i] > target) {
            continue;
        }
        for (Integer sum = target; sum >= values[i]; --sum) {
            if (chosen[sum] == -1 && chosen[sum - values[i]] != -1) {
                chosen[sum] = static_cast<int>(i);
            }
        }
    }
    if (chosen[target] == -1) {
        return std::nullopt;
    }
    std::vector<int> indices;
    for (Integer sum = target; sum > 0;) {
        int index = chosen[sum];
        indices.push_back(index);
        sum -= values[index];
    }
    std::sort(indices.begin(), indices.end());
    return indices;
}
} // namespace adm

#ifdef ADM_DEMO
int main() {
    using namespace adm;
    try {
        auto result = subset_sum({1, 3, 4}, 7);
        if (result) {
            for (auto index : *result) {
                std::cout << index << " ";
            }
        }
        std::cout << "\n";
    } catch (const std::exception &error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
}
#endif
