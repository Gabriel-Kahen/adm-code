"""Compile real repository C with small, bounded regression callers."""
import os
from pathlib import Path
import subprocess
import tempfile
ROOT = Path(__file__).resolve().parents[2]
def run_c(code="", sources=(), data="", flags=(), timeout=5, compiler="gcc", args=()):
    with tempfile.TemporaryDirectory(prefix="adm-regression-") as temporary:
        directory=Path(temporary); files=[str(ROOT/p) for p in sources]
        if code:
            source=directory/"caller.c";source.write_text(code);files.insert(0,str(source))
        executable=directory/"test"
        command=[compiler,"-std=c99","-fcommon","-O0","-g","-I",str(ROOT),*flags,*files,"-lm","-o",str(executable)]
        compiled=subprocess.run(command,text=True,capture_output=True)
        if compiled.returncode:raise AssertionError(compiled.stderr)
        return subprocess.run([str(executable),*args],input=data,text=True,capture_output=True,timeout=timeout,
                              env={**os.environ,"ASAN_OPTIONS":"detect_leaks=0"})
