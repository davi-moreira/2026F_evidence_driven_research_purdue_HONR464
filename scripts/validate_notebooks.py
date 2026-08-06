#!/usr/bin/env python3
"""validate_notebooks.py — template-conformance gate for the topic notebooks (v2).

Validates the v2 weekly notebooks registered in scripts/notebooks_map.py against
the canonical template (_project_docs/ACTIVITY_TEMPLATE.md). Only registered v2
notebooks are checked; stale v1 files (different slugs) are ignored — the
registry is the single source of truth.

Every STUDENT notebook must carry:

  * kernel metadata (python3), non-trivial cell count
  * the Inquiry & Claim Boundary block (inquiry emphasis + PERMITS/NOT rows)
  * the Sources & Provenance section + learning objectives
  * the seven active-learning moves (Predict First, Run the Study,
    Make a Design Choice, Practice, Read the Evidence, Take It to Your Project,
    Defend Your Decision — the closing move), each present in EVERY lecture
    AND above that lecture's `### ⏸` optional-depth line (D33: the whole
    path runs in class; nothing below ⏸ is required), plus a per-lecture
    📒 ledger row above the line (nb13 conference week: presence only)
  * the SRL opener: one `### 🧩 Research Puzzle` per `# Lecture N` (async-only
    modules are exempt)
  * the five required AI-collaboration blocks (SDIIVDD): AI Research Partner
    briefing, Modify the Prompt, Interrogate the Output, Human-Only Checkpoint,
    AI Research Ledger
  * ≥4 AI prompt blocks and ≥3 inline Q&A blocks
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
from notebooks_map import (  # noqa: E402
    NOTEBOOKS, MS_NOTEBOOKS, student_filename, instructor_filename,
    ms_student_filename,
)

# Headings are matched by their name text at level-3, robust to emoji variation
# (e.g. the 🧑‍⚖️ ZWJ sequence). The Runnable move keeps its emoji marker because
# its wording varies ("Run the Study" / "Hands-On: …").
MOVES = {
    "Predict First": re.compile(r"^\s*###[^\n]*Predict First", re.M),
    "Runnable activity": re.compile(r"^\s*###\s*🛠️", re.M),
    "Make a Design Choice": re.compile(r"^\s*###[^\n]*Make a Design Choice", re.M),
    "Practice": re.compile(r"^\s*###[^\n]*Practice", re.M),
    "Read the Evidence": re.compile(r"^\s*###[^\n]*Read the Evidence", re.M),
    "Take It to Your Project": re.compile(r"^\s*###[^\n]*Take It to Your Project", re.M),
    "Defend Your Decision": re.compile(r"^\s*###[^\n]*Defend Your Decision", re.M),
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
BRIEF_RE = re.compile(r"^\s*###[^\n]*SRL Lead Brief", re.M)
LECTURE_RE = re.compile(r"^\s*#\s*Lecture\s+\d", re.M)

# Communication/performance weeks satisfy the runnable move with structured
# criticism or delivery rounds instead (template §7 Variants). D49: nb12 is no
# longer a communication week — Studio 12 runs three seeded cells per its own
# lectures, so it satisfies the runnable move directly and loses its exemption.
RUNNABLE_EXEMPT = {11, 13}

# D33: the whole seven-move path runs INSIDE the 50-minute lecture — every
# move (and the lecture's 📒 ledger row) must sit ABOVE that lecture's
# `### ⏸` optional-depth line. nb13 (conference week) is exempt from the
# placement rule only: its reflection path completes at the Expo itself.
PLACEMENT_EXEMPT = {13}

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
    # D23: the pipe-separated build-provenance metadata line is retired from
    # student-facing cells; the Sources & Provenance section (real, retrievable
    # sources) remains required.
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

    # D32: the seven moves are PER LECTURE (nb01 is the orientation exception;
    # async modules keep the notebook-level requirement above).
    # D33: each move must also sit ABOVE the lecture's ⏸ optional-depth line —
    # the whole path is in class; nothing below ⏸ is required. The lecture's
    # 📒 ledger row is per lecture and in class too. nb13 keeps presence but
    # is exempt from placement (conference week).
    if not is_async and nb_num != 1:
        segments = re.split(r"(?m)^#\s*Lecture\s+\d", text)[1:]
        placed = nb_num not in PLACEMENT_EXEMPT
        for li, seg in enumerate(segments, 1):
            above = re.split(r"###\s*⏸", seg, maxsplit=1)[0]
            scope = above if placed else seg
            for name, pat in MOVES.items():
                if name == "Runnable activity" and nb_num in RUNNABLE_EXEMPT:
                    continue
                if not pat.search(scope):
                    where = " above the ⏸ line" if placed else ""
                    errs.append(f"Lecture {li}: missing move '{name}'{where} "
                                f"(D33: all seven moves in class, every lecture)")
            if placed and not AI_BLOCKS["AI Research Ledger"].search(above):
                errs.append(f"Lecture {li}: missing 📒 AI Research Ledger above "
                            f"the ⏸ line (D33: a ledger row closes every lecture)")
        # D33: the notebook-required SDIIVDD blocks are in-class work as well.
        if placed and segments:
            above_all = "\n\n".join(
                re.split(r"###\s*⏸", s, maxsplit=1)[0] for s in segments)
            for name in ("Modify the Prompt", "Interrogate the Output",
                         "Human-Only Checkpoint"):
                if not AI_BLOCKS[name].search(above_all):
                    errs.append(f"required AI block '{name}' must appear above "
                                f"a ⏸ line (D33: in-class, not homework)")

    for name, pat in AI_BLOCKS.items():
        if name == "AI Research Partner briefing" and nb_num != 1:
            continue  # the briefing lives in nb01 (orientation) + the book only
        if not pat.search(text):
            errs.append(f"missing required AI-collaboration block: {name}")

    # SRL opener: one SRL Lead Brief + one Research Puzzle per lecture
    # (async-only modules exempt). The brief is student-visible (D22).
    n_puzzle = len(PUZZLE_RE.findall(text))
    n_brief = len(BRIEF_RE.findall(text))
    n_lecture = len(LECTURE_RE.findall(text))
    if not is_async:
        need = max(1, n_lecture)
        if n_puzzle < need:
            errs.append(f"only {n_puzzle} '🧩 Research Puzzle' opener(s) — need "
                        f"{need} (one per lecture; {n_lecture} '# Lecture N' heading(s))")
        if n_brief < need:
            errs.append(f"only {n_brief} '🎤 SRL Lead Brief' cell(s) — need "
                        f"{need} (one per lecture, right after '# Lecture N'; D22)")
        # D34: exactly ONE `### ⏸` HEADING per lecture (a character count can
        # be satisfied by prose that merely mentions ⏸, which let a missing
        # pause heading pass the placement checks vacuously).
        if nb_num != 1:
            segments = re.split(r"(?m)^#\s*Lecture\s+\d", text)[1:] or [text]
            for li, seg in enumerate(segments, 1):
                n_pause = len(re.findall(r"(?m)^\s*###\s*⏸", seg))
                if n_pause != 1:
                    errs.append(f"Lecture {li}: {n_pause} '### ⏸' heading(s) — "
                                f"need exactly 1 (D34)")
            # D34: the notebook close (Wrap-Up, Sources & Provenance) is
            # required reading — it must sit ABOVE the final lecture's ⏸ line
            # (nbbuild hoists it; nb13's conference path is exempt).
            if nb_num not in PLACEMENT_EXEMPT and segments:
                last = segments[-1]
                above = re.split(r"###\s*⏸", last, maxsplit=1)[0]
                for name, patt in (
                        ("Wrap-Up", r"(?m)^##\s*\d*\.?\s*Wrap-?Up"),
                        ("Sources & Provenance",
                         r"(?m)^##\s*\d*\.?\s*Sources\s*&\s*Provenance")):
                    if re.search(patt, last) and not re.search(patt, above):
                        errs.append(f"{name} sits below the final ⏸ line "
                                    f"(D34: the notebook close is required)")

    n_gem = text.count("💡 **AI Prompt")
    if n_gem < 4:
        errs.append(f"only {n_gem} AI Prompt block(s) — frame requires ≥4 "
                    f"(one before every substantive code chunk)")

    # D34: at most ONE required (non-🏠) AI prompt above each governed
    # lecture's ⏸ line — the designated live exchange. nb03's single lecture
    # is allowed two (template P3 §2: the live prompt + the gap-attack its
    # SDIIVDD chain is built on). Optional prompts carry 🏠 in the same cell.
    if not is_async and nb_num not in (1,) and nb_num not in PLACEMENT_EXEMPT:
        allowed = 2 if nb_num == 3 else 1
        lect, in_optional, req = 0, False, {}
        for c in nb.cells:
            s = c.source
            if c.cell_type == "markdown" and re.search(r"(?m)^#\s*Lecture\s+\d", s):
                lect, in_optional = lect + 1, False
                req.setdefault(lect, 0)
                continue
            if lect == 0:
                continue
            if c.cell_type == "markdown" and re.search(r"(?m)^\s*###\s*⏸", s):
                in_optional = True
                continue
            if in_optional:
                continue
            n_p = s.count("💡 **AI Prompt")
            if n_p and "🏠" not in s:
                req[lect] += n_p
        for li, n_req in sorted(req.items()):
            if n_req > allowed:
                errs.append(f"Lecture {li}: {n_req} required (non-🏠) AI "
                            f"prompt(s) above the ⏸ line — max {allowed} "
                            f"(D34 one-live-prompt rule)")

    # D34: the retired label must not resurface.
    if re.search(r"[Hh]omework[ -]depth", text):
        errs.append("stale 'homework depth' label — D34 wording is "
                    "'🏠 Optional depth'")
    if text.count("After running, verify") < n_gem:
        errs.append("each AI Prompt must be followed by an "
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


def check_ms_student(path: Path) -> list[str]:
    """Reduced studio contract for a milestone studio notebook (msNN)."""
    nb = nbformat.read(path, as_version=4)
    text = "\n\n".join(c.source for c in nb.cells)
    errs = [f"missing required studio block: {name}"
            for name, pat in MS_REQUIRED.items() if not pat.search(text)]
    if text.count("💡 **AI Prompt") < 1:
        errs.append("studio notebook needs ≥1 AI Prompt block")
    if "INSTRUCTOR SOLUTION" in text:
        errs.append("INSTRUCTOR SOLUTION marker leaked into student file")
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
    args = sys.argv[1:]
    ms_args = [a for a in args if a.lower().startswith("ms")]
    nb_args = [a for a in args if not a.lower().startswith("ms")]
    no_filter = not args                 # bare call → validate everything
    run_topics = no_filter or bool(nb_args)
    run_studios = no_filter or bool(ms_args)
    student_dir = REPO / "notebooks" / "student"
    instructor_dir = REPO / "notebooks" / "instructor"

    checked_s = checked_i = 0
    failed = False
    for n in (_selected(set(nb_args)) if run_topics else []):
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
    # With explicit ms args validate exactly those; a bare call sweeps all.
    checked_ms = 0
    if run_studios:
        if ms_args:
            ms_paths = []
            for a in ms_args:
                m = re.search(r"\d+", a)
                if m:
                    ms_paths.append(student_dir / ms_student_filename(int(m.group())))
        else:
            ms_paths = sorted(student_dir.glob("ms*_student.ipynb"))
        for sp in ms_paths:
            if not sp.exists():
                failed = True
                print(f"✗ {sp.name}: studio notebook not built")
                continue
            checked_ms += 1
            errs = check_ms_student(sp)
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
