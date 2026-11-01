#include <stdio.h>
#include <limits.h>
#include <errno.h>
/*	binomial.c
	Compute the binomial coefficients using dynamic programming 

	begun: February 10, 2002
	by: Steven Skiena
*/

#define	MAXN	100		/* largest n or m */

/* Returns -1 with errno set for invalid arguments or an unrepresentable result. */
long binomial_coefficient(int n, int k) {
    long bc[MAXN+1] = {0};
    int i, j, last;

    errno = 0;
    if (n < 0 || n > MAXN || k < 0 || k > n) {
        errno = EDOM;
        return -1;
    }
    if (k > n-k) {
        k = n-k;
    }
    bc[0] = 1;
    for (i = 1; i <= n; i++) {
        last = i < k ? i : k;
        for (j = last; j > 0; j--) {
            if (bc[j] > LONG_MAX-bc[j-1]) {
                errno = ERANGE;
                return -1;
            }
            bc[j] += bc[j-1];
        }
    }
    return bc[k];
}

main()
{
	int a, b;
    long coefficient;
	long binomial_coefficient();

	while (1) {
        if (scanf("%d %d", &a, &b) != 2) {
            break;
        }
        coefficient = binomial_coefficient(a, b);
        if (coefficient < 0) {
            perror("binomial coefficient");
            return 1;
        }
        printf("%ld\n", coefficient);
	}
}

