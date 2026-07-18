#!/usr/bin/env python3
"""make_student.py — generate the committed student notebook from the
gitignored instructor notebook by stripping every cell whose source contains
the marker `INSTRUCTOR SOLUTION` (heading, code, or HTML-comment form).

Usage:
    python3 scripts/make_student.py notebooks/instructor/nb01_*_instructor.ipynb
    python3 scripts/make_student.py --all

Also clears outputs/execution counts in the student file (students run it
themselves) and verifies the result contains no marker and no empty shell.
"""
from __future__ import annotations

import sys
from pathlib import Path

import nbformat

REPO = Path(__file__).resolve().parent.parent
MARKER = "INSTRUCTOR SOLUTION"


def convert(instr_path: Path) -> Path:
    nb = nbformat.read(instr_path, as_version=4)
    kept = [c for c in nb.cells if MARKER not in c.source]
    dropped = len(nb.cells) - len(kept)
    for c in kept:
        if c.cell_type == "code":
            c.outputs = []
            c.execution_count = None
    nb.cells = kept

    out = (REPO / "notebooks" / "student" /
           instr_path.name.replace("_instructor.ipynb", "_student.ipynb"))
    nbformat.write(nb, out)

    # verification
    check = nbformat.read(out, as_version=4)
    assert all(MARKER not in c.source for c in check.cells), "marker survived strip!"
    assert len(check.cells) >= 8, f"student file suspiciously short ({len(check.cells)} cells)"
    print(f"✓ {out.name}: {len(kept)} cells kept, {dropped} instructor cells stripped")
    return out


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("usage: make_student.py <instructor.ipynb ...> | --all")
    if sys.argv[1] == "--all":
        targets = sorted((REPO / "notebooks" / "instructor").glob("nb*_instructor.ipynb"))
    else:
        targets = [Path(a) for a in sys.argv[1:]]
    if not targets:
        sys.exit("no instructor notebooks found")
    for t in targets:
        convert(t)


if __name__ == "__main__":
    main()
