#define main floyd_demo_main
#include "floyd.c"
#undef main

int main(void) {
    int cases;
    scanf("%d", &cases);
    while (cases--) {
        adjacency_matrix graph;
        int directed;
        scanf("%d", &directed);
        read_adjacency_matrix(&graph, directed);
        floyd(&graph);
        printf("RESULT");
        for (int from = 1; from <= graph.nvertices; from++) {
            for (int to = 1; to <= graph.nvertices; to++) {
                if (graph.weight[from][to] == MAXINT)
                    printf(" INF");
                else
                    printf(" %lld", graph.weight[from][to]);
            }
        }
        printf("\n");
    }
    return 0;
}
