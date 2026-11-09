#pragma once

/*	Header for Simulated Annealing Package

	These are the global variables needed for the system.
	The parameters which are most likely to be needed to
	modify in adapting it to another problem are at the top
	of the file.
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

#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#include "tsp.hpp"

#define TRACE_OUTPUT FALSE    /* print the swaps as they happen */
#define PRINT_FREQUENCY 10000 /* how often we report progress */

/**************** Simulated Annealing Constants **************************/

/* Repeated attempts let the caller compare independent heuristic runs. */
#define REPEAT_COUNT 1

/* Initial temperature and cooling rate control how readily uphill moves are accepted. */
#define INITIAL_TEMPERATURE 1
#define COOLING_FRACTION 0.998

/* Tune these together: more temperatures or proposals increase the search effort. */
#define COOLING_STEPS 1000
#define STEPS_PER_TEMP 1000

#define E 2.718 /* approximation retained for historical examples */

/* Problem-specific Boltzmann constant: tune the acceptance of uphill moves. */
#define K 0.01

/*=========================================================================*/

/*  The stuff below is less likely to change in adapting to new
    problems, but look for yourself before leaping.
*/

#define ERROR "ERROR"   /* string denoting error id */
#define ERROR_VALUE 0.0 /* float denoting error value */

void repeated_annealing(tsp_instance *t, int nsamples, tsp_solution *bestsol);
void repeated_hill_climbing(tsp_instance *t, int nsamples, tsp_solution *bestsol);
void random_sampling(tsp_instance *t, int nsamples, tsp_solution *bestsol);
