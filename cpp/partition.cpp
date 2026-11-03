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
struct Partition {
    Integer cost;
    Matrix groups;
};

Partition linear_partition(const Integers &values, int groups) {
    require(groups >= 1 && static_cast<std::size_t>(groups) <= values.size(),
            "partition requires 1 <= groups <= item count");
    Integers prefix(values.size() + 1);
    for (std::size_t i = 0; i < values.size(); ++i) {
        require(values[i] >= 0, "negative partition value");
        prefix[i + 1] = add(prefix[i], values[i]);
    }
    std::vector<std::vector<std::optional<Integer>>> cost(
        groups + 1, std::vector<std::optional<Integer>>(values.size() + 1));
    std::vector<std::vector<std::size_t>> split(groups + 1,
                                                std::vector<std::size_t>(values.size() + 1));
    cost[0][0] = 0;
    for (int count = 1; count <= groups; ++count) {
        for (std::size_t end = static_cast<std::size_t>(count); end <= values.size(); ++end) {
            for (std::size_t begin = static_cast<std::size_t>(count - 1); begin < end; ++begin) {
                if (!cost[count - 1][begin]) {
                    continue;
                }
                Integer candidate = std::max(*cost[count - 1][begin], prefix[end] - prefix[begin]);
                if (!cost[count][end] || candidate < *cost[count][end]) {
                    cost[count][end] = candidate;
                    split[count][end] = begin;
                }
            }
        }
    }
    Matrix parts;
    std::size_t end = values.size();
    for (int count = groups; count > 0; --count) {
        std::size_t begin = split[count][end];
        parts.emplace_back(values.begin() + static_cast<std::ptrdiff_t>(begin),
                           values.begin() + static_cast<std::ptrdiff_t>(end));
        end = begin;
    }
    std::reverse(parts.begin(), parts.end());
    return {*cost[groups][values.size()], parts};
}
} // namespace adm

#ifdef ADM_DEMO
int main() {
    using namespace adm;
    try {
        std::cout << linear_partition({1, 2, 3}, 2).cost << "\n";
    } catch (const std::exception &error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
}
#endif
