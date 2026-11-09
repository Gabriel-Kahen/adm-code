/* Exercise offset array pointers and the original swap/undo transition. */
#define main tsp_example_main
#ifdef __cplusplus
#include "../cpp/tsp.cpp"
#else
#include "../c/tsp.c"
#endif
#undef main

static int compare_ints(const void *left, const void *right) {
    int a = *(const int *)left;
    int b = *(const int *)right;
    return (a > b) - (a < b);
}

int main(void) {
    tsp_solution s;
    tsp_instance t;
    int prefix[3];
    int i;
    double delta;

    initialize_solution(4, &s);
    random_solution(&s);
    for (i = 0; i < 3; i++) {
        prefix[i] = s.p[i + 1];
    }
    qsort(prefix, 3, sizeof(prefix[0]), compare_ints);
    printf("random prefix=%d,%d,%d last=%d\n", prefix[0], prefix[1], prefix[2], s.p[4]);

    t.n = 4;
    t.p[1].x = 0;
    t.p[1].y = 0;
    t.p[2].x = 3;
    t.p[2].y = 0;
    t.p[3].x = 3;
    t.p[3].y = 4;
    t.p[4].x = 0;
    t.p[4].y = 4;
    initialize_solution(4, &s);
    printf("initial cost=%.1f\n", solution_cost(&s, &t));
    delta = transition(&s, &t, 1, 2);
    printf("forward delta=%.1f cost=%.1f\n", delta, solution_cost(&s, &t));
    delta = transition(&s, &t, 2, 1);
    printf("reverse delta=%.1f cost=%.1f\n", delta, solution_cost(&s, &t));
    printf("tour");
    for (i = 1; i <= s.n; i++) {
        printf(" %d", s.p[i]);
    }
    printf("\n");
    return 0;
}
