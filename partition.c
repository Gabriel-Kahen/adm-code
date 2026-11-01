/*  partition.c

    Optimally balance partitions using dynamic programming 
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
or https://www.amazon.com/exec/obidos/ASIN/0387001638/thealgorithmrepo/
*/




#include <stdio.h>

#define MAXN    45        /* largest number of books */
#define MAXK    10        /* largest number of dividers */


long long max(long long a, long long b) {
    return((a > b) ? a : b);
} 

void read_partition(int s[], int *n, int *k) {
    int i;    /* counter */

    scanf("%d %d\n", n, k);
    for (i = 1; i <= *n; i++) {
        scanf("%d\n", &(s[i]));
    }
}

/* [[[ print_books_297_cut */
void print_books(int s[], int start, int end) {
    int i;    /* counter */

    printf("\{");
    for (i = start; i <= end; i++) {
        printf(" %d ", s[i]);
    }
    printf("}\n");
}
/* ]]] */

void print_matrix(long long m[MAXN+1][MAXK+1], int n, int k) {
    int i,j;    /* counters */

    printf("\n");
    for (i = 1; i <=n; i++) {
        for (j = 1; j <= k; j++) { 
            printf(" %lld ", m[i][j]);
        }
        printf("\n");
    }
}

/* [[[ reconstruct_partition_297_cut */
void reconstruct_partition(int s[],int d[MAXN+1][MAXK+1], int n, int k) {
    if (k == 1) {
        print_books(s, 1, n);
    } else {
        reconstruct_partition(s, d, d[n][k], k-1);
        print_books(s, d[n][k]+1, n);
    }
}
/* ]]] */

/* [[[ partition_296_cut */
void partition(int s[], int n, int k) {
    long long p[MAXN+1];            /* prefix sums array */
    long long m[MAXN+1][MAXK+1];    /* DP table for values */
    int d[MAXN+1][MAXK+1];    /* DP table for dividers */
    long long cost;                 /* test split cost */
    int i,j,x;                /* counters */

    if (n < 1 || n > MAXN || k < 1 || k > MAXK || k > n) {
        fprintf(stderr, "invalid partition dimensions\n");
        return;
    }

    p[0] = 0;                 /* construct prefix sums */
    for (i = 1; i <= n; i++) {
        p[i] = p[i-1] + s[i];
    }

    for (i = 1; i <= n; i++) {
        m[i][1] = p[i];    /* initialize boundaries */
    }

    for (i = 2; i <= n; i++) {   /* evaluate main recurrence */
        for (j = 2; j <= k && j <= i; j++) {
            for (x = j-1; x <= (i-1); x++) {
                cost = max(m[x][j-1], p[i]-p[x]);
                if (x == j-1 || m[i][j] > cost) {
                    m[i][j] = cost;
                    d[i][j] = x;
                }
            }
        }
    }  
    reconstruct_partition(s, d, n, k);    /* print book partition */
}
/* ]]] */

int main(void) {
    int s[MAXN+1];    /* book thicknesses to partition */
    int n;            /* how many books? */
    int k;            /* how many partitions? */

    read_partition(s, &n, &k);
    partition(s, n, k);

    return 0;
}
