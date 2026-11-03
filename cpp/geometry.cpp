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
#include "distance.hpp"
#include "geometry.hpp"

namespace adm {
void finite_point(Point p) {
    require(std::isfinite(p.x) && std::isfinite(p.y), "nonfinite point");
}

void validate_tolerance(double tolerance) {
    require(std::isfinite(tolerance) && tolerance >= 0, "invalid tolerance");
}

Line normalized(Line line) {
    double length = std::hypot(line.a, line.b);
    require(std::isfinite(length) && length > 0 && std::isfinite(line.c), "invalid line");
    line.a /= length;
    line.b /= length;
    line.c /= length;
    require(std::isfinite(line.a) && std::isfinite(line.b) && std::isfinite(line.c),
            "line normalization overflow");
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
    // Translate the fan before multiplying. Direct shoelace products can
    // erase a small polygon's area at a large coordinate offset.
    for (std::size_t i = 1; i + 1 < polygon.size(); ++i) {
        twice += cross(polygon[0], polygon[i], polygon[i + 1]);
    }
    require(std::isfinite(twice), "polygon area overflow");
    return twice / 2;
}

// namespace
double cross(Point a, Point b, Point c) {
    finite_point(a);
    finite_point(b);
    finite_point(c);
    double result = (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x);
    require(std::isfinite(result), "orientation overflow");
    return result;
}

int orientation(Point a, Point b, Point c, double tolerance) {
    validate_tolerance(tolerance);
    double value = cross(a, b, c);
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
    double x_coefficient = a.y - b.y;
    double y_coefficient = b.x - a.x;
    double constant = -(x_coefficient * a.x + y_coefficient * a.y);
    return normalized({x_coefficient, y_coefficient, constant});
}

Line point_slope_line(Point p, double slope) {
    finite_point(p);
    require(std::isfinite(slope), "nonfinite slope");
    return normalized({slope, -1, p.y - slope * p.x});
}

bool parallel(Line a, Line b, double tolerance) {
    validate_tolerance(tolerance);
    a = normalized(a);
    b = normalized(b);
    return std::abs(a.a * b.b - b.a * a.b) <= tolerance;
}

bool same_line(Line a, Line b, double tolerance) {
    validate_tolerance(tolerance);
    a = normalized(a);
    b = normalized(b);
    return parallel(a, b, tolerance) && std::abs(a.a * b.c - b.a * a.c) <= tolerance &&
           std::abs(a.b * b.c - b.b * a.c) <= tolerance;
}

std::optional<Point> intersection(Line a, Line b, double tolerance) {
    validate_tolerance(tolerance);
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
    validate_tolerance(tolerance);
    finite_point(p);
    finite_point(a);
    finite_point(b);
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
} // namespace adm
