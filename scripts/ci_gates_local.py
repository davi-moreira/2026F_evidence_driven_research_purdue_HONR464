#!/usr/bin/env python3
"""ci_gates_local.py — run the GitHub `validate` job the way CI actually sees it.

Why it exists: a CI checkout contains ONLY TRACKED files. `_production_kit/`
and `notebooks/instructor/` are gitignored, so a gate that reads them is green
here and red on GitHub. That divergence kept the `validate` workflow failing
from 2026-07-31 to 2026-08-06 — every local run passed, every push mailed a
failure notice.

This mirror closes it. It exports a committed tree into a temporary directory
(tracked files only, exactly what `actions/checkout` hands the runner) and runs
the steps THE WORKFLOW DECLARES — the list is read out of
`.github/workflows/validate.yml`, never retyped here, so the mirror cannot
drift from the job it mirrors.

    .venv/bin/python scripts/ci_gates_local.py               # HEAD, all steps
    .venv/bin/python scripts/ci_gates_local.py --ref origin/main
    .venv/bin/python scripts/ci_gates_local.py --only misconception
    .venv/bin/python scripts/ci_gates_local.py --keep        # keep the export

Note what it does NOT cover: uncommitted work. It tests a COMMIT, because that
is what GitHub tests. Run it after committing and before pushing.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
WORKFLOW = REPO / ".github/workflows/validate.yml"


def workflow_steps(job: str = "static-gates") -> list[tuple[str, str]]:
    """(step name, shell command) for every `run:` step of the job.

    Steps without a `run:` (checkout, setup-python) and the dependency install
    are dropped: this machine already has the interpreter and the libraries.
    """
    data = yaml.safe_load(WORKFLOW.read_text())
    steps = data["jobs"][job]["steps"]
    out: list[tuple[str, str]] = []
    for st in steps:
        cmd = st.get("run")
        if not cmd:
            continue
        name = st.get("name", cmd.splitlines()[0])
        if cmd.strip().startswith("pip install"):
            continue
        out.append((name, cmd.strip()))
    return out


def export_tree(ref: str, dest: Path) -> None:
    """Materialize `ref` as tracked-files-only, the way checkout does."""
    dest.mkdir(parents=True, exist_ok=True)
    archive = subprocess.run(["git", "archive", ref], cwd=REPO,
                             stdout=subprocess.PIPE, check=True)
    subprocess.run(["tar", "-x", "-C", str(dest)], input=archive.stdout,
                   check=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ref", default="HEAD", help="commit-ish to test (default HEAD)")
    ap.add_argument("--only", default="", metavar="TEXT",
                    help="run only steps whose name or command contains TEXT")
    ap.add_argument("--keep", action="store_true",
                    help="keep the exported tree and print its path")
    args = ap.parse_args()

    python = str(REPO / ".venv/bin/python")
    if not Path(python).exists():
        python = sys.executable

    steps = workflow_steps()
    if args.only:
        steps = [(n, c) for n, c in steps
                 if args.only.lower() in n.lower() or args.only.lower() in c.lower()]
    if not steps:
        print("✗ no matching steps in .github/workflows/validate.yml")
        return 1

    sha = subprocess.run(["git", "rev-parse", "--short", args.ref], cwd=REPO,
                         capture_output=True, text=True, check=True).stdout.strip()
    tmp = Path(tempfile.mkdtemp(prefix="ci-gates-"))
    export = tmp / "checkout"
    print(f"→ CI-parity run of {len(steps)} step(s) against {args.ref} ({sha}), "
          f"tracked files only")
    export_tree(args.ref, export)

    failures: list[str] = []
    try:
        for name, cmd in steps:
            # The workflow calls `python3`; use this repo's interpreter, which
            # has the libraries the gates import.
            shell_cmd = cmd.replace("python3 ", f"{python} ")
            proc = subprocess.run(shell_cmd, shell=True, cwd=export,
                                  capture_output=True, text=True)
            tail = (proc.stdout + proc.stderr).strip().splitlines()
            if proc.returncode == 0:
                print(f"  ✓ {name}")
            else:
                failures.append(name)
                print(f"  ✗ {name}  (exit {proc.returncode})")
                for line in tail[-20:]:
                    print(f"      {line}")
    finally:
        if args.keep:
            print(f"  export kept at {export}")
        else:
            shutil.rmtree(tmp, ignore_errors=True)

    if failures:
        print(f"✗ CI parity FAILED — {len(failures)} step(s) that pass locally "
              f"would fail on GitHub: {', '.join(failures)}")
        return 1
    print(f"✓ CI parity clean — all {len(steps)} workflow step(s) pass on a "
          f"tracked-files-only checkout of {sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
