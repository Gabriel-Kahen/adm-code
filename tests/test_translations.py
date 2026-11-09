"""Compare the translations with the C programs, including their teaching traces."""

import difflib
import os
from pathlib import Path
import random
import re
import shlex
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = os.environ.get("PARITY_LANGUAGES", "cpp java python").split()
GRAPH = "5 5\n1 2\n1 3\n2 4\n3 4\n4 5\n"
WEIGHTED = "5 6\n1 2 4\n1 3 1\n3 2 2\n2 4 1\n3 4 5\n4 5 3\n"
DIRECTED = "6 7\n1 2\n2 3\n3 1\n3 4\n4 5\n5 4\n5 6\n"
DAG = "6 6\n1 2\n1 3\n2 4\n3 4\n4 5\n3 6\n"
SUDOKU = (
    "034678912\n672195348\n198342567\n859761423\n426853791\n"
    "713924856\n961537284\n287419635\n345286179\n"
)


def java_class(name):
    if name == "10055":
        return "P10055"
    if name == "8-queens":
        return "EightQueens"
    return "".join(part.capitalize() for part in re.split("[-_]", name))


def python_file(name):
    return {"10055": "p10055", "8-queens": "eight_queens"}.get(
        name, name.replace("-", "_")
    ) + ".py"


def command(language, name):
    if language == "c":
        return [str(ROOT / "c" / name)]
    if language == "cpp":
        return [str(ROOT / "build/cpp" / name)]
    if language == "java":
        return shlex.split(os.environ.get("JAVA", "java")) + [
            "-Duser.language=en", "-Duser.country=US", "-cp",
            str(ROOT / "build/java"), java_class(name),
        ]
    return shlex.split(os.environ.get("PYTHON", "python3")) + [
        str(ROOT / "python" / python_file(name))
    ]


def run(language, name, data, timeout=120):
    result = subprocess.run(
        command(language, name), input=data.encode(), capture_output=True,
        cwd=ROOT, timeout=timeout,
        env={**os.environ, "LC_ALL": "C", "PYTHONDONTWRITEBYTECODE": "1"},
    )
    return result.returncode, result.stdout, result.stderr


def demo_cases():
    cases = {
        "10055": "10 12\n12 10\n0 0\n2147483648 0\n",
        "8-queens": "",
        "bignum": "123 45\n-123 45\n123 -45\n0 3\n3 0\n-2147483648 1\n",
        "binomial": "5\n0 0\n5 2\n67 0\n66 33\n100 1\n",
        "cgtest": "0 0\n4 4\n0 4\n4 0\n",
        "convex-hull": "7\n0 0\n2 0\n2 2\n0 2\n1 1\n0 0\n1 0\n",
        "convolve": "3\n1 -2 3\n2\n4 5\n",
        "distance": "",
        "editbrute": "ab\nac\n",
        "elevator": "4 2\n1 4 7 10\n",
        "fib": "",
        "gcd": "48 18\n18014398509481987 2\n0 7\n",
        "geotest": "0 0\n4 4\n0 4\n4 0\n",
        "lcs": "abcde\nace\n",
        "list-demo": "i 2\ni 1\ni 2\np\ns 2\nd 2\np\nd 9\np\n",
        "matrix": "2 3\n1 2 3\n4 5 6\n3 2\n7 8\n9 10\n11 12\n",
        "name": '2\n"ACME" "ACME Corp"\n"old" "new"\n2\nACME and old\nold ACME ACME\n',
        "netflow": "1 6\n6 7\n1 3 1\n1 2 1\n2 5 1\n2 4 1\n3 4 1\n4 6 1\n5 6 1\n",
        "order": "",
        "partition": "5 3\n10 20 30 40 50\n",
        "paths": "4 4\n1 2\n1 3\n2 4\n3 4\n",
        "permutations": "",
        "plates": "10 7 1\n",
        "polly": "Amy Zed 180 76\nBob Able 180 74\nCarl Able 180 74\nDan Doe 179 75\n",
        "primes": "1\n2\n60\n97\n",
        "sentinel": "",
        "sorting": "",
        "stringedit": "kitten\nsitting\n",
        "subsets": "",
        "subsetsum": "3\n4 6\n1 2 3 4\n3 7\n2 4 8\n3 0\n1 2 3\n",
        "substringedit": "abc\nzzabcxx\n",
        "sudoku": SUDOKU,
        "superman": "0 0\n10 0\n1\n5 0 1\n",
        "tree-demo": "i 4\ni 2\ni 6\ni 2\ni 5\np\ns 5\nd 2\np\nd 4\np\ns 4\n",
        "triangulate": "5\n0 0\n3 0\n4 2\n2 4\n0 2\n",
        # All 2-city tours have equal nonzero cost, so RNG choice cannot affect
        # the heuristic's printed costs or saved best tour. Keep C's full loops.
        "tsp": "2\n1 0 0\n2 3 4\n2\n1 2\n",
        "tsp-astar": "4\n1 2 8\n2 8 10\n3 7 6\n4 1 9\n",
        "war": "Ah\nKh\n",
    }
    for name in ("bfs-demo", "biconnected", "bipartite", "connected", "countedges", "dfs-demo", "findcycle"):
        cases[name] = GRAPH
    for name in ("dijkstra", "floyd", "kruskal", "prim"):
        cases[name] = WEIGHTED
    for name in ("strong", "strong1"):
        cases[name] = DIRECTED
    for name in ("topsort", "topsort1"):
        cases[name] = DAG
    return [(name, "demo", data) for name, data in sorted(cases.items())]


def regression_cases():
    cases = [
        ("convex-hull", "collinear", "4\n3 0\n1 0\n0 0\n2 0\n"),
        ("bipartite", "self-loop", "1 1\n1 1\n"),
        ("countedges", "parallel", "2 2\n1 2\n1 2\n"),
        ("netflow", "parallel", "1 2\n2 2\n1 2 1\n1 2 1\n"),
        ("partition", "nonempty-groups", "3 3\n10 1 1\n"),
        ("partition", "large-cost", "2 2\n100000 100000\n"),
        ("plates", "too-narrow", "0.5 4 1\n"),
        ("tree-demo", "duplicate-root", "i 1\ni 1\nd 1\np\n"),
        ("name", "no-op", '1\n"ACME" "ACME"\n1\nACME\n'),
        ("editbrute", "parent-reconstruction", "a\nb\n"),
        ("floyd", "empty-path", "1 0\n"),
        ("lcs", "no-match", "a\nb\n"),
        ("substringedit", "ties", "ab\nxbab\n"),
        ("binomial", "domain-error", "1\n101 0\n"),
        ("binomial", "overflow-error", "1\n67 33\n"),
        ("convolve", "dimension-error", "0\n"),
        ("elevator", "dimension-error", "-1 0\n"),
        ("elevator", "destination-error", "1 1\n-1\n"),
        ("stringedit", "missing-string", "a\n"),
        ("name", "empty-pattern", '1\n"" "x"\n1\ntext\n'),
        ("tsp", "zero-cost-single-city", "1\n1 0 0\n1\n1\n"),
        ("convolve", "capacity-tail", "51\n" + "1 " * 51 + "\n51\n" + "1 " * 51 + "\n"),
    ]
    for name in ("bfs-demo", "dfs-demo", "connected", "strong", "strong1", "dijkstra", "prim", "kruskal"):
        cases.append((name, "disconnected", "4 0\n"))
    for name in ("dijkstra", "prim", "floyd", "kruskal"):
        cases.append((name, "wide-weights", "3 2\n1 2 2147483647\n2 3 2147483647\n"))
    # Same graph, multiple edge orders: the C linked-list insertion order and
    # array-scan tie breaking must survive translation.
    rng = random.Random(738)
    for trial in range(3):
        edges = [(1, 2), (1, 3), (2, 4), (3, 4), (4, 5), (5, 6), (2, 6)]
        rng.shuffle(edges)
        plain = "6 7\n" + "".join(f"{x} {y}\n" for x, y in edges)
        weighted = "6 7\n" + "".join(f"{x} {y} 1\n" for x, y in edges)
        for name in ("bfs-demo", "dfs-demo", "biconnected", "dijkstra", "prim"):
            cases.append((name, f"edge-order-{trial}", weighted if name in ("dijkstra", "prim") else plain))
    return cases


class TranslationParity(unittest.TestCase):
    @unittest.skipUnless("python" in LANGUAGES, "Python translation not selected")
    def test_python_scanf_preserves_c_assignment_semantics(self):
        import io
        from unittest.mock import patch
        from python import _c

        def scan(data, fmt, *previous):
            with patch("sys.stdin", io.StringIO(data)), patch.object(_c, "_lookahead", None):
                result = _c.scanf(fmt, *previous)
                return result, _c.getchar()

        cases = [
            ("", "%d %d", (7, 9), (-1, 7, 9), -1),
            ("12", "%d %d", (7, 9), (1, 12, 9), -1),
            ("12 x", "%d %d", (7, 9), (1, 12, 9), ord("x")),
            ("x", "%d %d", (7, 9), (0, 7, 9), ord("x")),
            ("12;x", "%d,%d", (7, 9), (1, 12, 9), ord(";")),
            (" \n", "%c", (0,), (1, ord(" ")), ord("\n")),
            (" -3.25e2 tail", "%lf", (7.0,), (1, -325.0), ord(" ")),
            (" \nQ", "\n", (), (0,), ord("Q")),
        ]
        for data, fmt, previous, expected, next_char in cases:
            with self.subTest(data=data, fmt=fmt):
                self.assertEqual(scan(data, fmt, *previous), (expected, next_char))

        buffer = [ord("z")] * 6 + [0]
        result, next_char = scan("hi", "%s %d", buffer, 9)
        self.assertEqual(result[0], 1)
        self.assertIs(result[1], buffer)
        self.assertEqual(result[2], 9)
        self.assertEqual(buffer, [ord("h"), ord("i"), 0] + [ord("z")] * 3 + [0])
        self.assertEqual(next_char, -1)
        result, _ = scan("", "%s", buffer)
        self.assertEqual(result[0], -1)
        self.assertIs(result[1], buffer)
        self.assertEqual(buffer, [ord("h"), ord("i"), 0] + [ord("z")] * 3 + [0])

    @unittest.skipUnless(os.name == "posix", "PTY console check requires POSIX")
    def test_console_processes_a_line_before_eof(self):
        import pty
        import select
        import termios
        import time

        for language in ["c"] + LANGUAGES:
            with self.subTest(language=language):
                master, slave = pty.openpty()
                settings = termios.tcgetattr(slave)
                settings[3] &= ~termios.ECHO
                termios.tcsetattr(slave, termios.TCSANOW, settings)
                process = subprocess.Popen(command(language, "10055"), cwd=ROOT,
                                           stdin=slave, stdout=slave, stderr=subprocess.PIPE)
                os.close(slave)
                output = b""
                try:
                    os.write(master, b"10 12\n")
                    deadline = time.monotonic() + 5
                    while time.monotonic() < deadline and b"2\n" not in output.replace(b"\r\n", b"\n"):
                        if select.select([master], [], [], 0.1)[0]:
                            try:
                                output += os.read(master, 4096)
                            except OSError:
                                break
                    self.assertEqual(output.replace(b"\r\n", b"\n"), b"2\n")
                finally:
                    process.terminate()
                    process.wait(timeout=5)
                    process.stderr.close()
                    os.close(master)

    def compare_helper(self, name, class_name):
        def snapshot(argv):
            result = subprocess.run(
                argv, cwd=ROOT, capture_output=True, timeout=30,
                env={**os.environ, "LC_ALL": "C", "PYTHONDONTWRITEBYTECODE": "1"},
            )
            self.assertEqual(result.returncode, 0, result.stderr.decode(errors="replace"))
            return result.stdout, result.stderr

        expected = snapshot([str(ROOT / "build/tests" / ("c-" + name))])
        commands = {
            "cpp": [str(ROOT / "build/tests" / ("cpp-" + name))],
            "java": shlex.split(os.environ.get("JAVA", "java")) + [
                "-Duser.language=en", "-Duser.country=US", "-cp",
                str(ROOT / "build/java") + os.pathsep + str(ROOT / "build/tests"), class_name,
            ],
            "python": shlex.split(os.environ.get("PYTHON", "python3")) + [
                str(ROOT / "tests" / (name.replace("-", "_") + ".py"))
            ],
        }
        for language in LANGUAGES:
            with self.subTest(language=language):
                self.assertEqual(snapshot(commands[language]), expected)

    def test_tsp_records_cross_queue_boundaries_by_value(self):
        self.compare_helper("tsp-values", "TspValues")

    def test_tsp_pointer_offsets_and_transition_undo(self):
        self.compare_helper("tsp-moves", "TspMoves")

    def test_auxiliary_structure_state_matches_c(self):
        self.compare_helper("structures", "Structures")

    def test_every_c_implementation_has_a_counterpart(self):
        for source in (ROOT / "c").glob("*.c"):
            for path in (
                ROOT / "cpp" / (source.stem + ".cpp"),
                ROOT / "java" / (java_class(source.stem) + ".java"),
                ROOT / "python" / python_file(source.stem),
            ):
                with self.subTest(source=source.name, counterpart=str(path.relative_to(ROOT))):
                    self.assertTrue(path.is_file())

    def test_original_demo_coverage(self):
        makefile = (ROOT / "c/Makefile").read_text()
        match = re.search(r"PROGRAMS := (.*?)\n\n", makefile, re.S)
        programs = set(match[1].replace("\\", "").split())
        self.assertEqual(programs, {name for name, _, _ in demo_cases()})

    def test_demo_and_regression_traces_match_c(self):
        for name, label, data in demo_cases() + regression_cases():
            expected = run("c", name, data)
            self.assertIn(expected[0], (0, 1, 255), f"C fixture failed: {name}/{label}: {expected}")
            for language in LANGUAGES:
                with self.subTest(program=name, case=label, language=language):
                    actual = run(language, name, data)
                    for index, stream in ((0, "status"), (1, "stdout"), (2, "stderr")):
                        if expected[index] != actual[index]:
                            detail = ""
                            if index:
                                detail = "\n" + "".join(difflib.unified_diff(
                                    expected[index].decode(errors="replace").splitlines(True),
                                    actual[index].decode(errors="replace").splitlines(True),
                                    fromfile="C", tofile=language,
                                ))[:8000]
                            self.fail(f"{name}/{label}: different {stream}{detail}")


if __name__ == "__main__":
    unittest.main()
