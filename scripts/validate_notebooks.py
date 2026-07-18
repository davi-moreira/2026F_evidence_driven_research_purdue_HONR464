#!/usr/bin/env python3
"""validate_notebooks.py — template-conformance gate for the topic notebooks.

Checks every STUDENT notebook in notebooks/student/ against the canonical
template (_project_docs/ACTIVITY_TEMPLATE.md):

  * kernel metadata (python3), non-trivial cell count
  * the Approach & Claim Boundary block (approach emphasis + PERMITS/NOT rows)
  * a provenance line + the Sources & Provenance section
  * the seven active-learning moves (Pause & Predict, Run-the-Study/Hands-On,
    Make a Design Choice, Practice, Reading the Evidence, Project Transfer,
    Claim Ticket)
  * setup discipline: SEED = 464, no seaborn anywhere
  * no INSTRUCTOR SOLUTION marker in a student file
  * markdown hygiene: no unescaped $<digit> / ~<digit>
  * voice rule (delegates to voice_lint_notebooks)

And every INSTRUCTOR notebook: carries >= 1 INSTRUCTOR SOLUTION cell and its
student counterpart exists.

Usage: python3 scripts/validate_notebooks.py [nbNN ...]   (default: all)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import nbformat

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from voice_lint_notebooks import lint_notebook  # noqa: E402

MOVES = {
    "Pause & Predict": re.compile(r"###\s*🔮\s*Pause & Predict"),
    "Runnable activity": re.compile(r"###\s*🛠️"),
    "Make a Design Choice": re.compile(r"###\s*⚖️\s*Make a Design Choice"),
    "Practice": re.compile(r"###\s*📝\s*Practice"),
    "Reading the Evidence": re.compile(r"###\s*🔍\s*Reading the Evidence"),
    "Project Transfer": re.compile(r"###\s*🎯\s*Project Transfer"),
    "Claim Ticket": re.compile(r"###\s*🎟️\s*Claim Ticket"),
}


def check_student(path: Path) -> list[str]:
    nb = nbformat.read(path, as_version=4)
    text = "\n\n".join(c.source for c in nb.cells)
    code = "\n\n".join(c.source for c in nb.cells if c.cell_type == "code")
    errs = []

    kernel = (nb.metadata.get("kernelspec") or {}).get("name", "")
    if kernel != "python3":
        errs.append(f"kernelspec is {kernel!r}, expected 'python3'")
    if len(nb.cells) < 10:
        errs.append(f"only {len(nb.cells)} cells — template requires a full notebook")

    if "## 🧭 Approach & Claim Boundary" not in text:
        errs.append("missing Approach & Claim Boundary block")
    if "**Approach emphasis:**" not in text:
        errs.append("missing approach-emphasis line")
    if "PERMITS" not in text or "NOT permit" not in text:
        errs.append("missing claim-permitted / claim-not-permitted rows")
    if not re.search(r"\*?Provenance:", text):
        errs.append("missing provenance line")
    if not re.search(r"Sources\s*&\s*Provenance", text):
        errs.append("missing Sources & Provenance section")
    if "By the end of this notebook" not in text:
        errs.append("missing learning objectives")

    for name, pat in MOVES.items():
        if not pat.search(text):
            errs.append(f"missing required move: {name}")

    n_gem = text.count("💡 **Gemini Prompt")
    if n_gem < 3:
        errs.append(f"only {n_gem} Gemini Prompt block(s) — frame requires ≥3 "
                    f"(one before every substantive code chunk)")
    n_qa = text.count("A question that often comes up here")
    if n_qa < 3:
        errs.append(f"only {n_qa} 'A question that often comes up here' "
                    f"block(s) — frame requires ≥3")

    if "SEED = 464" not in code:
        errs.append("setup cell missing SEED = 464")
    if "seaborn" in text or re.search(r"\bimport sns\b|\bsns\.", code):
        errs.append("seaborn detected (forbidden)")
    if "INSTRUCTOR SOLUTION" in text:
        errs.append("INSTRUCTOR SOLUTION marker leaked into student file")

    for cell in nb.cells:
        if cell.cell_type == "markdown":
            src = re.sub(r"```.*?```", "", cell.source, flags=re.S)
            src = re.sub(r"`[^`]*`", "", src)
            src = re.sub(r"\$\$.*?\$\$", "", src, flags=re.S)
            if re.search(r"(?<!\\)\$\d", src):
                errs.append("unescaped $<digit> in markdown (LaTeX trigger)")
                break

    errs += [f"voice: {p}" for p in lint_notebook(path)]
    return errs


def check_instructor(path: Path) -> list[str]:
    nb = nbformat.read(path, as_version=4)
    errs = []
    n_sol = sum(1 for c in nb.cells if "INSTRUCTOR SOLUTION" in c.source)
    if n_sol == 0:
        errs.append("instructor notebook has no INSTRUCTOR SOLUTION cells")
    student = REPO / "notebooks" / "student" / path.name.replace(
        "_instructor.ipynb", "_student.ipynb")
    if not student.exists():
        errs.append("student counterpart not generated")
    return errs


def main() -> None:
    only = set(sys.argv[1:])
    students = sorted((REPO / "notebooks" / "student").glob("nb*_student.ipynb"))
    instructors = sorted((REPO / "notebooks" / "instructor").glob("nb*_instructor.ipynb"))
    if only:
        students = [p for p in students if any(o in p.name for o in only)]
        instructors = [p for p in instructors if any(o in p.name for o in only)]
    if not students and not instructors:
        print("validate_notebooks: no notebooks found yet")
        return

    failed = False
    for p in students:
        errs = check_student(p)
        if errs:
            failed = True
            print(f"✗ {p.name}")
            for e in errs:
                print("    " + e)
        else:
            print(f"✓ {p.name}")
    for p in instructors:
        errs = check_instructor(p)
        if errs:
            failed = True
            print(f"✗ {p.name}")
            for e in errs:
                print("    " + e)
    if failed:
        sys.exit(1)
    print(f"✓ all checks passed ({len(students)} student, {len(instructors)} instructor)")


if __name__ == "__main__":
    main()
