# Contributing

Prefer a change a reader can understand from the source, a small example, and a
focused test. These programs teach algorithms, so preserve the connection
between the implementation, its mathematical state, and the book excerpts.

## Development setup

The programs need a C99 compiler and GNU Make. Tests additionally need Python 3,
GCC, Clang, and sanitizer runtimes. Formatting tools are optional for running the
programs and required for maintenance checks.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
make -j2 all
make test
```

Development versions are pinned in `requirements-dev.txt`: clang-format
**22.1.8** and Ruff **0.17.3**. Use those versions to avoid unrelated formatting
differences. The C layout is defined by `.clang-format`; `.editorconfig` covers
basic whitespace conventions.

## Readability first

- Give local state descriptive names when its role is not obvious. Short `i`,
  `j`, `n`, and `k` remain useful where they directly express an index, size, or
  recurrence from the book.
- Keep one logical operation per statement. Use braces for new or changed
  control-flow bodies and avoid compressed chains of mutations.
- Comment on an invariant, a precondition, a non-obvious choice, or an ownership
  rule. A comment saying “counter” beside an ordinary loop index adds less value.
- Keep error handling near the condition it protects. Make capacity exhaustion
  and unsupported inputs explicit rather than printing a plausible result.
- Separate algorithm state changes from display code where this makes the
  algorithm easier to follow. Preserve existing demo output unless the change
  deliberately updates its contract and tests.
- Preserve copyright and permission notices verbatim. Keep source extraction
  markers attached to the algorithm block they describe.

Use the formatters for mechanical layout:

```sh
make format
make check-format
```

Review the diff afterward. Formatting is not a substitute for clear names,
straightforward control flow, or accurate comments. Avoid unrelated algorithm
changes in a readability-only patch.

## Excerpts and historical copies

Most files in `code-fragments/` come from blocks delimited by
`/* [[[ name */` and `/* ]]] */` in root C/header files. Blocks may be nested.
Edit the full source first, then update and check its excerpts:

```sh
make fragments
make check-fragments
```

Some old excerpts have no current source marker and are retained as historical
material. `original/`, `tmp/`, and the source examples under `datafiles/` can have
different interfaces or incomplete drivers. If a fix applies to one of those
copies, include its own regression or explain why it is outside the change's
contract. Do not copy a modern header into a legacy translation unit without
checking the types and callbacks together.

## Testing a change

Add a focused test for a behavior change, using the real implementation and an
independent expected result or invariant. Deterministic seeds make randomized
checks reproducible. Use a boundary case when the change concerns an allocation,
a loop endpoint, or a numeric range. Avoid tests that simply restate the new
implementation.

See [the testing guide](docs/TESTING.md) for suite selection, sanitizer details,
and the distinction between current root programs and historical examples.

Before submitting:

```sh
make check
```

Describe the problem and resulting behavior in the PR, along with the tests run
and any changed input/output contract. For a style-only change, state that its
algorithm behavior is unchanged and keep semantic edits separately reviewable.
The [fix index](AUDIT_FIXES.md) records existing audit regressions and upstream
issue links; new work should use the same evidence-based approach.
