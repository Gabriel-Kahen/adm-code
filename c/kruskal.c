/*	kruskal.c

	Compute minimum spanning trees of graphs via Kruskal's algorithm.
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
#include <stdlib.h>
#include <stdbool.h>

#include "graph.h"
#include "set_union.h"

#define MAXINT 100007

typedef struct {
    int x, y;   /* adjacency info */
    int weight; /* edge weight, if any */
} edge_pair;

/************************************************************/

int to_edge_array(graph *g, edge_pair edges[]) {
    int i, edge_count; /* counters */
    edgenode *edge;    /* temporary pointer */

    edge_count = 0;
    for (i = 1; i <= g->nvertices; i++) {
        edge = g->edges[i];
        while (edge != NULL) {
            /* An undirected edge appears twice in the adjacency lists; omit loops. */
            if (edge->y > i) {
                edges[edge_count].x = i;
                edges[edge_count].y = edge->y;
                edges[edge_count].weight = edge->weight;
                edge_count = edge_count + 1;
            }
            edge = edge->next;
        }
    }
    return edge_count;
}

int weight_compare(const void *x, const void *y) {
    const edge_pair *left = x;
    const edge_pair *right = y;

    if (left->weight < right->weight) {
        return (-1);
    }

    if (left->weight > right->weight) {
        return (1);
    }

    return (0);
}

/* [[[ kruskal_cut */
long long kruskal(graph *g) {
    int i;                 /* counter */
    union_find components; /* union-find data structure */
    edge_pair *edges;      /* storage for all input edges */
    int edge_count;        /* extracted non-loop edge count */
    long long weight = 0;  /* cost of the minimum spanning tree */

    union_find_init(&components, g->nvertices);

    edges = malloc((g->nedges ? g->nedges : 1) * sizeof(*edges));
    if (edges == NULL) {
        perror("kruskal edge allocation");
        exit(EXIT_FAILURE);
    }
    /* The extracted count excludes self-loops and determines the initialized range. */
    edge_count = to_edge_array(g, edges);
    qsort(edges, edge_count, sizeof(*edges), &weight_compare);

    for (i = 0; i < edge_count; i++) {
        if (!same_component(&components, edges[i].x, edges[i].y)) {
            printf("edge (%d,%d) in MST\n", edges[i].x, edges[i].y);
            weight = weight + edges[i].weight;
            union_sets(&components, edges[i].x, edges[i].y);
        }
    }

    free(edges);
    return (weight);
}
/* ]]] */

int main(void) {
    graph g;
    long long weight;

    read_graph(&g, false);

    /*
    print_graph(&g);
*/

    weight = kruskal(&g);

    printf("Out of Kruskal: weight=%lld \n", weight);

    return 0;
}
