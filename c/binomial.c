#include <limits.h>
#include <errno.h>
/*	binomial.c
	Compute the binomial coefficients using dynamic programming 
	by: Steven Skiena
*/

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
or http://www.amazon.com/exec/obidos/ASIN/0387001638/thealgorithmrepo/
*/

#include <stdio.h>

#define MAXN 100 /* largest n or k */

/* compute n choose k */

/* [[[ binomial_coeff_cut */
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
/* ]]] */

int main(void) {
    int a, b, n, i;
    long coefficient;

    scanf("%d", &n);

    for (i = 0; i < n; i++) {
        scanf("%d %d", &a, &b);
        coefficient = binomial_coefficient(a, b);
        if (coefficient < 0) {
            perror("binomial coefficient");
            return 1;
        }
        printf("%d choose %d = %ld\n", a, b, coefficient);
    }

    return 0;
}
