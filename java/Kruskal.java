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

public class Kruskal {
    public static final int TREE = 0; /* tree edge */
    public static final int BACK = 1; /* back edge */
    public static final int CROSS = 2; /* cross edge */
    public static final int FORWARD = 3; /* forward edge */
    public static final int MAXV = 100; /* maximum number of vertices */
    public static final int SET_SIZE = 1000;
    public static final int MAXINT = 100007;
    public static class edge_pair {
        int x = 0; /* adjacency info */
        int y = 0; /* adjacency info */
        int weight = 0; /* edge weight, if any */
    }

    public static int to_edge_array(Graph.graph g, Kruskal.edge_pair[] edges) {
        int i = 0; /* counters */
        int edge_count = 0;
        Graph.edgenode edge = null; /* temporary pointer */
        edge_count = 0;
        for (i = 1; (i <= g.nvertices); i++) {
            edge = g.edges[i];
            while ((edge != null)) {
                /* An undirected edge appears twice in the adjacency lists; omit loops. */
                if ((edge.y > i)) {
                    edges[edge_count].x = i;
                    edges[edge_count].y = edge.y;
                    edges[edge_count].weight = edge.weight;
                    edge_count = (edge_count + 1);
                }
                edge = edge.next;
            }
        }
        return edge_count;
    }

    public static int weight_compare(Object x, Object y) {
        Kruskal.edge_pair left = ((Kruskal.edge_pair)x);
        Kruskal.edge_pair right = ((Kruskal.edge_pair)y);
        if ((left.weight < right.weight)) {
            return (-1);
        }
        if ((left.weight > right.weight)) {
            return 1;
        }
        return 0;
    }

    public static long kruskal(Graph.graph g) {
        int i = 0; /* counter */
        SetUnion.union_find components = new SetUnion.union_find(); /* union-find data structure */
        Kruskal.edge_pair[] edges = null; /* storage for all input edges */
        int edge_count = 0; /* extracted non-loop edge count */
        long weight = 0; /* cost of the minimum spanning tree */
        SetUnion.union_find_init(components, g.nvertices);
        edges = new Kruskal.edge_pair[((g.nedges != 0) ? g.nedges : 1)];
        for (int _i0 = 0; _i0 < edges.length; _i0++) edges[_i0] = new edge_pair();
        if ((edges == null)) {
            System.err.println("kruskal edge allocation");
            System.exit(1);
        }
        /* The extracted count excludes self-loops and determines the initialized range. */
        edge_count = to_edge_array(g, edges);
        java.util.Arrays.sort(edges, 0, (0 + edge_count), Kruskal::weight_compare);
        for (i = 0; (i < edge_count); i++) {
            if (!(SetUnion.same_component(components, edges[i].x, edges[i].y))) {
                C.printf("edge (%d,%d) in MST\n", edges[i].x, edges[i].y);
                weight = (weight + edges[i].weight);
                SetUnion.union_sets(components, edges[i].x, edges[i].y);
            }
        }
        // Java garbage collection releases edges;
        return weight;
    }

    public static int main() {
        Graph.graph g = new Graph.graph();
        long weight = 0;
        Wgraph.read_graph(g, false);
        /*
            print_graph(&g);
        */
        weight = kruskal(g);
        C.printf("Out of Kruskal: weight=%lld \n", weight);
        return 0;
    }

    public static void main(String[] args) {
        int status = main();
        if (status != 0) System.exit(status);
    }
}
