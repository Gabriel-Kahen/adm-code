"""Format maintained source and readable C examples embedded in Python tests."""

import argparse
import ast
import io
import os
import re
import shutil
import subprocess
import tokenize
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
C_EXTENSIONS = {".c", ".h", ".cc", ".java"}
HISTORICAL_C = {
    "tmp/binomial.v1",
    "tmp/sudoku-v2",
    "tmp/tsp-astar.v1",
    "datafiles/sudoku-examples/sudoku.v1",
}
VERSIONS = {"clang-format": "22.1.8", "ruff": "0.17.3"}


def tool(name: str) -> str:
    """Prefer the project's virtual environment, with explicit env overrides."""
    override = os.environ.get(name.upper().replace("-", "_"))
    local = ROOT / ".venv" / "bin" / name
    executable = override or (str(local) if local.is_file() else shutil.which(name))
    if not executable:
        raise RuntimeError(f"Missing {name}; install requirements-dev.txt in .venv")
    version = subprocess.check_output([executable, "--version"], text=True)
    if VERSIONS[name] not in re.findall(r"\d+\.\d+\.\d+", version):
        raise RuntimeError(f"Expected {name} {VERSIONS[name]}, found {version.strip()}")
    return executable


def source_files() -> list[Path]:
    result = subprocess.check_output(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"], cwd=ROOT
    )
    return sorted({ROOT / name for name in result.decode().split("\0") if name})


def preserve_notices(before: str, after: str) -> str:
    """The distribution requires copyright notices to remain unchanged."""
    notices = iter(
        comment for comment in re.findall(r"/\*.*?\*/", before, re.S) if "Copyright" in comment
    )
    return re.sub(
        r"/\*.*?\*/",
        lambda match: next(notices) if "Copyright" in match[0] else match[0],
        after,
        flags=re.S,
    )


def format_c(text: str, path: Path, executable: str) -> str:
    assumed = path if path.suffix in C_EXTENSIONS else path.with_suffix(".c")
    result = subprocess.run(
        [executable, "--style=file", f"--assume-filename={assumed}"],
        input=text,
        text=True,
        capture_output=True,
        check=True,
    )
    return preserve_notices(text, result.stdout)


def format_c_examples(source: str, executable: str) -> str:
    """Expand complete C main-function literals; leave interpolated templates alone.

    Decode/re-encode literal contents so C escape sequences keep their value.
    Python formatting itself is delegated to Ruff after these replacements.
    """
    lines = source.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))
    replacements = []
    for token in tokenize.generate_tokens(io.StringIO(source).readline):
        if token.type != tokenize.STRING:
            continue
        prefix = re.match(r"[A-Za-z]*", token.string)[0].lower()
        if "f" in prefix or "b" in prefix:
            continue
        value = ast.literal_eval(token.string)
        if isinstance(value, str) and "\n" not in value:
            continue  # A signature/search token is not a complete C example.
        # A closing quote can belong to an interpolated #include filename.
        # Such a literal is only part of a C unit and must not be reformatted.
        if isinstance(value, str) and value.lstrip().startswith(('"', "'")):
            continue
        if not isinstance(value, str) or not re.search(
            r"\b(?:int\s+main\s*\([^)]*\)\s*\{|typedef\s+struct\b)", value
        ):
            continue
        formatted = format_c(value, ROOT / "test-example.c", executable)
        delimiter = '"""' if '"""' not in formatted else "'''"
        if delimiter in formatted:
            continue
        replacement = "r" + delimiter + "\n" + formatted.strip("\n") + "\n" + delimiter
        start = offsets[token.start[0] - 1] + token.start[1]
        end = offsets[token.end[0] - 1] + token.end[1]
        replacements.append((start, end, replacement))
    for start, end, replacement in reversed(replacements):
        source = source[:start] + replacement + source[end:]
    return source


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Report changes without writing files")
    args = parser.parse_args(argv)
    try:
        clang_format, ruff = tool("clang-format"), tool("ruff")
        paths = source_files()
        changed = []
        python_files = []
        for path in paths:
            name = path.relative_to(ROOT).as_posix()
            if path.suffix in C_EXTENSIONS or name in HISTORICAL_C:
                before = path.read_text()
                after = format_c(before, path, clang_format)
            elif path.suffix == ".py":
                python_files.append(str(path))
                before = path.read_text()
                after = (
                    format_c_examples(before, clang_format)
                    if name.startswith(("tests/regressions/", "tests/algorithms/"))
                    else before
                )
            else:
                continue
            if before != after:
                changed.append(name)
                if not args.check:
                    path.write_text(after)
        if changed:
            print(("Needs formatting: " if args.check else "Formatted: ") + ", ".join(changed))
        lint = [ruff, "check", *([] if args.check else ["--fix"]), *python_files]
        formatted = [ruff, "format", *(["--check"] if args.check else []), *python_files]
        # Expand statements before linting, then normalize any fixed imports.
        format_result = subprocess.run(formatted, cwd=ROOT)
        lint_result = subprocess.run(lint, cwd=ROOT)
        if not args.check:
            format_result = subprocess.run(formatted, cwd=ROOT)
        return int(
            bool((args.check and changed) or lint_result.returncode or format_result.returncode)
        )
    except (OSError, RuntimeError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
