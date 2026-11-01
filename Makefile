#	
#	Makefile for "Algorithm Design Manual" / "Programming Challenges" Programs
#

# Copyright 2003-2020 by Steven S. Skiena; all rights reserved.
# Permission is granted for use in non-commerical applications
# provided this copyright notice remains intact and unchanged.
# 
# These programs appear in my books:
# 
# "The Algorithm Design Manual" by Steven Skiena, second edition, Springer,
# London 2008.  See out website www.algorist.com for additional information
# or https://www.amazon.com/exec/obidos/ASIN/1848000693/thealgorith01-20
# 
# "Programming Challenges: The Programming Contest Training Manual"
# by Steven Skiena and Miguel Revilla, Springer-Verlag, New York 2003.
# See our website www.programming-challenges.com for additional information,
# or http://www.amazon.com/exec/obidos/ASIN/0387001638/thealgorithmrepo/


# The default target builds current root-level programs only. Historical
# examples in original/ and tmp/ are exercised by compatibility regressions.
.DEFAULT_GOAL := all

CC = gcc
PYTHON ?= python3
CPPFLAGS ?=
CFLAGS ?= -g -Wall -std=c99 -pedantic
LDFLAGS ?=
LDLIBS ?= -lm

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

# Retain the old variable name for callers that inspect the distribution.
BINARIES := $(PROGRAMS)
SOURCES := $(wildcard *.c)
HEADERS := $(wildcard *.h)
OBJECTS := $(SOURCES:.c=.o)
DEPENDENCIES := $(OBJECTS:.o=.d)

.PHONY: all make test test-regressions test-algorithms clean lint backup tar

all: $(PROGRAMS)
make: all

# Every program has a same-named driver. Extra library objects are listed below.
$(PROGRAMS): %: %.o
	$(CC) $(LDFLAGS) -o $@ $^ $(LDLIBS) $(LFLAGS)

%.o: %.c Makefile
	$(CC) $(CPPFLAGS) $(CFLAGS) -MMD -MP -c -o $@ $<

bfs-demo: queue.o graph.o bfs-dfs.o
biconnected: bfs-dfs.o queue.o graph.o
bipartite: queue.o graph.o bfs-dfs.o
cgtest: geometry.o
connected: queue.o graph.o bfs-dfs.o
convex-hull: geometry.o
countedges: queue.o graph.o bfs-dfs.o
dfs-demo: queue.o graph.o bfs-dfs.o
dijkstra: wgraph.o
findcycle: queue.o graph.o bfs-dfs.o
geotest: geometry.o
kruskal: set_union.o wgraph.o
lcs: editdistance.o
netflow: queue.o
paths: graph.o
prim: wgraph.o
sorting: random.o queue.o priority_queue.o
stringedit: editdistance.o
strong: bfs-dfs.o queue.o graph.o stack.o
strong1: bfs-dfs.o queue.o graph.o stack.o
substringedit: editdistance.o
superman: geometry.o
topsort: queue.o graph.o
topsort1: queue.o graph.o stack.o bfs-dfs.o
triangulate: geometry.o
tsp: annealing.o random.o
tsp-astar: tsp-pq.o
war: queue.o random.o

# Each suite runs in its own process so direct test-script imports stay simple.
test: test-c test-ports

.PHONY: test-c ports test-ports
test-c: test-regressions test-algorithms test-tooling

# C++17, JDK17, and Python3.10+; compiler outputs stay under build/ports.
ports:
	$(PYTHON) tools/ports.py build all

test-ports:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m unittest discover -s tests/ports -p 'test_*.py' -v

test-regressions:
	CC="$(CC)" PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m unittest discover -s tests/regressions -p 'test_*.py' -v

test-algorithms:
	CC="$(CC)" PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m unittest discover -s tests/algorithms -p 'test_*.py' -v

# Source maintenance uses pinned optional tools from requirements-dev.txt.
.PHONY: format check-format fragments check-fragments check test-tooling

format:
	$(PYTHON) tools/format_code.py
	$(MAKE) fragments

check-format:
	$(PYTHON) tools/format_code.py --check

fragments:
	$(PYTHON) tools/fragments.py

check-fragments:
	$(PYTHON) tools/fragments.py --check

test-tooling:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m unittest discover -s tests/tooling -p 'test_*.py' -v

check: check-format check-fragments test

clean:
	rm -f $(PROGRAMS) $(OBJECTS) $(DEPENDENCIES) core a.out tests/*.o

# Legacy distribution utilities; regular development uses all, test, and clean.
lint:
	lint -h $(SOURCES)

backup:
	mkdir -p backup
	cp $(SOURCES) $(HEADERS) Makefile backup/

tar:
	$(MAKE) clean
	tar cvf /tmp/bookprograms.tar .

# Compiler-generated dependencies rebuild only the affected translation units.
-include $(DEPENDENCIES)
