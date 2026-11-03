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
Matrix matrix_multiply(const Matrix &a, const Matrix &b) {
    require(!a.empty() && !b.empty() && !a.front().empty() && !b.front().empty(), "empty matrix");
    const auto inner = a.front().size(), columns = b.front().size();
    require(inner == b.size(), "matrix dimension mismatch");
    for (const auto &row : a) {
        require(row.size() == inner, "ragged matrix");
    }
    for (const auto &row : b) {
        require(row.size() == columns, "ragged matrix");
    }
    Matrix result(a.size(), Integers(columns));
    for (std::size_t i = 0; i < a.size(); ++i) {
        for (std::size_t k = 0; k < inner; ++k) {
            for (std::size_t j = 0; j < columns; ++j) {
                result[i][j] = add(result[i][j], multiply(a[i][k], b[k][j]));
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
        auto product = matrix_multiply({{1, 2}}, {{3}, {4}});
        std::cout << product[0][0] << "\n";
    } catch (const std::exception &error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
}
#endif
