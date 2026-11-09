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
    int moves[][2] = {{1, 5}, {5, 1}, {1, 3}, {3, 1}, {2, 2}, {2, 2}};
    int i;
    int j;
    int n;
    double delta;

    initialize_solution(4, &s);
    s.p[0] = -7;
    s.p[5] = -9;
    random_solution(&s);
    for (i = 0; i < 3; i++) {
        prefix[i] = s.p[i + 1];
    }
    qsort(prefix, 3, sizeof(prefix[0]), compare_ints);
    printf("random prefix=%d,%d,%d last=%d left=%d right=%d\n",
           prefix[0], prefix[1], prefix[2], s.p[4], s.p[0], s.p[5]);

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

    /* Five cities give the nonadjacent swap a genuine cost change. */
    t.n = 5;
    t.p[5].x = 8;
    t.p[5].y = 7;
    initialize_solution(5, &s);
    for (i = 0; i < 6; i++) {
        delta = transition(&s, &t, moves[i][0], moves[i][1]);
        printf("move %d,%d delta=%.1f cost=%.1f tour",
               moves[i][0], moves[i][1], delta, solution_cost(&s, &t));
        for (j = 1; j <= s.n; j++) {
            printf(" %d", s.p[j]);
        }
        printf("\n");
    }

    /* The C pointer starts at p[1]; its n-1 prefix can be empty. */
    for (n = 1; n <= 2; n++) {
        initialize_solution(n, &s);
        s.p[0] = -7;
        s.p[n + 1] = -9;
        random_solution(&s);
        printf("small n=%d left=%d tour", n, s.p[0]);
        for (j = 1; j <= n; j++) {
            printf(" %d", s.p[j]);
        }
        printf(" right=%d\n", s.p[n + 1]);
    }
    return 0;
}
