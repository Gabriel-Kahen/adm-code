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
import java.util.Arrays;

public final class Gcd {
    /** Returns [g,x,y], g>=0 and a*x+b*y=g, including signed/zero operands. */
    public static BigInteger[] extendedGcd(BigInteger a, BigInteger b) {
        BigInteger oldR = a.abs();
        BigInteger r = b.abs();
        BigInteger oldX = BigInteger.ONE;
        BigInteger x = BigInteger.ZERO;
        BigInteger oldY = BigInteger.ZERO;
        BigInteger y = BigInteger.ONE;
        while (!r.equals(BigInteger.ZERO)) {
            BigInteger quotient = oldR.divide(r);
            BigInteger nextR = oldR.subtract(quotient.multiply(r));
            oldR = r;
            r = nextR;
            BigInteger nextX = oldX.subtract(quotient.multiply(x));
            oldX = x;
            x = nextX;
            BigInteger nextY = oldY.subtract(quotient.multiply(y));
            oldY = y;
            y = nextY;
        }
        return new BigInteger[] {oldR, a.signum() < 0 ? oldX.negate() : oldX,
                                 b.signum() < 0 ? oldY.negate() : oldY};
    }

    public static void main(String[] args) {
        System.out.println(
            Arrays.toString(extendedGcd(BigInteger.valueOf(252), BigInteger.valueOf(198))));
    }
}
