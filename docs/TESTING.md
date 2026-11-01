# Testing the algorithms

The supported suite compiles the real implementations with small C callers and
checks their results. Python's standard-library `unittest` runner coordinates
the tests; no Python test framework needs to be installed.

## Run the suite

On the checked Linux configuration, install GCC, Clang, GNU Make, Python 3.10 or newer, and
the compiler sanitizer runtimes. Then run:

```sh
make test
```

`./test-script.sh` runs the same suite and preserves a failing status. The suite
creates temporary executables and compilation files outside the source tree.
Historical tests select compatibility flags explicitly; the current programs
must build with normal C99 flags.

For a narrower check:

```sh
make test-regressions
make test-algorithms
make test-tooling
python3 -m unittest discover -s tests/regressions -p 'test_GN13.py' -v
python3 -m unittest discover -s tests/regressions -p 'test_DP*.py' -v
```

Finding IDs in existing test names refer to [AUDIT_FIXES.md](../AUDIT_FIXES.md).
Use descriptive names for new test cases so a failure explains the operation,
input property, or boundary being checked.

## What each kind of test establishes

| Check | Example | What it catches |
|---|---|---|
| Small counterexample | Delete one of two equal tree keys | A specific regression and its root cause |
| Independent oracle | Compare a small TSP result with exhaustive tours | Incorrect answers that still look plausible |
| Invariant | Check parent links or residual-capacity conservation | Corrupt intermediate state or a misleading reported result |
| Capacity boundary | Use the declared maximum number of vertices | Off-by-one allocations and indexing |
| Sanitizer | Run an actual C caller with ASan, UBSan, or MSan | Invalid memory access, undefined arithmetic, or uninitialized data |
| Fresh build | Compile current root programs with GCC and Clang | Missing dependencies, inconsistent declarations, or stale artifacts |

Passing a finite set of inputs is bounded evidence. Tests should state their
domain: nonnegative graph weights, valid polygons, representable numeric results,
or another relevant precondition. Heuristic quality is a different question
from memory safety, permutation validity, or termination.

The files under `datafiles/` remain useful sample inputs and historical outputs.
Some output snapshots record earlier bugs, platform-dependent random sequences,
or teaching diagnostics. Do not replace a mathematical oracle with a fresh copy
of the current program's output.

## Write a regression that explains the problem

1. Choose the smallest input demonstrating the behavior.
2. State the expected result independently: a simple known answer, an exhaustive
   reference calculation, or a structural invariant.
3. Compile and invoke the actual source through the shared test helper. When a
   source has its own driver, a caller can rename `main` before including it.
4. Assert the expected result, normal exit, and relevant sanitizer cleanliness.
   Add boundaries or a deterministic set of related cases when they test the
   same failure mechanism.
5. Include each affected historical copy only when it has a compatible contract.
   Explain extra compiler flags instead of applying legacy relaxations globally.

Keep embedded C callers readable. Use normal indentation, named intermediate
values, and failure messages that identify the source and case. A long random
loop should record its seed and compare against an independent result.

## Diagnose a failure

The helper reports compiler output when a caller cannot build. A nonzero program
exit, a mismatched result, and a subprocess timeout mean different things: read
the assertion and captured output before deciding which algorithm failed.

- **ASan** detects invalid memory accesses. Leak detection is disabled in the
  short-lived educational callers, which do not all own a complete cleanup API.
- **UBSan** detects operations such as signed overflow and invalid array indexing.
- **MSan** checks initialized values in selected Clang callers. Its runtime and
  address-space requirements depend on the platform; a shadow-memory mapping
  failure is distinct from an uninitialized-value diagnostic.

A sanitizer test passing on one compiler does not establish every platform's
integer widths or floating-point behavior. For example, the Fibonacci driver
uses `long` for values through index 92, and the checked host has 64-bit `long`.
Historical C++, Java, Pascal, Wolfram, and notebook examples are outside the
normal root C build and require their own toolchains.

## Repository checks

Install the pinned development tools described in
[CONTRIBUTING.md](../CONTRIBUTING.md), then run:

```sh
make check-format
make check-fragments
make check
```

Formatting checks should make no changes. Fragment checks compare marked root
source with its saved excerpts; changing a source block requires regeneration.
`make check` combines the maintenance checks with tests. CI builds the current
programs with GCC and Clang and runs the supported checks configured in the
workflow.
