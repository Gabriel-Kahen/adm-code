#include <limits.h>
#include <errno.h>
/*	binomial.c
	Compute the binomial coefficients using dynamic programming 

	begun: February 10, 2002
	by: Steven Skiena
*/

#define MAXN 45    /* largest n or m */
#define UNKNOWN -1 /* contents denote an empty cell */

long f[MAXN + 1]; /* array for caching computed fib values */

/* Returns -1 with errno set for invalid arguments or an unrepresentable result. */
long binomial_coefficient(int n, int k) {
    long bc[MAXN + 1] = {0};
    int i, j, last;

    errno = 0;
    if (n < 0 || n > MAXN || k < 0 || k > n) {
        errno = EDOM;
        return -1;
    }
    if (k > n - k) {
        k = n - k;
    }
    bc[0] = 1;
    for (i = 1; i <= n; i++) {
        last = i < k ? i : k;
        for (j = last; j > 0; j--) {
            if (bc[j] > LONG_MAX - bc[j - 1]) {
                errno = ERANGE;
                return -1;
            }
            bc[j] += bc[j - 1];
        }
    }
    return bc[k];
}

long fib_r(int n) {
    if (n == 0)
        return (0);
    if (n == 1)
        return (1);

    return (fib_r(n - 1) + fib_r(n - 2));
}

long fib_c(int n) {
    if (f[n] == UNKNOWN)
        f[n] = fib_c(n - 1) + fib_c(n - 2);

    return (f[n]);
}

long fib_c_driver(int n) {
    int i; /* counter */

    f[0] = 0;
    f[1] = 1;

    for (i = 2; i <= n; i++)
        f[i] = UNKNOWN;

    return (fib_c(n));
}

long fib_dp(int n) {
    int i;            /* counter */
    long f[MAXN + 1]; /* array for caching computed fib values */

    f[0] = 0;
    f[1] = 1;

    for (i = 2; i <= n; i++)
        f[i] = f[i - 1] + f[i - 2];

    return (f[n]);
}

long fib_dp2(int n) {
    int i;                     /* counter */
    long back1 = 1, back2 = 0; /* last two values of f[n] */
    long next;                 /* placeholder for sum */

    if (n == 0)
        return (0);

    /*
        back2 = 0;
        back1 = 1;
*/
    for (i = 2; i < n; i++) {
        next = back1 + back2;
        back2 = back1;
        back1 = next;
    }

    return (back1 + back2);
}

main() {
    int i;
    long fib_r(), fib_c_driver();

    for (i = 0; i < MAXN; i++) {
        printf("fib_c(%d) = %d\n", i, fib_c_driver(i));
    }

    for (i = 0; i < MAXN; i++) {
        printf("fib_dp(%d) = %d\n", i, fib_dp(i));
    }

    for (i = 0; i < MAXN; i++) {
        printf("fib_dp2(%d) = %d\n", i, fib_dp2(i));
    }

    for (i = 0; i < MAXN; i++) {
        printf("fib(%d) = %d\n", i, fib_r(i));
    }
}
