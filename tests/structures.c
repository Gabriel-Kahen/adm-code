/* Snapshot the original auxiliary representations, not just final answers. */
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#ifdef __cplusplus
#include "../cpp/queue.hpp"
#include "../cpp/stack.hpp"
#include "../cpp/priority_queue.hpp"
#include "../cpp/set_union.hpp"
#include "../cpp/graph.hpp"
#else
#include "../c/queue.h"
#include "../c/stack.h"
#include "../c/priority_queue.h"
#include "../c/set_union.h"
#include "../c/graph.h"
#endif

int heap_compare(priority_queue *q, int i, int count, int x);
int find(union_find *s, int x);
void insert_edge(graph *g, int x, int y, bool directed);
void delete_edge(graph *g, int x, int y, bool directed);

int main(void) {
    queue q;
    stack s;
    priority_queue h;
    union_find sets;
    graph g;
    int values[] = {4, 1, 7, 1, -3, 9, 2};
    int i, first, second;
    long sum = 0;

    init_queue(&q);
    for (i = 0; i < QUEUESIZE; i++) {
        enqueue(&q, i);
    }
    for (i = 0; i < 17; i++) {
        dequeue(&q);
    }
    for (i = QUEUESIZE; i < QUEUESIZE + 17; i++) {
        enqueue(&q, i);
    }
    printf("queue first=%d last=%d count=%d head=%d tail=%d\n", q.first, q.last,
           q.count, headq(&q), q.q[q.last]);
    while (!empty_queue(&q)) {
        sum += dequeue(&q);
    }
    printf("queue sum=%ld count=%d\n", sum, q.count);

    init_stack(&s);
    for (i = 0; i < STACKSIZE; i++) {
        push(&s, i);
    }
    push(&s, STACKSIZE);
    first = pop(&s);
    second = pop(&s);
    printf("stack first=%d second=%d top=%d count=%d\n", first, second, s.top,
           s.count);

    pq_init(&h);
    for (i = 0; i < (int)(sizeof(values) / sizeof(values[0])); i++) {
        pq_insert(&h, values[i]);
    }
    printf("heap array: ");
    print_pq(&h);
    printf("heap_compare=%d\n", heap_compare(&h, 1, 4, 3));
    printf("heap sorted: ");
    while (!empty_pq(&h)) {
        printf("%d ", extract_min(&h));
    }
    printf("\n");

    union_find_init(&sets, 6);
    union_sets(&sets, 2, 3);
    union_sets(&sets, 4, 5);
    union_sets(&sets, 4, 6);
    union_sets(&sets, 2, 4);
    printf("union root=%d\n", find(&sets, 3));
    print_union_find(&sets);

    initialize_graph(&g, false);
    g.nvertices = 4;
    insert_edge(&g, 1, 2, false);
    insert_edge(&g, 1, 3, false);
    insert_edge(&g, 1, 4, false);
    delete_edge(&g, 1, 3, false);
    print_graph(&g);
    printf("graph nedges=%d degree1=%d\n", g.nedges, g.degree[1]);
    for (i = 1; i <= g.nvertices; i++) {
        edgenode *edge = g.edges[i];
        while (edge != NULL) {
            edgenode *next = edge->next;
            free(edge);
            edge = next;
        }
    }
    return 0;
}
