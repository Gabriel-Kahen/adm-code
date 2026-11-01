/*	dijkstra.c

	Compute shortest paths in weighted graphs using Dijkstra's algorithm
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

#include <limits.h>
#include <stdio.h>
#include <stdlib.h>

#include <stdbool.h>
#include "bfs-dfs.h"

#define MAXINT (LLONG_MAX / 4)

/* Dijkstra requires nonnegative edge weights. Unreachable vertices keep parent -1. */

/* [[[ dijkstra_cut */
long long dijkstra(graph *g, int start) {
    int i;
    edgenode *edge;
    bool settled[MAXV + 1];
    long long distance[MAXV + 1]; /* shortest known distance from start */
    int vertex, neighbor;
    long long next_distance;
    long long tree_weight = 0;

    for (i = 1; i <= g->nvertices; i++) {
        settled[i] = false;
        distance[i] = MAXINT;
        parent[i] = -1;
    }

    distance[start] = 0;
    vertex = start;

    while (!settled[vertex]) {
        settled[vertex] = true;
        if (vertex != start) {
            printf("edge (%d,%d) in tree \n", parent[vertex], vertex);
            /* The distance difference is this parent edge's weight, not a full path length. */
            tree_weight += distance[vertex] - distance[parent[vertex]];
        }
        edge = g->edges[vertex];
        while (edge != NULL) {
            neighbor = edge->y;
            if (distance[neighbor] > (distance[vertex] + edge->weight)) {
                distance[neighbor] = distance[vertex] + edge->weight;
                parent[neighbor] = vertex;
            }
            edge = edge->next;
        }

        /* If none is reachable, vertex stays settled and the outer loop stops. */
        next_distance = MAXINT;
        for (i = 1; i <= g->nvertices; i++) {
            if ((!settled[i]) && (next_distance > distance[i])) {
                next_distance = distance[i];
                vertex = i;
            }
        }
    }

    return (tree_weight);
}
/* ]]] */

int main(void) {
    graph g;
    int i;
    long long weight;

    read_graph(&g, false);
    weight = dijkstra(&g, 1);

    printf("Total SPST edgeweight = %lld \n", weight);

    for (i = 1; i <= g.nvertices; i++) {
        find_path(1, i, parent);
    }
    printf("\n");

    return 0;
}
