/*	order.c

	Demonstrate traversal orders on a grid.

	by: Steven Skiena
	begun: July 14, 2002
*/

/*
Copyright 2003 by Steven S. Skiena; all rights reserved. 

Permission is granted for use in non-commerical applications
provided this copyright notice remains intact and unchanged.

This program appears in my book:

"Programming Challenges: The Programming Contest Training Manual"
by Steven Skiena and Miguel Revilla, Springer-Verlag, New York 2003.

See our website www.programming-challenges.com for additional information.

This book can be ordered from Amazon.com at

http://www.amazon.com/exec/obidos/ASIN/0387001638/thealgorithmrepo/

*/


#include "geometry.h"

row_major(int n, int m)
{
	int i,j;	/* counters */

	for (i=1; i<=n; i++)
		for (j=1; j<=m; j++)
			process(i,j);
}

column_major(int n, int m)
{
	int i,j;	/* counters */

	for (j=1; j<=m; j++)
		for (i=1; i<=n; i++)
			process(i,j);
}


snake_order(int n, int m)
{
	int i,j;	/* counters */

	for (i=1; i<=n; i++)
		for (j=1; j<=m; j++)
			process(i, j + (m+1-2*j) * ((i+1) % 2));
}

diagonal_order(int n, int m)
{
    int d, row;
    int first, last;

    for (d = 1; d <= n + m - 1; d++) {
        first = max(1, d + 1 - m);
        last = min(n, d);
        for (row = first; row <= last; row++) {
            process(row, d + 1 - row);
        }
    }
}

process(int i, int j)
{
	printf("(%d,%d)\n",i,j);
}

main()
{
	printf("row_major\n");
	row_major(5,5);

	printf("\ncolumn_major\n");
        column_major(3,3);

	printf("\nsnake_order\n");
        snake_order(5,5);

	printf("\ndiagonal_order\n");
        diagonal_order(3,4);

        printf("\ndiagonal_order\n");
        diagonal_order(4,3);


}

