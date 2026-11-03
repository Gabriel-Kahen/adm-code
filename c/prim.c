/*    prim.c

    Compute minimum spanning trees of graphs via Dijkstra/Prim's algorithm.
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

#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#include "bfs-dfs.h"

#define MAXINT (LLONG_MAX / 4)

/************************************************************/
/* [[[ prim_cut */
long long prim(graph *g, int start) {
    int i;
    edgenode *edge;
    bool in_tree[MAXV + 1];
    long long distance[MAXV + 1]; /* cheapest known edge from the tree */
    int vertex, neighbor;
    long long next_distance;
    long long tree_weight = 0;

    for (i = 1; i <= g->nvertices; i++) {
        in_tree[i] = false;
        distance[i] = MAXINT;
        parent[i] = -1;
    }

    distance[start] = 0;
    vertex = start;

    /* Grow the tree in start's connected component; other parents remain -1. */
    while (!in_tree[vertex]) {
        in_tree[vertex] = true;
        if (vertex != start) {
            printf("edge (%d,%d) in tree \n", parent[vertex], vertex);
            tree_weight = tree_weight + next_distance;
        }
        edge = g->edges[vertex];
        while (edge != NULL) {
            neighbor = edge->y;
            if ((distance[neighbor] > edge->weight) && (!in_tree[neighbor])) {
                distance[neighbor] = edge->weight;
                parent[neighbor] = vertex;
            }
            edge = edge->next;
        }

        next_distance = MAXINT;
        for (i = 1; i <= g->nvertices; i++) {
            if ((!in_tree[i]) && (next_distance > distance[i])) {
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
    long long weight;

    read_graph(&g, false);

    weight = prim(&g, 1);

    printf("Out of Prim: weight = %lld \n", weight);

    return 0;
}
