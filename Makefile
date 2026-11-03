# Original programs and direct language counterparts. No package installation.
.DEFAULT_GOAL := all
CC = gcc
CXX ?= g++
JAVAC ?= javac
JAVA ?= java
PYTHON ?= python3
CXXFLAGS ?= -O2 -Wall -Wextra -Werror -pedantic -std=c++17

PROGRAMS := 10055 8-queens bfs-demo biconnected bignum binomial bipartite cgtest connected convex-hull convolve countedges dfs-demo dijkstra distance editbrute elevator fib findcycle floyd gcd geotest kruskal lcs list-demo matrix name netflow order partition paths permutations plates polly prim primes sentinel sorting stringedit strong strong1 subsets subsetsum substringedit sudoku superman topsort topsort1 tree-demo triangulate tsp tsp-astar war
CPP_SOURCES := $(wildcard cpp/*.cpp)
CPP_OBJECTS := $(patsubst cpp/%.cpp,build/cpp/%.o,$(CPP_SOURCES))

.PHONY: all c cpp java test clean
all: c cpp java

c:
	$(MAKE) -C c CC="$(CC)" all

cpp: $(addprefix build/cpp/,$(PROGRAMS))

build/cpp/%.o: cpp/%.cpp $(wildcard cpp/*.hpp)
	@mkdir -p $(@D)
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Define the small main() in the selected file; shared code has no main().
$(addprefix build/cpp/,$(PROGRAMS)): build/cpp/%: cpp/%.cpp $(CPP_OBJECTS)
	$(CXX) $(CXXFLAGS) -DADM_DEMO $< $(filter-out build/cpp/$*.o,$(CPP_OBJECTS)) -o $@

java:
	@mkdir -p build/java
	$(JAVAC) --release 17 -Xlint:all -Werror -d build/java java/*.java

build/tests/cpp: tests/cpp.cpp $(CPP_SOURCES) $(wildcard cpp/*.hpp)
	@mkdir -p $(@D)
	$(CXX) $(CXXFLAGS) tests/cpp.cpp -o $@

test: c java build/tests/cpp $(CPP_OBJECTS) build/cpp/dijkstra
	./build/tests/cpp
	$(JAVAC) --release 17 -Xlint:all -Werror -cp build/java -d build/java tests/TestJava.java
	$(JAVA) -cp build/java TestJava
	JAVA="$(JAVA)" PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. $(PYTHON) -m unittest discover -s tests -p 'test_*.py' -v

clean:
	$(MAKE) -C c clean
	rm -rf build
