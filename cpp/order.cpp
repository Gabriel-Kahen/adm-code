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
std::vector<std::pair<int, int>> grid_order(const std::string &method, int rows, int columns) {
    require(rows >= 0 && columns >= 0, "negative grid dimension");
    std::vector<std::pair<int, int>> result;
    if (method == "row" || method == "snake") {
        for (int row = 0; row < rows; ++row) {
            for (int column = 0; column < columns; ++column) {
                result.emplace_back(row,
                                    method == "snake" && row % 2 ? columns - 1 - column : column);
            }
        }
    } else if (method == "column") {
        for (int column = 0; column < columns; ++column) {
            for (int row = 0; row < rows; ++row) {
                result.emplace_back(row, column);
            }
        }
    } else {
        require(method == "diagonal", "unknown grid order");
        for (Integer diagonal = 0; diagonal < static_cast<Integer>(rows) + columns - 1;
             ++diagonal) {
            for (Integer row = std::max<Integer>(0, diagonal - columns + 1);
                 row <= std::min<Integer>(rows - 1, diagonal); ++row) {
                result.emplace_back(static_cast<int>(row), static_cast<int>(diagonal - row));
            }
        }
    }
    return result;
}
} // namespace adm

#ifdef ADM_DEMO
int main() {
    using namespace adm;
    try {
        for (auto cell : grid_order("diagonal", 3, 4)) {
            std::cout << cell.first << " " << cell.second << "\n";
        }
    } catch (const std::exception &error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
}
#endif
