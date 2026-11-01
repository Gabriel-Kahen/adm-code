"""Extract the book's named C fragments, including nested marked regions.

Markers have the form ``/* [[[ name */`` and ``/* ]]] */``. Parsing finishes
before any output is written, so malformed input cannot truncate saved snippets.
"""

import argparse
import re
from dataclasses import dataclass, field
from pathlib import Path

OUTPUT_DIR = "fragment"
EXTENSION = ""
START = re.compile(r"^\s*/\*\s*\[\[\[\s*([A-Za-z_][\w-]*)\s*\*/\s*$")
END = re.compile(r"^\s*/\*\s*\]\]\]\s*\*/\s*$")


class FragmentError(ValueError):
    """A marker is invalid, duplicated, or unbalanced."""


@dataclass
class _OpenFragment:
    name: str
    line: int
    lines: list[str] = field(default_factory=list)


def extract_fragments(filename: str | Path) -> dict[str, str]:
    """Read one source file without writing output; omit marker lines."""
    path = Path(filename)
    fragments = {}
    stack = []
    names = set()

    # The historical distribution also supports Latin-1 source comments.
    raw = path.read_bytes()
    try:
        source = raw.decode("utf-8")
    except UnicodeDecodeError:
        source = raw.decode("iso-8859-1")

    for number, line in enumerate(source.splitlines(keepends=True), 1):
        start = START.fullmatch(line)
        if start:
            name = start.group(1)
            if name in names:
                raise FragmentError(f"{path}:{number}: duplicate fragment {name!r}")
            names.add(name)
            stack.append(_OpenFragment(name, number))
        elif END.fullmatch(line):
            if not stack:
                raise FragmentError(f"{path}:{number}: closing marker without an opening marker")
            opened = stack.pop()
            text = "".join(opened.lines)
            fragments[opened.name] = text
            if stack:
                stack[-1].lines.append(text)
        elif re.match(r"\s*/\*\s*(?:\[\[\[|\]\]\])", line):
            raise FragmentError(f"{path}:{number}: malformed fragment marker")
        elif stack:
            stack[-1].lines.append(line)

    if stack:
        opened = stack[-1]
        raise FragmentError(f"{path}:{opened.line}: unclosed fragment {opened.name!r}")
    return fragments


def source_files(inputs: list[str | Path]) -> list[Path]:
    """Select explicit files and immediate C/header children of directories."""
    paths = set()
    for filename in inputs:
        path = Path(filename)
        if path.is_dir():
            paths.update(
                child
                for child in path.iterdir()
                if child.is_file() and child.suffix in {".c", ".h"}
            )
        elif path.is_file():
            paths.add(path)
        else:
            raise FragmentError(f"Source does not exist: {path}")
    return sorted(paths)


def collect_fragments(inputs: list[str | Path]) -> dict[str, str]:
    """Collect sources deterministically and reject ambiguous fragment names."""
    fragments = {}
    owners = {}
    for path in source_files(inputs):
        for name, text in extract_fragments(path).items():
            if name in owners:
                raise FragmentError(f"Fragment {name!r} occurs in both {owners[name]} and {path}")
            owners[name] = path
            fragments[name] = text
    return fragments


def write_fragments(fragments: dict[str, str], directory: str | Path, extension: str = "") -> None:
    """Write parsed fragments using the historical optional extension syntax."""
    destination = Path(directory)
    destination.mkdir(parents=True, exist_ok=True)
    suffix = f".{extension.lstrip('.')}" if extension else ""
    for name, text in sorted(fragments.items()):
        (destination / f"{name}{suffix}").write_text(text, encoding="utf-8")


def parse_file(filename: str | Path) -> None:
    """Compatibility entry point for callers that set OUTPUT_DIR/EXTENSION."""
    write_fragments(extract_fragments(filename), OUTPUT_DIR, EXTENSION)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", help="Source files or directories of C/header files")
    parser.add_argument("-d", "--directory", default=OUTPUT_DIR, help="Output directory")
    parser.add_argument("-e", "--extension", default=EXTENSION, help="Optional output extension")
    args = parser.parse_args(argv)
    try:
        fragments = collect_fragments(args.inputs)
        write_fragments(fragments, args.directory, args.extension)
    except (OSError, FragmentError) as error:
        parser.error(str(error))
    print(f"Wrote {len(fragments)} fragments to {args.directory}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
