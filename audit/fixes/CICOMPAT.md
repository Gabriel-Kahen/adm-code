# CICOMPAT: Compile legacy regression callers on both Clang 18 and Clang 22

Audit baseline: `f74a015406c0821aa23390e3983d2c385712e3f4`.

Upstream issue: No matching issue found among all open and closed upstream issues checked on 2026-10-31.

Regression: `python tests/regressions/test_DP03.py`.

The regression compiles the actual implementation and asserts corrected behavior for this finding.
