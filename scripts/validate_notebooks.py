#!/usr/bin/env python3
"""validate_notebooks.py — template-conformance gate for the topic notebooks (v2).

Validates the v2 weekly notebooks registered in scripts/notebooks_map.py against
the canonical template (_project_docs/ACTIVITY_TEMPLATE.md). Only registered v2
notebooks are checked; stale v1 files (different slugs) are ignored — the
registry is the single source of truth.

Every STUDENT notebook must carry:

  * kernel metadata (python3), non-trivial cell count
  * the Inquiry & Claim Boundary block (inquiry emphasis + PERMITS/NOT rows)
  * a provenance line + the Sources & Provenance section + learning objectives
  * the seven active-learning moves (Pause & Predict, Run-the-Study/Hands-On,
    Make a Design Choice, Practice, Reading the Evidence, Project Transfer,
    Exit Defense — the v2 closing move that replaces the Claim Ticket)
  * the SRL opener: one `### 🧩 Research Puzzle` per `# Lecture N` (async-only
    modules are exempt)
  * the five required AI-collaboration blocks (SDIIVDD): AI Research Partner
    briefing, Modify the Prompt, Interrogate the Output, Human-Only Checkpoint,
    AI Research Ledger
  * ≥3 Gemini prompt blocks and ≥3 inline Q&A blocks
  * setup discipline: SEED = 464, no seaborn anywhere
  * no INSTRUCTOR SOLUTION marker in a student file
  * markdown hygiene: no unescaped $<digit>
  * voice rule (delegates to voice_lint_notebooks)

And every INSTRUCTOR notebook: carries >= 1 INSTRUCTOR SOLUTION cell and its
student counterpart exists.

Usage: python3 scripts/validate_notebooks.py [nbNN ...]   (default: all registered)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import nbformat

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from voice_lint_notebooks import lint_notebook  # noqa: E402
from notebooks_map import NOTEBOOKS, student_filename, instructor_filename  # noqa: E402

# Headings are matched by their name text at level-3, robust to emoji variation
# (e.g. the 🧑‍⚖️ ZWJ sequence). The Runnable move keeps its emoji marker because
# its wording varies ("Run the Study" / "Hands-On: …").
MOVES = {
    "Pause & Predict": re.compile(r"^\s*###[^\n]*Pause & Predict", re.M),
    "Runnable activity": re.compile(r"^\s*###\s*🛠️", re.M),
    "Make a Design Choice": re.compile(r"^\s*###[^\n]*Make a Design Choice", re.M),
    "Practice": re.compile(r"^\s*###[^\n]*Practice", re.M),
    "Reading the Evidence": re.compile(r"^\s*###[^\n]*Reading the Evidence", re.M),
    "Project Transfer": re.compile(r"^\s*###[^\n]*Project Transfer", re.M),
    "Exit Defense": re.compile(r"^\s*###[^\n]*Exit Defense", re.M),
}

# The high-intensity AI-collaboration blocks (SDIIVDD); each required ≥1.
AI_BLOCKS = {
    "AI Research Partner briefing": re.compile(r"^\s*###[^\n]*AI Research Partner", re.M),
    "Modify the Prompt": re.compile(r"^\s*###[^\n]*Modify the Prompt", re.M),
    "Interrogate the Output": re.compile(r"^\s*###[^\n]*Interrogate the Output", re.M),
    "Human-Only Checkpoint": re.compile(r"^\s*###[^\n]*Human-Only Checkpoint", re.M),
    "AI Research Ledger": re.compile(r"^\s*###[^\n]*AI Research Ledger", re.M),
}

PUZZLE_RE = re.compile(r"^\s*###[^\n]*Research Puzzle", re.M)
LECTURE_RE = re.compile(r"^\s*#\s*Lecture\s+\d", re.M)

# Communication/performance weeks satisfy the runnable move with structured
# criticism or delivery rounds instead (template §7 Variants).
RUNNABLE_EXEMPT = {10, 11, 12}

# Milestone studio notebooks (msNN) — reduced required set (template, final §).
MS_REQUIRED = {
    "milestone header": re.compile(r"\*\*Milestone M\d{1,2} · studio notebook\*\*"),
    "Definition of Done": re.compile(r"^\s*##[^\n]*Definition of Done", re.M),
    "AI Research Partner briefing": re.compile(r"^\s*###[^\n]*AI Research Partner", re.M),
    "Red-Team Exchange": re.compile(r"^\s*###[^\n]*Red-Team Exchange", re.M),
    "AI Research Ledger": re.compile(r"^\s*###[^\n]*AI Research Ledger", re.M),
    "Submission Checklist": re.compile(r"^\s*###[^\n]*Submission Checklist", re.M),
}


def check_student(path: Path, is_async: bool, nb_num: int | None = None) -> list[str]:
    nb = nbformat.read(path, as_version=4)
    text = "\n\n".join(c.source for c in nb.cells)
    code = "\n\n".join(c.source for c in nb.cells if c.cell_type == "code")
    errs = []

    kernel = (nb.metadata.get("kernelspec") or {}).get("name", "")
    if kernel != "python3":
        errs.append(f"kernelspec is {kernel!r}, expected 'python3'")
    if len(nb.cells) < 10:
        errs.append(f"only {len(nb.cells)} cells — template requires a full notebook")

    if "## 🧭 Inquiry & Claim Boundary" not in text:
        errs.append("missing Inquiry & Claim Boundary block")
    if "**Inquiry emphasis:**" not in text:
        errs.append("missing inquiry-emphasis line")
    if "**Design pathway:**" not in text:
        errs.append("missing design-pathway line (library pathway or 'cross-cutting')")
    if "PERMITS" not in text or "NOT permit" not in text:
        errs.append("missing claim-permitted / claim-not-permitted rows")
    if not re.search(r"\*?Provenance:", text):
        errs.append("missing provenance line")
    if not re.search(r"Sources\s*&\s*Provenance", text):
        errs.append("missing Sources & Provenance section")
    if "By the end of this notebook" not in text:
        errs.append("missing learning objectives")
    if not re.search(r"\*\*Topic \d", text):
        errs.append("missing '**Topic NN · …**' header line")
    if "colab.research.google.com/github/" not in text:
        errs.append("missing Colab badge")
    if not re.search(r"^\s*##[^\n]*Wrap-?Up", text, re.M | re.I):
        errs.append("missing Wrap-Up section")
    if "Thank you!" not in text:
        errs.append("missing final thank-you cell")

    for name, pat in MOVES.items():
        if name == "Runnable activity" and nb_num in RUNNABLE_EXEMPT:
            continue
        if not pat.search(text):
            errs.append(f"missing required move: {name}")

    for name, pat in AI_BLOCKS.items():
        if not pat.search(text):
            errs.append(f"missing required AI-collaboration block: {name}")

    # SRL opener: one Research Puzzle per lecture (async-only modules exempt).
    n_puzzle = len(PUZZLE_RE.findall(text))
    n_lecture = len(LECTURE_RE.findall(text))
    if not is_async:
        need = max(1, n_lecture)
        if n_puzzle < need:
            errs.append(f"only {n_puzzle} '🧩 Research Puzzle' opener(s) — need "
                        f"{need} (one per lecture; {n_lecture} '# Lecture N' heading(s))")

    n_gem = text.count("💡 **Gemini Prompt")
    if n_gem < 3:
        errs.append(f"only {n_gem} Gemini Prompt block(s) — frame requires ≥3 "
                    f"(one before every substantive code chunk)")
    if text.count("After running, verify") < n_gem:
        errs.append("each Gemini Prompt must be followed by an "
                    "'After running, verify' checklist")
    n_qa = text.count("A question that often comes up here")
    if n_qa < 3:
        errs.append(f"only {n_qa} 'A question that often comes up here' "
                    f"block(s) — frame requires ≥3")

    if "SEED = 464" not in code:
        errs.append("setup cell missing SEED = 464")
    if "default_rng" not in code:
        errs.append("setup cell missing np.random.default_rng(SEED)")
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


def _selected(only: set[str]) -> list[int]:
    """Registered notebook numbers, optionally filtered by nbNN args."""
    nums = sorted(NOTEBOOKS)
    if only:
        wanted = {int(m.group(1)) for o in only
                  if (m := re.search(r"(?:nb)?0*(\d+)", o, re.I))}
        nums = [n for n in nums if n in wanted]
    return nums


def main() -> None:
    only = set(sys.argv[1:])
    student_dir = REPO / "notebooks" / "student"
    instructor_dir = REPO / "notebooks" / "instructor"

    checked_s = checked_i = 0
    failed = False
    for n in _selected(only):
        title = NOTEBOOKS[n][1]
        is_async = title.lower().startswith("async module")

        sp = student_dir / student_filename(n)
        if sp.exists():
            checked_s += 1
            errs = check_student(sp, is_async, nb_num=n)
            if errs:
                failed = True
                print(f"✗ {sp.name}")
                for e in errs:
                    print("    " + e)
            else:
                print(f"✓ {sp.name}")

        ip = instructor_dir / instructor_filename(n)
        if ip.exists():
            checked_i += 1
            errs = check_instructor(ip)
            if errs:
                failed = True
                print(f"✗ {ip.name}")
                for e in errs:
                    print("    " + e)

    # Milestone studio notebooks (msNN_*_student.ipynb): reduced required set.
    checked_ms = 0
    if not only:
        for sp in sorted(student_dir.glob("ms*_student.ipynb")):
            checked_ms += 1
            nb = nbformat.read(sp, as_version=4)
            text = "\n\n".join(c.source for c in nb.cells)
            errs = [f"missing required studio block: {name}"
                    for name, pat in MS_REQUIRED.items() if not pat.search(text)]
            if text.count("💡 **Gemini Prompt") < 1:
                errs.append("studio notebook needs ≥1 Gemini Prompt block")
            if "INSTRUCTOR SOLUTION" in text:
                errs.append("INSTRUCTOR SOLUTION marker leaked into student file")
            errs += [f"voice: {p}" for p in lint_notebook(sp)]
            if errs:
                failed = True
                print(f"✗ {sp.name}")
                for e in errs:
                    print("    " + e)
            else:
                print(f"✓ {sp.name}")

    if checked_s == 0 and checked_i == 0 and checked_ms == 0:
        print("validate_notebooks: no registered v2 notebooks built yet")
        return
    if failed:
        sys.exit(1)
    print(f"✓ all checks passed ({checked_s} student, {checked_i} instructor, "
          f"{checked_ms} studio)")


if __name__ == "__main__":
    main()
