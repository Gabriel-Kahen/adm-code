/*	netflow.c

	Network flow implementation -- Ford-Fulkerson augmenting path algorithm.

	by: Steven Skiena
	begun: September 19, 2002

	This algorithm requires its own special graph type, to allow for
	flows and residual flow fields.
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


#include "bool.h"
#include "queue.h"
#include <stdio.h>
#include <stdlib.h>
#include "geometry.h"


#define	MAXV		100		/* maximum number of vertices */
#define MAXDEGREE MAXV		/* one coalesced arc per destination */


typedef struct {
	int v;				/* neighboring vertex */
	long long capacity;			/* capacity of edge */
	long long flow;			/* signed net flow; reverse edge stores its negative */
	long long residual;			/* residual capacity of edge */
} edge;

typedef struct {
	edge edges[MAXV+1][MAXDEGREE+1];	/* adjacency info */
	int degree[MAXV+1];		/* outdegree of each vertex */
	int nvertices;			/* number of vertices in the graph */
	int nedges;			/* number of edges in the graph */
} flow_graph;



main()
{
	flow_graph g;			/* graph to analyze */
	int source, sink;		/* source and sink vertices */
	long long flow;			/* total flow */
	int i;				/* counter */

	scanf("%d %d",&source,&sink);
	read_flow_graph(&g,TRUE);

	netflow(&g,source,sink);

	print_flow_graph(&g);

	flow = 0;
	for (i=0; i<g.nvertices; i++)
		flow += g.edges[source][i].flow;

	printf("total flow = %lld\n",flow);
}



initialize_graph(g)
flow_graph *g;				/* graph to initialize */
{
	int i;				/* counter */

	g -> nvertices = 0;
	g -> nedges = 0;

	for (i=0; i<=MAXV; i++) g->degree[i] = 0;
}

read_flow_graph(g,directed)
flow_graph *g;				/* graph to initialize */
bool directed;				/* is this graph directed? */
{
	int i;				/* counter */
	int m;				/* number of edges */
	int x,y,w;			/* placeholder for edge and weight */

	initialize_graph(g);

    if (scanf("%d %d\n", &(g->nvertices), &m) != 2 ||
        g->nvertices < 1 || g->nvertices > MAXV || m < 0) {
        fprintf(stderr, "Invalid flow graph size\n");
        exit(EXIT_FAILURE);
    }

	for (i=1; i<=m; i++) {
        if (scanf("%d %d %d\n", &x, &y, &w) != 3 ||
            x < 1 || x > g->nvertices || y < 1 || y > g->nvertices || w < 0) {
            fprintf(stderr, "Invalid flow edge\n");
            exit(EXIT_FAILURE);
        }
		insert_flow_edge(g,x,y,directed,w);
	}
}

edge *find_edge(flow_graph *g, int x, int y);

insert_flow_edge(flow_graph *g, int x, int y, bool directed, int w)
{
    edge *existing;
    if (x < 1 || x > MAXV || y < 1 || y > MAXV || w < 0) {
        fprintf(stderr, "Invalid flow edge\n");
        exit(EXIT_FAILURE);
    }
    existing = find_edge(g, x, y);
    /* Parallel arcs share a single residual-capacity entry. */
    if (existing != NULL) {
        existing->capacity += w;
        existing->residual += w;
        if (!directed) insert_flow_edge(g, y, x, TRUE, w);
        return;
    }

    if (g->degree[x] >= MAXDEGREE) {
        fprintf(stderr, "Flow adjacency capacity exceeded\n");
        exit(EXIT_FAILURE);
    }

	g->edges[x][g->degree[x]].v = y;
	g->edges[x][g->degree[x]].capacity = w;
	g->edges[x][g->degree[x]].flow = 0;
	g->edges[x][g->degree[x]].residual = w;
	g->degree[x] ++;

	if (directed == FALSE)
		insert_flow_edge(g,y,x,TRUE,w);
	else
		g->nedges ++;
}


edge *find_edge(flow_graph *g, int x, int y)
{
	int i;				/* counter */

	for (i=0; i<g->degree[x]; i++) 
		if (g->edges[x][i].v == y) 
			return( &g->edges[x][i] );

	return(NULL);
}


add_residual_edges(flow_graph *g)
{
	int i,j;			/* counters */

	for (i=1; i<=g->nvertices; i++) 
		for (j=0; j<g->degree[i]; j++)
			if (find_edge(g,g->edges[i][j].v,i) == NULL)
				insert_flow_edge(g,g->edges[i][j].v,i,TRUE,0);
}


print_flow_graph(flow_graph *g)
{
	int i,j;			/* counters */

	for (i=1; i<=g->nvertices; i++) {
		printf("%d: ",i);
		for (j=0; j<g->degree[i]; j++)
			printf(" %d(%lld,%lld,%lld)",g->edges[i][j].v,
				g->edges[i][j].capacity,
				g->edges[i][j].flow,
				g->edges[i][j].residual);
		printf("\n");
	}
}

bool processed[MAXV+1];		/* which vertices have been processed */
bool discovered[MAXV+1];          /* which vertices have been found */
int parent[MAXV+1];		/* discovery relation */

bool finished = FALSE;          /* if true, cut off search immediately */


initialize_search(g)
flow_graph *g;				/* graph to traverse */
{
        int i;                          /* counter */

        for (i=1; i<=g->nvertices; i++) {
                processed[i] = FALSE;
                discovered[i] = FALSE;
                parent[i] = -1;
        }
}


bfs(flow_graph *g, int start)
{
	queue q;			/* queue of vertices to visit */
	int v;				/* current vertex */
	int i;				/* counter */

	init_queue(&q);
	enqueue(&q,start);
	discovered[start] = TRUE;

	while (empty(&q) == FALSE) {
		v = dequeue(&q);
		process_vertex_early(v);
		processed[v] = TRUE;
		for (i=0; i<g->degree[v]; i++) 
		    if (valid_edge(g->edges[v][i]) == TRUE) {
			if (discovered[g->edges[v][i].v] == FALSE) {
				enqueue(&q,g->edges[v][i].v);
				discovered[g->edges[v][i].v] = TRUE;
				parent[g->edges[v][i].v] = v;
			}
			if (processed[g->edges[v][i].v] == FALSE) 
				process_edge(v,g->edges[v][i].v);
		    }
		process_vertex_late(v);
	}
}


bool valid_edge(edge e)
{
	if (e.residual > 0) return (TRUE);
	else return(FALSE);
}

process_vertex_early(v)
int v;					/* vertex to process */
{
}

process_vertex_late(v)
int v;                                  /* vertex to process */
{
}

process_edge(x,y)
int x,y;                                /* edge to process */
{
}




int find_path(start,end,parents)
int start;				/* first vertex on path */
int end;				/* last vertex on path */
int parents[];				/* array of parent pointers */
{
    if (end == -1) {
        printf("\nNo path");
        return 0;
    }
    if (start == end) {
        printf("\n%d", start);
    } else {
        if (!find_path(start, parents[end], parents)) return 0;
        printf(" %d", end);
    }
    return 1;
}

long long path_volume(flow_graph *g, int start, int end, int parents[])
{
	edge *e;			/* edge in question */
	edge *find_edge();

	if (parents[end] == -1) return(0);

	e = find_edge(g,parents[end],end);

	if (start == parents[end])
		return(e->residual);
	else
		return( min(path_volume(g,start,parents[end],parents), e->residual) );
}


augment_path(flow_graph *g, int start, int end, int parents[], long long volume)
{
	edge *e;			/* edge in question */
	edge *find_edge();

	if (start == end) return;

	e = find_edge(g,parents[end],end);
	e->flow += volume;
	e->residual -= volume;
	
	e = find_edge(g,end,parents[end]);
	e->flow -= volume;
	e->residual += volume;

	augment_path(g,start,parents[end],parents,volume);
}


netflow(flow_graph *g, int source, int sink)
{
	long long volume;			/* weight of the augmenting path */

    if (source < 1 || source > g->nvertices || sink < 1 ||
        sink > g->nvertices || source == sink) {
        fprintf(stderr, "Invalid flow terminals\n");
        exit(EXIT_FAILURE);
    }

	add_residual_edges(g);

	initialize_search(g);
	bfs(g,source);

	volume = path_volume(g, source, sink, parent);

	while (volume > 0) {
		augment_path(g,source,sink,parent,volume);
		initialize_search(g);
		bfs(g,source);
		volume = path_volume(g, source, sink, parent);
	}
}
