#!/bin/sh
# Historical output fixtures remain reference data; use the corrected regressions.
cd "$(dirname "$0")" || exit 1
exec make test
