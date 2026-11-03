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

#pragma once

#include "item.hpp"

namespace adm {
// Exact signed decimal integers. No fixed digit capacity.
class BigInteger {
    std::string digits_; // Magnitude, most significant digit first.
    bool negative_ = false;
    static int compare_magnitude(const std::string &, const std::string &);
    static std::string add_magnitude(const std::string &, const std::string &);
    static std::string subtract_magnitude(const std::string &, const std::string &);
    void normalize();

  public:
    explicit BigInteger(const std::string &value = "0");
    explicit BigInteger(Integer value);
    std::string str() const;
    BigInteger operator-() const;
    friend BigInteger operator+(const BigInteger &, const BigInteger &);
    friend BigInteger operator-(const BigInteger &, const BigInteger &);
    friend BigInteger operator*(const BigInteger &, const BigInteger &);
    friend BigInteger operator/(const BigInteger &, const BigInteger &);
};
} // namespace adm
