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
#include "geometry.hpp"

namespace adm {
Integer integer_floor(double value) {
    require(std::isfinite(value) && value >= 0 &&
                value < static_cast<double>(std::numeric_limits<Integer>::max()),
            "packing count overflow");
    return static_cast<Integer>(std::floor(value));
}

Integer dense_layers(double width, double height, double radius) {
    packing_domain(width, height, radius);
    if (width < 2 * radius || height < 2 * radius) {
        return 0;
    }
    return add(1, integer_floor((height - 2 * radius) / (std::sqrt(3.0) * radius)));
}

Integer plates_per_row(Integer row, double width, double radius) {
    packing_domain(width, 0, radius);
    require(row >= 0, "negative packing row");
    if (width < 2 * radius) {
        return 0;
    }
    double columns = width / (2 * radius);
    Integer full = integer_floor(columns);
    return row % 2 == 0 || columns - static_cast<double>(full) >= 0.5 ? full : full - 1;
}

Integer dense_plates(double width, double height, double radius) {
    Integer layers = dense_layers(width, height, radius);
    return add(multiply(layers / 2 + layers % 2, plates_per_row(0, width, radius)),
               multiply(layers / 2, plates_per_row(1, width, radius)));
}

Integer grid_plates(double width, double height, double radius) {
    packing_domain(width, height, radius);
    return multiply(integer_floor(height / (2 * radius)), plates_per_row(0, width, radius));
}

Point hex_to_cartesian(Point hex, double radius) {
    packing_domain(0, 0, radius);
    finite_point(hex);
    Point result{radius * hex.x + 2 * radius * hex.y, std::sqrt(3.0) * radius * hex.x};
    finite_point(result);
    return result;
}

Point cartesian_to_hex(Point point, double radius) {
    packing_domain(0, 0, radius);
    finite_point(point);
    double row = point.y / (std::sqrt(3.0) * radius);
    Point result{row, (point.x - radius * row) / (2 * radius)};
    finite_point(result);
    return result;
}

std::pair<int, int> array_to_hex(int row, int column) {
    // ceil(row/2) is row-floor(row/2), also for negative rows.
    int half = static_cast<int>(std::floor(row / 2.0));
    Integer diagonal = static_cast<Integer>(column) - half;
    require(diagonal >= std::numeric_limits<int>::min() &&
                diagonal <= std::numeric_limits<int>::max(),
            "hex coordinate overflow");
    return {row, static_cast<int>(diagonal)};
}

std::pair<int, int> hex_to_array(int row, int column) {
    Integer column_index =
        static_cast<Integer>(column) + static_cast<Integer>(std::floor(row / 2.0));
    require(column_index >= std::numeric_limits<int>::min() &&
                column_index <= std::numeric_limits<int>::max(),
            "array coordinate overflow");
    return {row, static_cast<int>(column_index)};
}

Integer plates_on_top(int row, int diagonal, double width, double height, double radius) {
    Integer layers = dense_layers(width, height, radius);
    require(row >= 0 && row < layers, "packing cell outside rows");
    auto cell = hex_to_array(row, diagonal);
    require(cell.second >= 0 && cell.second < plates_per_row(row, width, radius),
            "packing cell outside columns");
    Integer total = 0;
    for (Integer next = static_cast<Integer>(row) + 1; next < layers; ++next) {
        // The supported patch is clipped to the finite rectangle on each row.
        Integer left = std::max<Integer>(0, diagonal - (next - row) + next / 2);
        Integer right =
            std::min<Integer>(plates_per_row(next, width, radius) - 1, diagonal + next / 2);
        if (right >= left) {
            total = add(total, right - left + 1);
        }
    }
    return total;
}
} // namespace adm

#ifdef ADM_DEMO
int main() {
    using namespace adm;
    try {
        double w = 4, h = 4, r = 1;
        std::cin >> w >> h >> r;
        std::cout << grid_plates(w, h, r) << " " << dense_plates(w, h, r) << "\n";
    } catch (const std::exception &error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
}
#endif
