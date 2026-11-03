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
#include "editdistance.hpp"

namespace adm {
EditResult edit_distance(const std::string &a, const std::string &b) {
    const std::size_t rows = a.size() + 1, columns = b.size() + 1;
    Matrix cost(rows, Integers(columns));
    std::vector<std::string> parent(rows, std::string(columns, 'M'));
    for (std::size_t i = 1; i < rows; ++i) {
        cost[i][0] = static_cast<Integer>(i);
        parent[i][0] = 'D';
    }
    for (std::size_t j = 1; j < columns; ++j) {
        cost[0][j] = static_cast<Integer>(j);
        parent[0][j] = 'I';
    }
    for (std::size_t i = 1; i < rows; ++i) {
        for (std::size_t j = 1; j < columns; ++j) {
            cost[i][j] = cost[i - 1][j - 1] + (a[i - 1] != b[j - 1]);
            parent[i][j] = a[i - 1] == b[j - 1] ? 'M' : 'S';
            if (cost[i][j - 1] + 1 < cost[i][j]) {
                cost[i][j] = cost[i][j - 1] + 1;
                parent[i][j] = 'I';
            }
            if (cost[i - 1][j] + 1 < cost[i][j]) {
                cost[i][j] = cost[i - 1][j] + 1;
                parent[i][j] = 'D';
            }
        }
    }
    std::string operations;
    std::size_t i = a.size(), j = b.size();
    while (i || j) {
        char operation = parent[i][j];
        operations.push_back(operation);
        if (operation != 'I') {
            --i;
        }
        if (operation != 'D') {
            --j;
        }
    }
    std::reverse(operations.begin(), operations.end());
    return {cost.back().back(), operations};
}
} // namespace adm
