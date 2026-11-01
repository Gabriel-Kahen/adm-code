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
void require(bool condition, const std::string &message) {
    if (!condition) {
        throw std::invalid_argument(message);
    }
}
Integer add(Integer a, Integer b) {
    Integer result;
    if (__builtin_add_overflow(a, b, &result)) {
        throw std::overflow_error("integer addition overflow");
    }
    return result;
}
Integer subtract(Integer a, Integer b) {
    Integer result;
    if (__builtin_sub_overflow(a, b, &result)) {
        throw std::overflow_error("integer subtraction overflow");
    }
    return result;
}
Integer multiply(Integer a, Integer b) {
    Integer result;
    if (__builtin_mul_overflow(a, b, &result)) {
        throw std::overflow_error("integer multiplication overflow");
    }
    return result;
}
void BigInteger::normalize() {
    auto first = digits_.find_first_not_of('0');
    digits_ = first == std::string::npos ? "0" : digits_.substr(first);
    if (digits_ == "0") {
        negative_ = false;
    }
}
BigInteger::BigInteger(const std::string &value) {
    require(!value.empty(), "empty integer");
    std::size_t start = value[0] == '-' || value[0] == '+' ? 1 : 0;
    require(start < value.size(), "integer requires digits");
    negative_ = value[0] == '-';
    digits_ = value.substr(start);
    require(
        std::all_of(digits_.begin(), digits_.end(), [](char c) { return c >= '0' && c <= '9'; }),
        "invalid decimal integer");
    normalize();
}
BigInteger::BigInteger(Integer value) : BigInteger(std::to_string(value)) {}
std::string BigInteger::str() const {
    return (negative_ ? "-" : "") + digits_;
}
int BigInteger::compare_magnitude(const std::string &a, const std::string &b) {
    if (a.size() != b.size()) {
        return a.size() < b.size() ? -1 : 1;
    }
    return a == b ? 0 : (a < b ? -1 : 1);
}
std::string BigInteger::add_magnitude(const std::string &a, const std::string &b) {
    std::string result;
    std::size_t i = a.size(), j = b.size();
    int carry = 0;
    while (i || j || carry) {
        int digit = carry;
        if (i) {
            digit += a[--i] - '0';
        }
        if (j) {
            digit += b[--j] - '0';
        }
        result.push_back(static_cast<char>('0' + digit % 10));
        carry = digit / 10;
    }
    std::reverse(result.begin(), result.end());
    return result;
}
std::string BigInteger::subtract_magnitude(const std::string &a, const std::string &b) {
    std::string result;
    std::size_t i = a.size(), j = b.size();
    int borrow = 0;
    while (i) {
        int digit = a[--i] - '0' - borrow;
        if (j) {
            digit -= b[--j] - '0';
        }
        borrow = digit < 0;
        if (borrow) {
            digit += 10;
        }
        result.push_back(static_cast<char>('0' + digit));
    }
    while (result.size() > 1 && result.back() == '0') {
        result.pop_back();
    }
    std::reverse(result.begin(), result.end());
    return result;
}
BigInteger BigInteger::operator-() const {
    BigInteger result = *this;
    if (digits_ != "0") {
        result.negative_ = !negative_;
    }
    return result;
}
BigInteger operator+(const BigInteger &a, const BigInteger &b) {
    BigInteger result;
    if (a.negative_ == b.negative_) {
        result.digits_ = BigInteger::add_magnitude(a.digits_, b.digits_);
        result.negative_ = a.negative_;
    } else if (BigInteger::compare_magnitude(a.digits_, b.digits_) >= 0) {
        result.digits_ = BigInteger::subtract_magnitude(a.digits_, b.digits_);
        result.negative_ = a.negative_;
    } else {
        result.digits_ = BigInteger::subtract_magnitude(b.digits_, a.digits_);
        result.negative_ = b.negative_;
    }
    result.normalize();
    return result;
}
BigInteger operator-(const BigInteger &a, const BigInteger &b) {
    return a + (-b);
}
BigInteger operator*(const BigInteger &a, const BigInteger &b) {
    std::vector<int> digits(a.digits_.size() + b.digits_.size());
    for (std::size_t i = a.digits_.size(); i-- > 0;) {
        for (std::size_t j = b.digits_.size(); j-- > 0;) {
            int product = (a.digits_[i] - '0') * (b.digits_[j] - '0') + digits[i + j + 1];
            digits[i + j + 1] = product % 10;
            digits[i + j] += product / 10;
        }
    }
    BigInteger result;
    result.digits_.clear();
    for (int digit : digits) {
        result.digits_.push_back(static_cast<char>('0' + digit));
    }
    result.negative_ = a.negative_ != b.negative_;
    result.normalize();
    return result;
}
BigInteger operator/(const BigInteger &a, const BigInteger &b) {
    require(b.digits_ != "0", "division by zero");
    BigInteger result;
    result.digits_.clear();
    std::string remainder = "0";
    for (char digit : a.digits_) {
        remainder = remainder == "0" ? std::string(1, digit) : remainder + digit;
        int quotient = 0;
        while (BigInteger::compare_magnitude(remainder, b.digits_) >= 0) {
            remainder = BigInteger::subtract_magnitude(remainder, b.digits_);
            ++quotient;
        }
        result.digits_.push_back(static_cast<char>('0' + quotient));
    }
    result.negative_ = a.negative_ != b.negative_;
    result.normalize();
    return result;
}
BigInteger fibonacci(const std::string &method, int n) {
    require(n >= 0, "negative Fibonacci index");
    if (method == "recursive") {
        require(n <= 35, "recursive Fibonacci limited to index 35");
        if (n < 2) {
            return BigInteger(n);
        }
        return fibonacci(method, n - 1) + fibonacci(method, n - 2);
    }
    if (method == "memo") {
        std::vector<std::optional<BigInteger>> cache(static_cast<std::size_t>(n) + 2);
        cache[0] = BigInteger(0);
        cache[1] = BigInteger(1);
        std::function<BigInteger(int)> solve = [&](int index) {
            if (!cache[index]) {
                cache[index] = solve(index - 1) + solve(index - 2);
            }
            return *cache[index];
        };
        return solve(n);
    }
    if (method == "table") {
        std::vector<BigInteger> values(static_cast<std::size_t>(n) + 2);
        values[1] = BigInteger(1);
        for (int i = 2; i <= n; ++i) {
            values[i] = values[i - 1] + values[i - 2];
        }
        return values[n];
    }
    require(method == "constant", "unknown Fibonacci method");
    BigInteger previous(0), current(1);
    for (int i = 0; i < n; ++i) {
        BigInteger next = previous + current;
        previous = current;
        current = next;
    }
    return previous;
}
BigInteger binomial(int n, int k) {
    require(n >= 0 && k >= 0 && k <= n, "invalid binomial indices");
    k = std::min(k, n - k);
    if (k == 0) {
        return BigInteger(1);
    }
    std::vector<BigInteger> row(static_cast<std::size_t>(k) + 1);
    row[0] = BigInteger(1);
    for (Integer level = 1; level <= n; ++level) {
        for (int column = std::min(static_cast<int>(level), k); column > 0; --column) {
            row[column] = row[column] + row[column - 1];
        }
    }
    return row[k];
}
std::array<Integer, 3> extended_gcd(Integer a, Integer b) {
    require(a != std::numeric_limits<Integer>::min() && b != std::numeric_limits<Integer>::min(),
            "GCD magnitude exceeds signed64");
    Integer old_r = std::abs(a), r = std::abs(b), old_x = 1, x = 0, old_y = 0, y = 1;
    while (r != 0) {
        Integer q = old_r / r;
        Integer next_r = old_r % r;
        Integer next_x = subtract(old_x, multiply(q, x));
        Integer next_y = subtract(old_y, multiply(q, y));
        old_r = r;
        r = next_r;
        old_x = x;
        x = next_x;
        old_y = y;
        y = next_y;
    }
    return {old_r, a < 0 ? -old_x : old_x, b < 0 ? -old_y : old_y};
}
Integers prime_factors(Integer n) {
    require(n >= 1, "factorization requires positive integer");
    Integers factors;
    for (Integer divisor = 2; divisor <= n / divisor; divisor += divisor == 2 ? 1 : 2) {
        while (n % divisor == 0) {
            factors.push_back(divisor);
            n /= divisor;
        }
    }
    if (n > 1) {
        factors.push_back(n);
    }
    return factors;
}
double distance(const std::vector<double> &a, const std::vector<double> &b) {
    require(a.size() == b.size(), "distance dimension mismatch");
    double result = 0;
    for (std::size_t i = 0; i < a.size(); ++i) {
        result = std::hypot(result, a[i] - b[i]);
    }
    require(std::isfinite(result), "distance overflow");
    return result;
}
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
Integers convolve(const Integers &a, const Integers &b) {
    if (a.empty() || b.empty()) {
        return {};
    }
    Integers result(a.size() + b.size() - 1);
    for (std::size_t i = 0; i < a.size(); ++i) {
        for (std::size_t j = 0; j < b.size(); ++j) {
            result[i + j] = add(result[i + j], multiply(a[i], b[j]));
        }
    }
    return result;
}
Integer Random::integer(Integer low, Integer high) {
    require(low <= high, "invalid integer random interval");
    return std::uniform_int_distribution<Integer>(low, high)(engine_);
}
double Random::real(double low, double high) {
    require(std::isfinite(low) && std::isfinite(high) && low <= high,
            "invalid real random interval");
    if (low == high) {
        return low;
    }
    require(std::isfinite(high - low), "real random interval width overflow");
    return std::uniform_real_distribution<double>(low, high)(engine_);
}
} // namespace adm
