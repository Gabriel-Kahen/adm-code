.DEFAULT_GOAL := all
CC = gcc
CXX ?= g++
JAVAC ?= javac
JAVA ?= java
PYTHON ?= python3
CXXFLAGS ?= -O2 -g -Wall -pedantic -std=c++17
STRUCTURES := queue stack priority_queue set_union graph
TEST_DRIVERS := Structures TspValues TspMoves

.PHONY: all c cpp java python test clean
all: c cpp java python

c:
	$(MAKE) -C c CC="$(CC)" all

cpp:
	$(MAKE) -C cpp CXX="$(CXX)" CXXFLAGS="$(CXXFLAGS)" all

java:
	@mkdir -p build/java
	$(JAVAC) --release 17 -Xlint:all -d build/java java/*.java

python:
	$(PYTHON) -c 'from pathlib import Path; [compile(p.read_text(), str(p), "exec") for p in Path("python").glob("*.py")]'

build/tests/c-structures: tests/structures.c $(addprefix c/,$(addsuffix .c,$(STRUCTURES))) $(wildcard c/*.h)
	@mkdir -p $(@D)
	$(CC) -std=c99 -Wall -Ic $< $(addprefix c/,$(addsuffix .c,$(STRUCTURES))) -o $@

build/tests/cpp-structures: tests/structures.c $(addprefix cpp/,$(addsuffix .cpp,$(STRUCTURES))) $(wildcard cpp/*.hpp)
	@mkdir -p $(@D)
	$(CXX) $(CXXFLAGS) -Icpp -x c++ $< $(addprefix cpp/,$(addsuffix .cpp,$(STRUCTURES))) -o $@

$(addprefix build/tests/,$(addsuffix .class,$(TEST_DRIVERS))): build/tests/%.class: tests/%.java java
	@mkdir -p $(@D)
	$(JAVAC) --release 17 -Xlint:all -cp build/java -d build/tests $<

build/tests/c-tsp-values: tests/tsp_values.c c/tsp-pq.c $(wildcard c/*.h)
	@mkdir -p $(@D)
	$(CC) -std=c99 -Wall $< c/tsp-pq.c -o $@

build/tests/cpp-tsp-values: tests/tsp_values.c cpp/tsp-pq.cpp $(wildcard cpp/*.hpp)
	@mkdir -p $(@D)
	$(CXX) $(CXXFLAGS) -x c++ $< cpp/tsp-pq.cpp -o $@

build/tests/c-tsp-moves: tests/tsp_moves.c c/tsp.c c/annealing.c c/random.c $(wildcard c/*.h)
	@mkdir -p $(@D)
	$(CC) -std=c99 -Wall $< c/annealing.c c/random.c -lm -o $@

build/tests/cpp-tsp-moves: tests/tsp_moves.c cpp/tsp.cpp cpp/annealing.cpp cpp/random.cpp $(wildcard cpp/*.hpp)
	@mkdir -p $(@D)
	$(CXX) $(CXXFLAGS) -x c++ $< cpp/annealing.cpp cpp/random.cpp -o $@

test: all build/tests/c-structures build/tests/cpp-structures build/tests/c-tsp-values build/tests/cpp-tsp-values build/tests/c-tsp-moves build/tests/cpp-tsp-moves $(addprefix build/tests/,$(addsuffix .class,$(TEST_DRIVERS)))
	JAVA="$(JAVA)" PYTHON="$(PYTHON)" PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m unittest discover -s tests -p 'test_*.py' -v

clean:
	$(MAKE) -C c clean
	$(MAKE) -C cpp clean
	rm -rf build
