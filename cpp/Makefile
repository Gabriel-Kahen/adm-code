# Direct C++ translations of the C programs; matching link dependencies.
.DEFAULT_GOAL := all
CXX ?= g++
CXXFLAGS ?= -g -Wall -pedantic -std=c++17
CPPFLAGS ?=
LDFLAGS ?=
LDLIBS ?= -lm
BUILD ?= ../build/cpp
PROGRAMS := \
    10055 \
    8-queens \
    bfs-demo \
    biconnected \
    bignum \
    binomial \
    bipartite \
    cgtest \
    connected \
    convex-hull \
    convolve \
    countedges \
    dfs-demo \
    dijkstra \
    distance \
    editbrute \
    elevator \
    fib \
    findcycle \
    floyd \
    gcd \
    geotest \
    kruskal \
    lcs \
    list-demo \
    matrix \
    name \
    netflow \
    order \
    partition \
    paths \
    permutations \
    plates \
    polly \
    prim \
    primes \
    sentinel \
    sorting \
    stringedit \
    strong \
    strong1 \
    subsets \
    subsetsum \
    substringedit \
    sudoku \
    superman \
    topsort \
    topsort1 \
    tree-demo \
    triangulate \
    tsp \
    tsp-astar \
    war
SOURCES := $(wildcard *.cpp)
OBJECTS := $(addprefix $(BUILD)/,$(SOURCES:.cpp=.o))
DEPENDENCIES := $(OBJECTS:.o=.d)
BINARIES := $(addprefix $(BUILD)/,$(PROGRAMS))
.PHONY: all clean
all: $(BINARIES) $(OBJECTS)
$(BINARIES): $(BUILD)/%: $(BUILD)/%.o
	$(CXX) $(LDFLAGS) -o $@ $^ $(LDLIBS)
$(BUILD)/%.o: %.cpp Makefile
	@mkdir -p $(@D)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -MMD -MP -c -o $@ $<

$(BUILD)/bfs-demo: $(BUILD)/queue.o $(BUILD)/graph.o $(BUILD)/bfs-dfs.o
$(BUILD)/biconnected: $(BUILD)/bfs-dfs.o $(BUILD)/queue.o $(BUILD)/graph.o
$(BUILD)/bipartite: $(BUILD)/queue.o $(BUILD)/graph.o $(BUILD)/bfs-dfs.o
$(BUILD)/cgtest: $(BUILD)/geometry.o
$(BUILD)/connected: $(BUILD)/queue.o $(BUILD)/graph.o $(BUILD)/bfs-dfs.o
$(BUILD)/convex-hull: $(BUILD)/geometry.o
$(BUILD)/countedges: $(BUILD)/queue.o $(BUILD)/graph.o $(BUILD)/bfs-dfs.o
$(BUILD)/dfs-demo: $(BUILD)/queue.o $(BUILD)/graph.o $(BUILD)/bfs-dfs.o
$(BUILD)/dijkstra: $(BUILD)/wgraph.o
$(BUILD)/findcycle: $(BUILD)/queue.o $(BUILD)/graph.o $(BUILD)/bfs-dfs.o
$(BUILD)/geotest: $(BUILD)/geometry.o
$(BUILD)/kruskal: $(BUILD)/set_union.o $(BUILD)/wgraph.o
$(BUILD)/lcs: $(BUILD)/editdistance.o
$(BUILD)/netflow: $(BUILD)/queue.o
$(BUILD)/paths: $(BUILD)/graph.o
$(BUILD)/prim: $(BUILD)/wgraph.o
$(BUILD)/sorting: $(BUILD)/random.o $(BUILD)/queue.o $(BUILD)/priority_queue.o
$(BUILD)/stringedit: $(BUILD)/editdistance.o
$(BUILD)/strong: $(BUILD)/bfs-dfs.o $(BUILD)/queue.o $(BUILD)/graph.o $(BUILD)/stack.o
$(BUILD)/strong1: $(BUILD)/bfs-dfs.o $(BUILD)/queue.o $(BUILD)/graph.o $(BUILD)/stack.o
$(BUILD)/substringedit: $(BUILD)/editdistance.o
$(BUILD)/superman: $(BUILD)/geometry.o
$(BUILD)/topsort: $(BUILD)/queue.o $(BUILD)/graph.o
$(BUILD)/topsort1: $(BUILD)/queue.o $(BUILD)/graph.o $(BUILD)/stack.o $(BUILD)/bfs-dfs.o
$(BUILD)/triangulate: $(BUILD)/geometry.o
$(BUILD)/tsp: $(BUILD)/annealing.o $(BUILD)/random.o
$(BUILD)/tsp-astar: $(BUILD)/tsp-pq.o
$(BUILD)/war: $(BUILD)/queue.o $(BUILD)/random.o

clean:
	rm -f $(BINARIES) $(OBJECTS) $(DEPENDENCIES)
-include $(DEPENDENCIES)
