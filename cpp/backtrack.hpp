#pragma once

/*	backtrack.h
	A header file for generic backtracking
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

#ifndef BACKTRACK_H
#define BACKTRACK_H

#define MAXCANDIDATES 100 /* maximum extensions of one prefix */
#define NMAX 100          /* maximum solution length */

typedef char *data; /* application context; retained for the book examples */

/* Reset finished to 0 before each independent search. A callback may set
 * it to nonzero to stop; every active move is still undone before returning. */
extern int finished; /* Preserve the original int-backed control flag. */

/* Search extensions of the one-based prefix a[1..k]. Slot a[0] is unused;
 * allocate at least NMAX + 1 elements for a full-length solution. */
void backtrack(int a[], int k, data input);

/* Applications supply these callbacks; the engine owns the traversal order. */
int is_a_solution(int a[], int k, data input);
void process_solution(int a[], int k, data input);

/* Fill c[0..*nc-1], with 0 <= *nc <= MAXCANDIDATES. The current prefix is
 * a[1..k-1]; the engine writes each candidate into a[k] before make_move. */
void construct_candidates(int a[], int k, data input, int c[], int *nc);

/* Apply and undo exactly one extension. unmake_move must reverse make_move,
 * including when process_solution requests an early stop via finished. */
void make_move(int a[], int k, data input);
void unmake_move(int a[], int k, data input);

#endif /* BACKTRACK_H */
