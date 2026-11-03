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
#include "bignum.hpp"

namespace adm {
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
} // namespace adm

#ifdef ADM_DEMO
int main() {
    using namespace adm;
    try {
        BigInteger a("123"), b("17");
        std::cout << (a + b).str() << "\n"
                  << (a - b).str() << "\n"
                  << (a * b).str() << "\n"
                  << (a / b).str() << "\n";
    } catch (const std::exception &error) {
        std::cerr << error.what() << "\n";
        return 1;
    }
}
#endif
