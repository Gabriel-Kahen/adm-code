"""Build and run small C callers against the real repository implementations.

Modern callers use the selected compiler without ``-fcommon``. Historical
translation units retain their original tentative globals and GNU89 syntax;
those callers receive compatibility options before any explicit test flags.
"""

import os
import re
import shlex
import subprocess
import tempfile
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _excerpt(text, limit=3000):
    """Keep diagnostics useful without dumping an entire generated dataset."""
    return text if len(text) <= limit else text[:limit] + "\n... (truncated)"


def _legacy_caller(code, sources):
    historical_paths = ("original/", "tmp/", "datafiles/")
    return any(str(source).startswith(historical_paths) for source in sources) or bool(
        re.search(r'#include\s+"[^"\n]*(?:original|tmp|datafiles)/', code)
    )


@contextmanager
def compiled_c(code="", sources=(), flags=(), compiler=None):
    """Yield a temporary executable, compiling once for a collection of cases.

    ``compiler`` overrides the ``CC`` environment variable (default: GCC).
    ``flags`` come last so a test can deliberately select a language standard,
    sanitizer, or stricter diagnostic policy. Build failures include the command
    and compiler output; every test gets an isolated temporary directory.
    """
    compiler_words = shlex.split(compiler or os.environ.get("CC", "gcc"))
    if not compiler_words:
        raise AssertionError("CC must name a C compiler")

    compatibility = []
    if _legacy_caller(code, sources):
        compatibility.append("-fcommon")
    if "-std=gnu89" in flags and "clang" in Path(compiler_words[-1]).name:
        compatibility.append("-Wno-return-type")

    with tempfile.TemporaryDirectory(prefix="adm-test-") as temporary:
        directory = Path(temporary)
        files = [str(ROOT / source) for source in sources]
        if code:
            caller = directory / "caller.c"
            caller.write_text(code)
            files.insert(0, str(caller))
        executable = directory / "test"
        command = [
            *compiler_words,
            "-std=c99",
            "-O0",
            "-g",
            "-I",
            str(ROOT),
            *compatibility,
            *flags,
            *files,
            "-lm",
            "-o",
            str(executable),
        ]
        try:
            result = subprocess.run(command, text=True, capture_output=True, timeout=60)
        except (OSError, subprocess.TimeoutExpired) as error:
            raise AssertionError(
                f"Could not compile caller: {shlex.join(command)}\n{error}"
            ) from error
        if result.returncode:
            raise AssertionError(
                f"C compilation failed: {shlex.join(command)}\n"
                f"{_excerpt(result.stdout)}{_excerpt(result.stderr)}"
            )
        yield executable


def run_executable(executable, data="", args=(), timeout=5):
    """Run one bounded case, retaining nonzero exits for explicit error tests."""
    environment = os.environ.copy()
    # Many educational demos deliberately retain allocations until process exit.
    environment.setdefault("ASAN_OPTIONS", "detect_leaks=0")
    command = [str(executable), *map(str, args)]
    try:
        return subprocess.run(
            command,
            input=data,
            text=True,
            capture_output=True,
            timeout=timeout,
            env=environment,
        )
    except subprocess.TimeoutExpired as error:
        raise AssertionError(
            f"C caller exceeded {timeout}s: {shlex.join(command)}\nInput:\n{_excerpt(data)}"
        ) from error


def run_c(code="", sources=(), data="", flags=(), timeout=5, compiler=None, args=()):
    """Compile and run one caller; use ``compiled_c`` to reuse a build across cases."""
    with compiled_c(code=code, sources=sources, flags=flags, compiler=compiler) as executable:
        return run_executable(executable, data=data, args=args, timeout=timeout)
