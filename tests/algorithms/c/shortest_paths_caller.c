/* A caller compiled for either Dijkstra or BFS by the Python test. */
#include <stdio.h>
#ifdef TEST_DIJKSTRA
#define main dijkstra_demo_main
#include "dijkstra.c"
#undef main
#else
#include "bfs-dfs.h"
void process_vertex_early(int vertex) {}
void process_vertex_late(int vertex) {}
void process_edge(int from, int to) {}
#endif

int main(void) {
    int cases;
    scanf("%d", &cases);
    while (cases--) {
        graph input;
        int directed, start;
        scanf("%d %d", &directed, &start);
        read_graph(&input, directed);
#ifdef TEST_DIJKSTRA
        dijkstra(&input, start);
#else
        initialize_search(&input);
        bfs(&input, start);
#endif
        printf("RESULT");
        for (int vertex = 1; vertex <= input.nvertices; vertex++) {
            printf(" %d", parent[vertex]);
        }
        printf("\n");
    }
    return 0;
}
