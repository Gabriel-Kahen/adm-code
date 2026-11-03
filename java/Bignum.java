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

import java.math.BigInteger;

public final class Bignum {
    public static BigInteger bigint(String operation, BigInteger a, BigInteger b) {
        return switch (operation) {
            case "add" -> a.add(b);
            case "sub" -> a.subtract(b);
            case "mul" -> a.multiply(b);
            case "div" -> a.divide(b); // BigInteger uses truncation toward zero.
            default -> throw new IllegalArgumentException("unknown integer operation");
        };
    }

    public static void main(String[] args) {
        System.out.println(bigint("mul", new BigInteger("123"), new BigInteger("17")));
    }
}
