#!/usr/bin/env python3
"""check_runtime_syntax.py — every tracked script must PARSE on CI's Python.

The gap this closes (2026-08-24). The workflow pins **Python 3.11**; this
machine's `.venv` is newer. Python 3.12 relaxed f-strings (PEP 701) so that a
backslash may appear inside the expression part, and two generators quietly
started relying on it:

    f"{re.sub(r'\\s+', ' ', r['title']).strip()}"
    f"{len(re.findall(r'href=\\"https?:', frag))} links"

Both run fine locally and are a hard `SyntaxError` on 3.11, so `validate`
failed on every push for days while every local gate stayed green —
`ci_gates_local.py` could not catch it, because it runs the steps with the
local interpreter, which is exactly the interpreter that is wrong.

So this gate does not trust the interpreter it is running under. It reads the
pinned version out of the workflow and compiles every tracked `.py` with an
interpreter of THAT version: itself when the versions already match (which is
the case on CI), otherwise `pythonX.Y` from PATH. A missing interpreter is a
FAILURE, never a skip — a silent skip is what shipped the break.

Usage:
    python3 scripts/check_runtime_syntax.py
    python3 scripts/check_runtime_syntax.py --version 3.11   # override the pin
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
WORKFLOW = REPO / ".github" / "workflows" / "validate.yml"


def pinned_version() -> tuple[int, int]:
    """The `python-version:` actions/setup-python is pinned to, as (major, minor).

    Read rather than hardcoded: when the workflow moves to a newer Python this
    gate moves with it instead of certifying a version nothing runs any more.
    """
    import yaml

    data = yaml.safe_load(WORKFLOW.read_text())
    found: set[str] = set()
    for job in data.get("jobs", {}).values():
        for step in job.get("steps", []):
            if str(step.get("uses", "")).startswith("actions/setup-python"):
                v = step.get("with", {}).get("python-version")
                if v is not None:
                    found.add(str(v))
    if not found:
        raise SystemExit("✗ no actions/setup-python python-version in the workflow")
    if len(found) > 1:
        raise SystemExit(f"✗ jobs pin different Pythons: {sorted(found)}")
    major, _, minor = found.pop().partition(".")
    return int(major), int(minor or 0)


def tracked_scripts() -> list[str]:
    out = subprocess.run(["git", "ls-files", "*.py"], cwd=REPO,
                         capture_output=True, text=True, check=True).stdout
    return sorted(out.split())


def compile_here(files: list[str]) -> list[tuple[str, int, str]]:
    """Compile each file in THIS interpreter; return (file, line, message)."""
    bad: list[tuple[str, int, str]] = []
    for f in files:
        src = (REPO / f).read_text(encoding="utf-8")
        try:
            compile(src, f, "exec")
        except SyntaxError as e:
            bad.append((f, e.lineno or 0, e.msg))
    return bad


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", help="target as X.Y (default: the workflow pin)")
    ap.add_argument("--_emit", action="store_true", help=argparse.SUPPRESS)
    args = ap.parse_args()

    if args._emit:                       # the re-exec'd child: report and exit
        print(json.dumps(compile_here(tracked_scripts())))
        return 0

    want = (tuple(int(p) for p in args.version.split(".")[:2])
            if args.version else pinned_version())
    files = tracked_scripts()
    tag = f"{want[0]}.{want[1]}"

    if sys.version_info[:2] == want:
        bad = compile_here(files)
        how = f"this interpreter ({sys.version.split()[0]})"
    else:
        exe = shutil.which(f"python{tag}")
        if not exe:
            print(f"✗ runtime syntax gate needs Python {tag} — the version "
                  f"`.github/workflows/validate.yml` pins — and no `python{tag}` "
                  f"is on PATH.\n"
                  f"  This interpreter is {sys.version.split()[0]}, which accepts "
                  f"syntax that CI rejects, so it cannot stand in.\n"
                  f"  Install it:  brew install python@{tag}")
            return 1
        proc = subprocess.run([exe, __file__, "--_emit"],
                              capture_output=True, text=True)
        if proc.returncode != 0:
            print(f"✗ could not run the Python {tag} probe:\n{proc.stderr.strip()}")
            return 1
        bad = [tuple(row) for row in json.loads(proc.stdout)]
        how = f"{exe} ({tag})"

    if bad:
        print(f"✗ {len(bad)} tracked script(s) do not parse on Python {tag}, "
              f"which is what CI runs:")
        for f, line, msg in bad:
            print(f"    {f}:{line} — {msg}")
        print("  They may run fine locally on a newer interpreter. CI will "
              "still fail on every push until they are fixed.")
        return 1

    print(f"✓ runtime syntax clean — {len(files)} tracked script(s) parse on "
          f"Python {tag}, checked with {how}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
