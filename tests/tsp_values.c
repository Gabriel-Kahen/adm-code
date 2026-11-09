/* TSP records cross insertion, inspection, and extraction boundaries by value. */
#include <stdio.h>

#ifdef __cplusplus
#include "../cpp/tsp-pq.hpp"
#else
#include "../c/tsp-pq.h"
#endif

static priority_queue q;

static void print_record(const char *label, tsp_solution *s) {
    printf("%s cost=%.1f n=%d p=%d,%d,%d\n", label, s->cost, s->n,
           s->p[1], s->p[2], s->p[3]);
}

int main(void) {
    tsp_solution source, peek, extracted;
    int i;

    for (i = 0; i <= NMAX; i++) {
        source.p[i] = 0;
    }
    source.cost = 8.0;
    source.n = 3;
    source.p[1] = 1;
    source.p[2] = 2;
    source.p[3] = 3;
    pq_init(&q);
    pq_insert(&q, &source);
    source.cost = 80.0;
    source.n = 1;
    source.p[1] = 9;
    print_record("insert-copy", &q.q[1]);

    source.cost = 4.0;
    source.n = 3;
    source.p[1] = 3;
    source.p[2] = 2;
    source.p[3] = 1;
    pq_insert(&q, &source);
    source.cost = 40.0;
    source.p[1] = 9;
    peek = top_pq(&q);
    peek.cost = -1.0;
    peek.n = 1;
    peek.p[1] = 99;
    print_record("modified-top", &peek);
    print_record("top-copy", &q.q[1]);
    print_record("heap-second", &q.q[2]);

    extracted = extract_min(&q);
    print_record("extracted", &extracted);
    extracted.cost = -2.0;
    extracted.n = 1;
    extracted.p[2] = 99;
    print_record("modified-extracted", &extracted);
    print_record("extract-copy", &q.q[1]);
    extracted = extract_min(&q);
    print_record("last", &extracted);
    printf("empty size=%d flag=%d\n", q.n, empty_pq(&q));
    return 0;
}
