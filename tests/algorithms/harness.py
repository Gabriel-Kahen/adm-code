"""Share the C build helpers while keeping each suite directly runnable."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "regressions"))
from support import ROOT as ROOT
from support import compiled_c as compiled_c
from support import run_c as run_c
from support import run_executable as run_executable
