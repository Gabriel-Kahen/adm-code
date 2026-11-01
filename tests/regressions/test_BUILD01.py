import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from support import ROOT, run_c


class SourceBuild(unittest.TestCase):
    def test_default_build_with_both_modern_compilers(self):
        for compiler in ["gcc", "clang"]:
            with (
                self.subTest(compiler=compiler),
                tempfile.TemporaryDirectory(prefix="adm-source-build-") as name,
            ):
                directory = Path(name)
                for pattern in ["*.c", "*.h", "Makefile"]:
                    for source in ROOT.glob(pattern):
                        shutil.copy2(source, directory / source.name)
                result = subprocess.run(
                    ["make", "-B", "-j2", "all", "CC=" + compiler],
                    cwd=directory,
                    text=True,
                    capture_output=True,
                    timeout=120,
                )
                self.assertEqual(result.returncode, 0, result.stdout + "\n" + result.stderr)
                self.assertNotIn("-fcommon", result.stdout)

    def test_legacy_annealing_builds_with_explicit_function_types(self):
        code = r"""
#include <stdio.h>
double solution_cost();
double transition();
double random_float();
#include "original/annealing.c"
int initialize_solution(int n, tsp_solution *s) {
    s->n = n;
    return 0;
}
int random_solution(tsp_solution *s) {
    return 0;
}
int copy_solution(tsp_solution *a, tsp_solution *b) {
    *b = *a;
    return 0;
}
int print_solution(tsp_solution *s) {
    return 0;
}
int random_int(int a, int b) {
    return a;
}
double random_float(double a, double b) {
    return a;
}
double solution_cost(tsp_solution *s, tsp_instance *t) {
    return 1.0;
}
double transition(tsp_solution *s, tsp_instance *t, int i, int j) {
    return 0.0;
}
int main(void) {
    tsp_instance t;
    tsp_solution s;
    t.n = 2;
    solution_count = 0;
    hill_climbing(&t, &s);
    return solution_count != 1;
}
"""
        result = run_c(code, flags=["-std=gnu89", "-w"])
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_legacy_tsp_declares_hypot(self):
        code = r"""
#include <stdio.h>
#include <limits.h>
int random_permutation(int *, int);
int repeated_annealing();
void swap(int *, int *);
#define main tsp_demo_main
#include "original/tsp.c"
#undef main
int solution_count;
int random_permutation(int *a, int n) {
    return 0;
}
int repeated_annealing(tsp_instance *t, int n, tsp_solution *s) {
    return 0;
}
void swap(int *a, int *b) {
    int old = *a;
    *a = *b;
    *b = old;
}
int main(void) {
    tsp_instance t;
    tsp_solution s;
    t.n = 2;
    initialize_solution(2, &s);
    t.p[1].x = INT_MIN;
    t.p[1].y = 0;
    t.p[2].x = INT_MAX;
    t.p[2].y = 0;
    return distance(&s, 1, 2, &t) != 4294967295.0;
}
"""
        result = run_c(code, flags=["-std=gnu89", "-Werror=implicit-function-declaration"])
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_script_delegates_and_preserves_failure(self):
        with tempfile.TemporaryDirectory(prefix="adm-test-entry-") as name:
            directory = Path(name)
            make = directory / "make"
            make.write_text('#!/bin/sh\nprintf "%s\\n" "$PWD" "$@"\nexit 7\n')
            make.chmod(0o755)
            result = subprocess.run(
                ["sh", str(ROOT / "test-script.sh")],
                cwd=directory,
                env={
                    **os.environ,
                    "PATH": str(directory) + os.pathsep + os.environ.get("PATH", ""),
                },
                text=True,
                capture_output=True,
                timeout=5,
            )
            self.assertEqual(result.returncode, 7, result.stderr)
            self.assertEqual(result.stdout.splitlines(), [str(ROOT), "test"])


if __name__ == "__main__":
    unittest.main()
