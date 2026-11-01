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

package adm;

import java.math.BigInteger;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/** Exact integer routines and checked long matrix/polynomial arithmetic. */
public final class Numeric {
    private Numeric() {}
    private static final BigInteger ZERO = BigInteger.ZERO;
    private static final BigInteger ONE = BigInteger.ONE;

    public static BigInteger absoluteDifference(BigInteger a, BigInteger b) {
        return a.subtract(b).abs();
    }
    public static BigInteger bigint(String operation, BigInteger a, BigInteger b) {
        return switch (operation) {
            case "add" -> a.add(b);
            case "sub" -> a.subtract(b);
            case "mul" -> a.multiply(b);
            case "div" -> a.divide(b); // BigInteger uses truncation toward zero.
            default -> throw new IllegalArgumentException("unknown integer operation");
        };
    }

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
                values[0] = ZERO;
                values[1] = ONE;
                for (int i = 2; i <= n; i++) {
                    values[i] = values[i - 1].add(values[i - 2]);
                }
                yield values[n];
            }
            case "constant" -> {
                BigInteger previous = ZERO;
                BigInteger current = ONE;
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
    private static BigInteger recursiveFibonacci(int n) {
        if (n < 2) {
            return BigInteger.valueOf(n);
        }
        return recursiveFibonacci(n - 1).add(recursiveFibonacci(n - 2));
    }

    private static BigInteger memoFibonacci(int n, BigInteger[] cache) {
        if (n < 2) {
            return BigInteger.valueOf(n);
        }
        if (cache[n] == null) {
            cache[n] = memoFibonacci(n - 1, cache).add(memoFibonacci(n - 2, cache));
        }
        return cache[n];
    }

    /** Pascal-row dynamic programming, O(n min(k,n-k)) additions and O(min(k,n-k)) space. */
    public static BigInteger binomial(int n, int k) {
        if (n < 0 || k < 0 || k > n) {
            throw new IllegalArgumentException("require 0 <= k <= n");
        }
        k = Math.min(k, n - k);
        if (k == 0) {
            return ONE;
        }
        BigInteger[] row = new BigInteger[k + 1];
        java.util.Arrays.fill(row, ZERO);
        row[0] = ONE;
        for (long i = 1; i <= n; i++) {
            for (int column = (int)Math.min(i, k); column > 0; column--) {
                row[column] = row[column].add(row[column - 1]);
            }
        }
        return row[k];
    }

    /** Returns [g,x,y], g>=0 and a*x+b*y=g, including signed/zero operands. */
    public static BigInteger[] extendedGcd(BigInteger a, BigInteger b) {
        BigInteger oldR = a.abs();
        BigInteger r = b.abs();
        BigInteger oldX = ONE;
        BigInteger x = ZERO;
        BigInteger oldY = ZERO;
        BigInteger y = ONE;
        while (!r.equals(ZERO)) {
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

    /** Trial division, O(sqrt(n)) worst case; repeated prime factors in ascending order. */
    public static List<Long> factors(long n) {
        if (n < 1) {
            throw new IllegalArgumentException("factorization requires a positive integer");
        }
        List<Long> result = new ArrayList<>();
        while (n % 2 == 0) {
            result.add(2L);
            n /= 2;
        }
        for (long divisor = 3; divisor <= n / divisor; divisor += 2) {
            while (n % divisor == 0) {
                result.add(divisor);
                n /= divisor;
            }
        }
        if (n > 1) {
            result.add(n);
        }
        return result;
    }

    public static double distance(double[] a, double[] b) {
        if (a.length != b.length) {
            throw new IllegalArgumentException("dimension mismatch");
        }
        double result = 0;
        for (int i = 0; i < a.length; i++) {
            finite(a[i]);
            finite(b[i]);
            result = Math.hypot(result, a[i] - b[i]);
        }
        return finite(result);
    }
    public static double finite(double x) {
        if (!Double.isFinite(x)) {
            throw new IllegalArgumentException("finite values required");
        }
        return x;
    }

    public static long[][] multiply(long[][] a, long[][] b) {
        int inner = a.length == 0 ? 0 : a[0].length;
        int columns = b.length == 0 ? 0 : b[0].length;
        for (long[] row : a) {
            if (row.length != inner) {
                throw new IllegalArgumentException("ragged matrix");
            }
        }
        for (long[] row : b) {
            if (row.length != columns) {
                throw new IllegalArgumentException("ragged matrix");
            }
        }
        if (inner != b.length) {
            throw new IllegalArgumentException("matrix dimensions do not match");
        }
        long[][] result = new long[a.length][columns];
        for (int i = 0; i < a.length; i++) {
            for (int j = 0; j < columns; j++) {
                for (int k = 0; k < inner; k++) {
                    result[i][j] =
                        Math.addExact(result[i][j], Math.multiplyExact(a[i][k], b[k][j]));
                }
            }
        }
        return result;
    }

    public static long[] convolve(long[] a, long[] b) {
        if (a.length == 0 || b.length == 0) {
            return new long[0];
        }
        long[] result = new long[Math.addExact(a.length, b.length) - 1];
        for (int i = 0; i < a.length; i++) {
            for (int j = 0; j < b.length; j++) {
                result[i + j] = Math.addExact(result[i + j], Math.multiplyExact(a[i], b[j]));
            }
        }
        return result;
    }

    /** Seeded local generator. Reproducibility is within Java, not across languages. */
    public static final class Generator {
        private final Random random;
        public Generator(long seed) {
            random = new Random(seed);
        }
        public int integer(int low, int high) {
            if (low > high) {
                throw new IllegalArgumentException("empty integer interval");
            }
            return (int)((long)low + random.nextLong((long)high - low + 1));
        }
        public double real(double low, double high) {
            finite(low);
            finite(high);
            if (low > high) {
                throw new IllegalArgumentException("empty real interval");
            }
            if (low == high) {
                return low;
            }
            double fraction = random.nextDouble();
            double value = finite((1 - fraction) * low + fraction * high);
            return value < high ? Math.max(low, value) : Math.nextDown(high);
        }
        public void shuffle(int[] values) {
            for (int i = values.length - 1; i > 0; i--) {
                int j = random.nextInt(i + 1);
                int value = values[i];
                values[i] = values[j];
                values[j] = value;
            }
        }
    }
}
