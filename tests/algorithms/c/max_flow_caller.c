#define main flow_demo_main
#include "netflow.c"
#undef main

int main(void) {
    int cases;
    scanf("%d", &cases);
    while (cases--) {
        flow_graph graph;
        long long balance[MAXV + 1] = {0};
        read_flow_graph(&graph, true);
        netflow(&graph, 1, graph.nvertices);
        for (int vertex = 1; vertex <= graph.nvertices; vertex++) {
            for (edgenode *edge = graph.edges[vertex]; edge; edge = (edgenode *)edge->next) {
                edgenode *reverse = find_edge(&graph, edge->v, vertex);
                if (!reverse || edge->flow != -reverse->flow)
                    return 1;
                if (edge->residual != edge->capacity - edge->flow || edge->residual < 0)
                    return 2;
                balance[vertex] += edge->flow;
            }
        }
        for (int vertex = 2; vertex < graph.nvertices; vertex++) {
            if (balance[vertex] != 0)
                return 3;
        }
        if (balance[1] != -balance[graph.nvertices])
            return 4;
        printf("RESULT %lld\n", balance[1]);
    }
    return 0;
}
