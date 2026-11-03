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

public final class Fib {
    /** F(0)=0, F(1)=1; recursive O(phi^n), table/constant O(n) additions. */
    public static BigInteger fibonacci(String method, int n) {
        if (n < 0 || n > 100000) {
            throw new IllegalArgumentException("Fibonacci index outside 0..100000");
        }
        return switch (method) {
            case "recursive" -> {
                if (n > 35) {
                    throw new IllegalArgumentException("recursive Fibonacci is limited to 35");
                }
                yield recursiveFibonacci(n);
            }
            case "memo" -> {
                if (n > 1000) {
                    throw new IllegalArgumentException("memo Fibonacci is limited to 1000");
                }
                yield memoFibonacci(n, new BigInteger[n + 1]);
            }
            case "table" -> {
                BigInteger[] values = new BigInteger[Math.max(2, n + 1)];
                values[0] = BigInteger.ZERO;
                values[1] = BigInteger.ONE;
                for (int i = 2; i <= n; i++) {
                    values[i] = values[i - 1].add(values[i - 2]);
                }
                yield values[n];
            }
            case "constant" -> {
                BigInteger previous = BigInteger.ZERO;
                BigInteger current = BigInteger.ONE;
                for (int i = 0; i < n; i++) {
                    BigInteger next = previous.add(current);
                    previous = current;
                    current = next;
                }
                yield previous;
            }
            default -> throw new IllegalArgumentException("unknown Fibonacci method");
        };
    }

    static BigInteger recursiveFibonacci(int n) {
        if (n < 2) {
            return BigInteger.valueOf(n);
        }
        return recursiveFibonacci(n - 1).add(recursiveFibonacci(n - 2));
    }

    static BigInteger memoFibonacci(int n, BigInteger[] cache) {
        if (n < 2) {
            return BigInteger.valueOf(n);
        }
        if (cache[n] == null) {
            cache[n] = memoFibonacci(n - 1, cache).add(memoFibonacci(n - 2, cache));
        }
        return cache[n];
    }

    public static void main(String[] args) {
        java.util.Scanner in = new java.util.Scanner(System.in);
        System.out.println(fibonacci("table", in.hasNextInt() ? in.nextInt() : 10));
    }
}
