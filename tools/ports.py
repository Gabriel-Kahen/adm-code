"""Build and run the C++, Java, and Python algorithm libraries without dependencies."""

import argparse
import ast
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build" / "ports"
LANGUAGES = ("cpp", "java", "python")


def executable(variable: str, default: str) -> str:
    """Resolve explicit overrides, JAVA_HOME, then tools on PATH."""
    selected = os.environ.get(variable)
    if not selected and variable in ("JAVA", "JAVAC") and os.environ.get("JAVA_HOME"):
        selected = str(Path(os.environ["JAVA_HOME"]) / "bin" / default)
    selected = selected or shutil.which(default)
    if not selected or not (shutil.which(selected) or Path(selected).is_file()):
        raise RuntimeError(f"Missing {default}; install it or set {variable}")
    return selected


def build(language: str) -> None:
    """Build into an ignored directory; propagate compiler errors without hiding output."""
    destination = BUILD / language
    destination.mkdir(parents=True, exist_ok=True)
    if language == "cpp":
        sources = sorted((ROOT / "cpp" / "src").glob("*.cpp"))
        if not sources:
            raise RuntimeError("No C++ sources found")
        command = [
            executable("CXX", "g++"),
            "-std=c++17",
            "-Wall",
            "-Wextra",
            "-Wpedantic",
            "-Werror",
            *shlex.split(os.environ.get("CXXFLAGS", "-O2")),
            "-I",
            str(ROOT / "cpp" / "include"),
            *map(str, sources),
            *shlex.split(os.environ.get("PORTS_LDFLAGS", "")),
            "-o",
            str(destination / "adm"),
        ]
    elif language == "java":
        sources = sorted((ROOT / "java" / "src" / "adm").glob("*.java"))
        if not sources:
            raise RuntimeError("No Java sources found")
        command = [
            executable("JAVAC", "javac"),
            "--release",
            "17",
            "-Xlint:all",
            "-Werror",
            "-d",
            str(destination),
            *map(str, sources),
        ]
    elif language == "python":
        for source in sorted((ROOT / "python" / "adm").glob("*.py")):
            ast.parse(source.read_text(), filename=str(source))
        command = [sys.executable, "-B", "-c", "import adm"]
    else:
        raise ValueError(f"Unknown language: {language}")
    subprocess.run(command, cwd=ROOT, env=environment(), check=True, timeout=180)


def environment() -> dict[str, str]:
    result = dict(os.environ)
    result["PYTHONPATH"] = str(ROOT / "python")
    result["PYTHONDONTWRITEBYTECODE"] = "1"
    return result


def command(language: str) -> list[str]:
    if language == "cpp":
        return [str(BUILD / "cpp" / "adm")]
    if language == "java":
        return [executable("JAVA", "java"), "-cp", str(BUILD / "java"), "adm.Main"]
    if language == "python":
        return [sys.executable, "-B", "-m", "adm"]
    raise ValueError(f"Unknown language: {language}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("build", "run"))
    parser.add_argument("language", choices=(*LANGUAGES, "all"))
    parser.add_argument("arguments", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    try:
        if args.action == "run":
            if args.language == "all" or not args.arguments:
                parser.error("run requires one language and an operation")
            return subprocess.run(
                [*command(args.language), *args.arguments], cwd=ROOT, env=environment()
            ).returncode
        if args.arguments:
            parser.error("build does not accept operation arguments")
        for language in LANGUAGES if args.language == "all" else (args.language,):
            build(language)
        return 0
    except (OSError, RuntimeError, subprocess.SubprocessError) as error:
        print(error, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
