#define main spanning_tree_demo_main
#ifdef TEST_KRUSKAL
#include "kruskal.c"
#else
#include "prim.c"
#endif
#undef main

int main(void) {
    int cases;
    scanf("%d", &cases);
    while (cases--) {
        graph input;
        read_graph(&input, false);
        puts("CASE");
#ifdef TEST_KRUSKAL
        long long total = kruskal(&input);
#else
        long long total = prim(&input, 1);
        if (parent[1] != -1)
            return 1;
        for (int vertex = 2; vertex <= input.nvertices; vertex++) {
            int current = vertex, steps = 0;
            while (current != 1) {
                if (++steps >= input.nvertices)
                    return 2;
                current = parent[current];
                if (current < 1 || current > input.nvertices)
                    return 3;
            }
        }
#endif
        printf("RESULT %lld\n", total);
    }
    return 0;
}
