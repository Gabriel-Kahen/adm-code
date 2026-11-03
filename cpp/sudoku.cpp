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
std::optional<std::string> sudoku(const std::string &input, bool smart = true, bool fast = true) {
    require(input.size() == 81 && std::all_of(input.begin(), input.end(),
                                              [](char c) { return c >= '0' && c <= '9'; }),
            "Sudoku requires 81 decimal digits");
    std::string board = input;
    std::array<int, 9> rows{}, columns{}, boxes{};
    auto box = [](int cell) { return (cell / 27) * 3 + (cell % 9) / 3; };
    for (int cell = 0; cell < 81; ++cell) {
        int digit = board[cell] - '0';
        if (!digit) {
            continue;
        }
        int bit = 1 << digit, row = cell / 9, column = cell % 9, block = box(cell);
        require(((rows[row] | columns[column] | boxes[block]) & bit) == 0,
                "contradictory Sudoku givens");
        rows[row] |= bit;
        columns[column] |= bit;
        boxes[block] |= bit;
    }
    auto candidate_mask = [&](int cell) {
        if (fast) {
            return 0x3fe & ~(rows[cell / 9] | columns[cell % 9] | boxes[box(cell)]);
        }
        int blocked = 0;
        for (int other = 0; other < 81; ++other) {
            if (other / 9 == cell / 9 || other % 9 == cell % 9 || box(other) == box(cell)) {
                blocked |= 1 << (board[other] - '0');
            }
        }
        return 0x3fe & ~blocked;
    };
    std::function<bool()> solve = [&]() {
        int best_cell = -1, best_mask = 0, best_count = 10;
        for (int cell = 0; cell < 81; ++cell) {
            if (board[cell] != '0') {
                continue;
            }
            int mask = candidate_mask(cell);
            int count = 0;
            for (int bits = mask; bits; bits &= bits - 1) {
                ++count;
            }
            if (count < best_count) {
                best_count = count;
                best_cell = cell;
                best_mask = mask;
            }
            if (!smart) {
                break;
            }
        }
        if (best_cell == -1) {
            return true;
        }
        if (best_count == 0) {
            return false;
        }
        int row = best_cell / 9, column = best_cell % 9, block = box(best_cell);
        for (int digit = 1; digit <= 9; ++digit) {
            int bit = 1 << digit;
            if (!(best_mask & bit)) {
                continue;
            }
            board[best_cell] = static_cast<char>('0' + digit);
            rows[row] |= bit;
            columns[column] |= bit;
            boxes[block] |= bit;
            if (solve()) {
                return true;
            }
            rows[row] ^= bit;
            columns[column] ^= bit;
            boxes[block] ^= bit;
            board[best_cell] = '0';
        }
        return false;
    };
    if (solve()) {
        return board;
    }
    return std::nullopt;
}
} // namespace adm

#ifdef ADM_DEMO
int main() {
    using namespace adm;
    try {
        std::string puzzle;
        std::cin >> puzzle;
        auto result = sudoku(puzzle);
        std::cout << (result ? *result : "No solution") << "\n";
    } catch (const std::exception &error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
}
#endif
