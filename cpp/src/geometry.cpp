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

#include "adm.hpp"

#include <numeric>

namespace adm {
namespace {
void finite_point(Point p) {
    require(std::isfinite(p.x) && std::isfinite(p.y), "nonfinite point");
}
Line normalized(Line line) {
    double length = std::hypot(line.a, line.b);
    require(std::isfinite(length) && length > 0 && std::isfinite(line.c), "invalid line");
    line.a /= length;
    line.b /= length;
    line.c /= length;
    if (line.a < 0 || (line.a == 0 && line.b < 0)) {
        line.a = -line.a;
        line.b = -line.b;
        line.c = -line.c;
    }
    return line;
}
void packing_domain(double width, double height, double radius) {
    require(std::isfinite(width) && std::isfinite(height) && std::isfinite(radius) && width >= 0 &&
                height >= 0 && radius > 0,
            "invalid packing dimensions");
}
Integer integer_floor(double value) {
    require(std::isfinite(value) && value >= 0 &&
                value < static_cast<double>(std::numeric_limits<Integer>::max()),
            "packing count overflow");
    return static_cast<Integer>(std::floor(value));
}
void simple_polygon(const std::vector<Point> &polygon) {
    require(polygon.size() >= 3, "polygon needs at least three vertices");
    const std::size_t n = polygon.size();
    for (auto point : polygon) {
        finite_point(point);
    }
    for (std::size_t i = 0; i < n; ++i) {
        require(point_distance(polygon[i], polygon[(i + 1) % n]) > epsilon,
                "zero-length polygon edge");
        for (std::size_t j = i + 1; j < n; ++j) {
            if (j == i + 1 || (i == 0 && j == n - 1)) {
                continue;
            }
            require(!segments_intersect(polygon[i], polygon[(i + 1) % n], polygon[j],
                                        polygon[(j + 1) % n]),
                    "self-intersecting polygon");
        }
    }
    require(polygon_area(polygon) > epsilon, "degenerate polygon");
}
double signed_polygon_area(const std::vector<Point> &polygon) {
    double twice = 0;
    for (std::size_t i = 0; i < polygon.size(); ++i) {
        Point a = polygon[i], b = polygon[(i + 1) % polygon.size()];
        twice += a.x * b.y - a.y * b.x;
    }
    require(std::isfinite(twice), "polygon area overflow");
    return twice / 2;
}
} // namespace
double cross(Point a, Point b, Point c) {
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x);
}
int orientation(Point a, Point b, Point c, double tolerance) {
    require(tolerance >= 0 && std::isfinite(tolerance), "invalid tolerance");
    double value = cross(a, b, c);
    require(std::isfinite(value), "orientation overflow");
    return value > tolerance ? 1 : (value < -tolerance ? -1 : 0);
}
double triangle_area(Point a, Point b, Point c) {
    return std::abs(cross(a, b, c)) / 2;
}
double point_distance(Point a, Point b) {
    finite_point(a);
    finite_point(b);
    double result = std::hypot(a.x - b.x, a.y - b.y);
    require(std::isfinite(result), "point distance overflow");
    return result;
}
Line points_to_line(Point a, Point b) {
    finite_point(a);
    finite_point(b);
    return normalized({a.y - b.y, b.x - a.x, a.x * b.y - b.x * a.y});
}
Line point_slope_line(Point p, double slope) {
    finite_point(p);
    require(std::isfinite(slope), "nonfinite slope");
    return normalized({slope, -1, p.y - slope * p.x});
}
bool parallel(Line a, Line b, double tolerance) {
    a = normalized(a);
    b = normalized(b);
    return std::abs(a.a * b.b - b.a * a.b) <= tolerance;
}
bool same_line(Line a, Line b, double tolerance) {
    a = normalized(a);
    b = normalized(b);
    return parallel(a, b, tolerance) && std::abs(a.a * b.c - b.a * a.c) <= tolerance &&
           std::abs(a.b * b.c - b.b * a.c) <= tolerance;
}
std::optional<Point> intersection(Line a, Line b, double tolerance) {
    a = normalized(a);
    b = normalized(b);
    double determinant = a.a * b.b - b.a * a.b;
    if (std::abs(determinant) <= tolerance) {
        return std::nullopt;
    }
    Point result{(a.b * b.c - b.b * a.c) / determinant, (a.c * b.a - b.c * a.a) / determinant};
    finite_point(result);
    return result;
}
Point project(Point point, Line line) {
    finite_point(point);
    line = normalized(line);
    double offset = line.a * point.x + line.b * point.y + line.c;
    Point result{point.x - line.a * offset, point.y - line.b * offset};
    finite_point(result);
    return result;
}
bool in_box(Point p, Point a, Point b, double tolerance) {
    return p.x >= std::min(a.x, b.x) - tolerance && p.x <= std::max(a.x, b.x) + tolerance &&
           p.y >= std::min(a.y, b.y) - tolerance && p.y <= std::max(a.y, b.y) + tolerance;
}
bool segments_intersect(Point a, Point b, Point c, Point d, double tolerance) {
    int abc = orientation(a, b, c, tolerance), abd = orientation(a, b, d, tolerance);
    int cda = orientation(c, d, a, tolerance), cdb = orientation(c, d, b, tolerance);
    if (abc * abd < 0 && cda * cdb < 0) {
        return true;
    }
    return (abc == 0 && in_box(c, a, b, tolerance)) || (abd == 0 && in_box(d, a, b, tolerance)) ||
           (cda == 0 && in_box(a, c, d, tolerance)) || (cdb == 0 && in_box(b, c, d, tolerance));
}
double polygon_area(const std::vector<Point> &points) {
    for (Point point : points) {
        finite_point(point);
    }
    return std::abs(signed_polygon_area(points));
}
std::vector<Point> convex_hull(std::vector<Point> points) {
    for (Point point : points) {
        finite_point(point);
    }
    std::sort(points.begin(), points.end(),
              [](Point a, Point b) { return std::tie(a.x, a.y) < std::tie(b.x, b.y); });
    points.erase(std::unique(points.begin(), points.end(),
                             [](Point a, Point b) { return a.x == b.x && a.y == b.y; }),
                 points.end());
    if (points.size() <= 2) {
        return points;
    }
    std::vector<Point> lower, upper;
    for (Point point : points) {
        while (lower.size() >= 2 &&
               orientation(lower[lower.size() - 2], lower.back(), point) <= 0) {
            lower.pop_back();
        }
        lower.push_back(point);
    }
    for (auto it = points.rbegin(); it != points.rend(); ++it) {
        while (upper.size() >= 2 && orientation(upper[upper.size() - 2], upper.back(), *it) <= 0) {
            upper.pop_back();
        }
        upper.push_back(*it);
    }
    lower.pop_back();
    upper.pop_back();
    lower.insert(lower.end(), upper.begin(), upper.end());
    return lower;
}
std::vector<std::array<int, 3>> triangulate(const std::vector<Point> &polygon) {
    simple_polygon(polygon);
    std::vector<int> remaining(polygon.size());
    std::iota(remaining.begin(), remaining.end(), 0);
    if (signed_polygon_area(polygon) < 0) {
        std::reverse(remaining.begin(), remaining.end());
    }
    std::vector<std::array<int, 3>> result;
    while (remaining.size() > 3) {
        bool found = false;
        for (std::size_t i = 0; i < remaining.size(); ++i) {
            int a = remaining[(i + remaining.size() - 1) % remaining.size()], b = remaining[i],
                c = remaining[(i + 1) % remaining.size()];
            if (orientation(polygon[a], polygon[b], polygon[c]) <= 0) {
                continue;
            }
            bool blocked = false;
            for (int vertex : remaining) {
                if (vertex == a || vertex == b || vertex == c) {
                    continue;
                }
                if (orientation(polygon[a], polygon[b], polygon[vertex]) >= 0 &&
                    orientation(polygon[b], polygon[c], polygon[vertex]) >= 0 &&
                    orientation(polygon[c], polygon[a], polygon[vertex]) >= 0) {
                    blocked = true;
                    break;
                }
            }
            if (!blocked) {
                result.push_back({a, b, c});
                remaining.erase(remaining.begin() + static_cast<std::ptrdiff_t>(i));
                found = true;
                break;
            }
        }
        require(found, "polygon has no nondegenerate ear at tolerance");
    }
    require(triangle_area(polygon[remaining[0]], polygon[remaining[1]], polygon[remaining[2]]) >
                epsilon,
            "degenerate final triangle");
    result.push_back({remaining[0], remaining[1], remaining[2]});
    return result;
}
double minimum_weight_triangulation(const std::vector<Point> &polygon) {
    simple_polygon(polygon);
    const std::size_t n = polygon.size();
    int direction = orientation(polygon[0], polygon[1], polygon[2]);
    require(direction != 0, "minimum-weight triangulation requires strict convexity");
    for (std::size_t i = 0; i < n; ++i) {
        require(orientation(polygon[i], polygon[(i + 1) % n], polygon[(i + 2) % n]) == direction,
                "minimum-weight triangulation requires strict convexity");
    }
    std::vector<std::vector<double>> cost(n, std::vector<double>(n));
    for (std::size_t gap = 2; gap < n; ++gap) {
        for (std::size_t begin = 0; begin + gap < n; ++begin) {
            std::size_t end = begin + gap;
            cost[begin][end] = std::numeric_limits<double>::infinity();
            for (std::size_t middle = begin + 1; middle < end; ++middle) {
                double perimeter = point_distance(polygon[begin], polygon[middle]) +
                                   point_distance(polygon[middle], polygon[end]) +
                                   point_distance(polygon[end], polygon[begin]);
                cost[begin][end] =
                    std::min(cost[begin][end], cost[begin][middle] + cost[middle][end] + perimeter);
            }
        }
    }
    return cost[0][n - 1];
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
    return {radius * hex.x + 2 * radius * hex.y, std::sqrt(3.0) * radius * hex.x};
}
Point cartesian_to_hex(Point point, double radius) {
    packing_domain(0, 0, radius);
    finite_point(point);
    double row = point.y / (std::sqrt(3.0) * radius);
    return {row, (point.x - radius * row) / (2 * radius)};
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
std::pair<double, double> superman(Point start, Point end, const std::vector<Circle> &circles) {
    finite_point(start);
    finite_point(end);
    for (std::size_t i = 0; i < circles.size(); ++i) {
        const auto &circle = circles[i];
        finite_point(circle.center);
        require(std::isfinite(circle.radius) && circle.radius > 0, "invalid obstacle radius");
        require(point_distance(start, circle.center) >= circle.radius - epsilon &&
                    point_distance(end, circle.center) >= circle.radius - epsilon,
                "endpoint inside obstacle");
        for (std::size_t j = 0; j < i; ++j) {
            require(point_distance(circle.center, circles[j].center) >=
                        circle.radius + circles[j].radius - epsilon,
                    "overlapping circles outside model");
        }
    }
    double direct = point_distance(start, end), through = 0, around = 0;
    if (direct == 0) {
        return {0, 0};
    }
    Line path = points_to_line(start, end);
    for (const auto &circle : circles) {
        Point closest = project(circle.center, path);
        double away = point_distance(circle.center, closest);
        if (away < circle.radius && in_box(closest, start, end)) {
            through += 2 * std::sqrt(std::max(0.0, circle.radius * circle.radius - away * away));
            around += 2 * circle.radius * std::acos(std::clamp(away / circle.radius, -1.0, 1.0));
        }
    }
    return {through, direct - through + around};
}
} // namespace adm
