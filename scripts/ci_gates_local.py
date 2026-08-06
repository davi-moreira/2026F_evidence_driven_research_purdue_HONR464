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

Note what it does NOT cover: uncommitted work (it tests a COMMIT, because that
is what GitHub tests — run it after committing, before pushing), the runner's
case-sensitive filesystem, and its Linux/library versions. Pinned versions this
interpreter does not match are printed rather than assumed away.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
WORKFLOW = REPO / ".github/workflows/validate.yml"


def pin_drift(job: str = "static-gates") -> list[str]:
    """Pins the workflow installs that this interpreter does NOT match.

    The misconception gate EXECUTES seeded simulations, so a numpy that
    differs from the runner's can compute a different number here than there.
    Named, not silently tolerated.
    """
    import importlib.metadata as md
    data = yaml.safe_load(WORKFLOW.read_text())
    drift: list[str] = []
    for st in data["jobs"][job]["steps"]:
        cmd = st.get("run", "")
        if not cmd.strip().startswith("pip install"):
            continue
        for tok in re.findall(r'"?([A-Za-z0-9_.-]+)==([0-9][^"\s]*)"?', cmd):
            pkg, want = tok
            try:
                have = md.version(pkg)
            except md.PackageNotFoundError:
                drift.append(f"{pkg} pinned {want}, not installed here")
                continue
            if have != want:
                drift.append(f"{pkg} pinned {want}, this run uses {have}")
    return drift


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


def checkout_depth(job: str = "static-gates") -> int | None:
    """The `fetch-depth:` the workflow asks actions/checkout for (None = the
    action's default of 1, i.e. a SHALLOW checkout with no history)."""
    data = yaml.safe_load(WORKFLOW.read_text())
    for st in data["jobs"][job]["steps"]:
        if str(st.get("uses", "")).startswith("actions/checkout"):
            with_ = st.get("with") or {}
            return with_.get("fetch-depth")
    return None


def export_tree(ref: str, dest: Path) -> None:
    """Materialize `ref` the way actions/checkout does: a git clone containing
    ONLY tracked files, with history (the workflow asks for fetch-depth: 0).

    A clone, not `git archive`: gates may legitimately read git history — the
    A10 identity gate reads BOOK_ARCHITECTURE.yml at the epoch commit — and a
    bare export has no `.git`, which would fail them for the wrong reason.
    """
    subprocess.run(["git", "clone", "--quiet", "--no-checkout", str(REPO),
                    str(dest)], check=True)
    subprocess.run(["git", "checkout", "--quiet", "--detach", ref], cwd=dest,
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
    for d in pin_drift():
        print(f"  ⓘ version drift vs the runner: {d}")
    depth = checkout_depth()
    if depth != 0:
        # Say it rather than imply coverage: this mirror clones with full
        # history, so a gate that reads git history passes here and could
        # still fail on a shallow runner checkout.
        print(f"  ⓘ the workflow checks out with fetch-depth: {depth!r} "
              f"(shallow); this mirror has full history, so history-reading "
              f"gates are NOT certified by this run")
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
