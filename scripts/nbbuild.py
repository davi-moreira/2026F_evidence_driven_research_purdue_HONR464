#!/usr/bin/env python3
"""nbbuild.py — build → execute → strip → validate one topic notebook.

Authoring convention: each notebook's cells live in a LOCAL, gitignored source
module `_production_kit/nb_sources/nbNN_<slug>.py` exporting

    CELLS: list[tuple[str, str]]     # ("md" | "code", source)

(the module contains INSTRUCTOR SOLUTION content, hence gitignored — the
committed artifact is the generated student notebook only). This script:

  1. writes notebooks/instructor/nbNN_<slug>_instructor.ipynb (nbformat v4)
  2. executes it end-to-end with nbclient (kernel: repo .venv, cwd: repo root,
     timeout 300s/cell) — any raised error fails the build
  3. generates the student file via scripts/make_student.py logic
  4. runs scripts/validate_notebooks.py on the pair
  5. refreshes schedule.qmd badges (scripts/update_schedule_badges.py)

Milestone studio notebooks build the same way: `nbbuild.py ms04` reads
`_production_kit/nb_sources/ms04_<slug>.py`, writes the ms instructor/student
pair, and validates it with the reduced studio contract. Studio notebooks carry
no schedule badge, so the badge refresh runs only when a topic notebook (nbNN)
was built.

Usage: .venv/bin/python scripts/nbbuild.py nb01 [nb02 ...] [ms04 ...] [--no-exec]
"""
from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from notebooks_map import (  # noqa: E402
    NOTEBOOKS, MS_NOTEBOOKS, instructor_filename, ms_instructor_filename,
)

SOURCES = REPO / "_production_kit" / "nb_sources"

# D32/D33: every lecture opens with the same visible frame, injected at build
# time (topic notebooks only; nb01 orientation and the async module are
# exempt). D33: all seven moves run INSIDE the 50 minutes; below each
# lecture's ⏸ line is optional depth, never homework.
FRAME_MON = (
    "🗺️ **Today's frame (Monday, 9 / 22 / 12 / 7):** open with the 🧩 puzzle "
    "and 🔮 **Predict First** · investigate with 🛠️ **Run the Study** and "
    "your AI · verify with 🔍 **Read the Evidence** · drill 📝 **Practice** "
    "aloud and take ⚖️ **Make a Design Choice** · close in the room with "
    "🎯 **Take It to Your Project**, 🛡️ **Defend Your Decision**, and your "
    "📒 ledger row. All seven moves happen in class; 🏠-marked items and "
    "everything below the ⏸ line are optional depth.")
FRAME_WED = (
    "🗺️ **Today's frame (Wednesday, 7 / 23 / 12 / 8):** open with the 🧩 "
    "challenge, a spoken 📝 **Practice** retrieval drill, and 🔮 **Predict "
    "First** · attack the problem with 🛠️ **Run the Study**, 🔁 modifying "
    "the prompt and 🔬 interrogating what comes back · verify with 🔍 **Read "
    "the Evidence** · defend ⚖️ **Make a Design Choice** to your peers, AI "
    "closed at the 🧑‍⚖️ checkpoint · close with 🎯 **Take It to Your "
    "Project**, 🛡️ **Defend Your Decision**, and your 📒 ledger row. All "
    "seven moves happen in class; 🏠-marked items and everything below the "
    "⏸ line are optional depth.")
FRAME_ONE = (
    "🗺️ **The frame (50 min):** 🧩 puzzle → 🔮 **Predict First** · 🛠️ **Run "
    "the Study** with your AI · 🔍 **Read the Evidence** · 📝 **Practice** · "
    "⚖️ **Make a Design Choice** · 🎯 **Take It to Your Project** · "
    "🛡️ **Defend Your Decision** · 📒 ledger row. All seven moves happen in "
    "class; 🏠-marked items and everything below the ⏸ line are optional "
    "depth.")
FRAME_CONF = (
    "🗺️ **The frame (50 min, then the Expo):** in the room: 🧩 puzzle → "
    "🔮 **Predict First** · dress-rehearsal rounds · 🔍 **Read the "
    "Evidence** · 📝 **Practice** · ⚖️ **Make a Design Choice** · 🛡️ "
    "**Defend Your Decision** with your 📒 ledger row. 🎯 **Take It to Your "
    "Project** completes at the conference itself: capture, tally, reflect.")
FRAME_EXEMPT = {1, 14}   # nb01 orientation; nb14 async module
FRAME_SPECIAL = {13: FRAME_CONF}   # conference week: the path ends at the Expo

LECTURE_HEAD = re.compile(r"(?m)^#\s*Lecture\s+(\d)\s*$")

# The Student Research Lead fills the lecture notebook itself and submits it two
# days before leading; the plan cell is the one thing the brief above does not
# already give them. Injected at build time next to the frame, so all 25 brief
# locations stay identical and the gitignored sources stay free of it. nb01's
# briefs are the instructor-led Week-1 models and take no plan cell (FRAME_EXEMPT).
BRIEF_MARK = re.compile(r"(?m)^\s*###[^\n]*SRL Lead Brief")
LEAD_PLAN = (
    "### 🎤 My Lead Plan\n\n"
    "*If this lecture is your slot, fill this in, fill the rest of the notebook "
    "as a learner, and submit the whole notebook two days before you lead, by "
    "11:59 PM on the course platform. Your classmates can read it, the same way "
    "they read the brief above. If it is not your slot, read it to see how the "
    "session will run.*\n\n"
    "The frame, the puzzle, and the checkpoints above are fixed. **The staging "
    "is yours.** Five lines are enough; your ledger row below records the AI you "
    "used and how you checked it.\n\n"
    "**1. How I will stage the puzzle** *(my own words, my own example, or the "
    "seed puzzle sharpened):*\n\n\n"
    "**2. The one thing I am adding that the brief does not have:**\n\n\n"
    "**3. My commitment question, and how the room records it** *(the exact "
    "question everyone answers in writing before any AI tool opens):*\n\n\n"
    "**4. The decision I will close on, and the defense question I will put to "
    "one person:**\n\n\n"
    "**5. If my AI tool is slow or down, I will:**\n")

# D34: the ⏸ optional-depth region is NORMALIZED at build time. In every
# lecture segment the ⏸ cell body is standardized, and in a notebook's final
# lecture the close (Wrap-Up → Sources & Provenance → thank-you) is hoisted
# ABOVE the ⏸ line, so the optional region ends the notebook and the close is
# never formally optional. nb13 keeps its conference-path semantics; nb14 is
# async. Sources stay edit-canonical for content; placement is build machinery.
PAUSE_RE = re.compile(r"(?m)^###\s*⏸")
WRAP_RE = re.compile(r"(?m)^##\s*\d+\.\s*Wrap-?Up")
PAUSE_MID = (
    "---\n\n### ⏸ Optional depth from here\n\n"
    "**Today's lecture path is complete.** Anything between this line and the "
    "next lecture heading is optional depth: run it if you want to push the "
    "ideas further. Nothing below this line is required, and any 🏠-marked "
    "prompt above it is optional too.")
PAUSE_END = (
    "---\n\n### ⏸ Optional depth from here\n\n"
    "**Today's lecture path and the notebook's close are complete.** "
    "Everything below this line is optional depth: run it if you want to push "
    "the ideas further. Nothing here is required, and any 🏠-marked prompt "
    "above is optional too.")
NORMALIZE_EXEMPT = {13, 14}


def normalize_pause_regions(cells, nb_num):
    """Standardize each lecture's ⏸ cell and keep the notebook close above it."""
    if nb_num in NORMALIZE_EXEMPT:
        return cells
    out = list(cells)
    lect_idx = [i for i, (k, s) in enumerate(out)
                if k == "md" and LECTURE_HEAD.search(s)]
    bounds = ([(0, len(out))] if not lect_idx else
              [(s, lect_idx[j + 1] if j + 1 < len(lect_idx) else len(out))
               for j, s in enumerate(lect_idx)])
    for li in range(len(bounds) - 1, -1, -1):
        st, en = bounds[li]
        seg = out[st:en]
        p = next((i for i, (k, s) in enumerate(seg)
                  if k == "md" and PAUSE_RE.search(s)), None)
        if p is None:
            continue
        final = li == len(bounds) - 1
        w = next((i for i in range(p + 1, len(seg))
                  if seg[i][0] == "md" and WRAP_RE.search(seg[i][1])), None)
        if w is not None:
            tail, optional = seg[w:], seg[p:w]
            seg = seg[:p] + tail + optional
            p = len(seg) - len(optional)
        seg[p] = ("md", PAUSE_END if final else PAUSE_MID)
        out[st:en] = seg
    return out


# Every built notebook carries the EDR|AI wordmark inside its TITLE cell,
# right after the <hr> that separates the topic line from the course name
# (the MGMT474 launchpad placement). Injected at build time so the sources
# stay logo-free and the brand can change in one place.
LOGO_BLOCK = (
    "<center>\n"
    "<div>\n"
    '<img src="https://davi-moreira.github.io/'
    "2026F_evidence_driven_research_purdue_HONR464/book/images/"
    'edrai_logo.png" width="300"/>\n'
    "</div>\n"
    "</center>\n")


def inject_logo(source: str) -> str:
    """Place the wordmark after the title cell's first <hr>; no-op if present."""
    if "edrai_logo" in source or "<hr>" not in source:
        return source
    return source.replace("<hr>", "<hr>\n\n" + LOGO_BLOCK, 1)


def load_cells(slug: str):
    src = SOURCES / f"{slug}.py"
    if not src.exists():
        sys.exit(f"✗ source module missing: {src}")
    spec = importlib.util.spec_from_file_location(slug, src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.CELLS


def _frame_for(lecture_no: int, n_lectures: int, nb: int | None = None) -> str:
    if nb in FRAME_SPECIAL:
        return FRAME_SPECIAL[nb]
    if n_lectures == 1:
        return FRAME_ONE
    return FRAME_MON if lecture_no == 1 else FRAME_WED


def _write_instructor(cells, out: Path, frames_nb: int | None = None) -> Path:
    nb = nbformat.v4.new_notebook()
    nb.metadata = {
        "kernelspec": {"display_name": "Python 3", "language": "python",
                       "name": "python3"},
        "language_info": {"name": "python", "version": "3.11"},
        "colab": {"provenance": []},
    }
    n_lectures = sum(1 for k, src in cells if k == "md" and LECTURE_HEAD.search(src))
    for i, (kind, source) in enumerate(cells):
        if kind == "md":
            if i == 0:
                source = inject_logo(source)
            nb.cells.append(nbformat.v4.new_markdown_cell(source))
            m = LECTURE_HEAD.search(source)
            if m and frames_nb is not None and frames_nb not in FRAME_EXEMPT:
                nb.cells.append(nbformat.v4.new_markdown_cell(
                    _frame_for(int(m.group(1)), n_lectures, frames_nb)))
            if (BRIEF_MARK.search(source) and "### 🎤 My Lead Plan" not in source
                    and frames_nb is not None and frames_nb not in FRAME_EXEMPT):
                nb.cells.append(nbformat.v4.new_markdown_cell(LEAD_PLAN))
        elif kind == "code":
            nb.cells.append(nbformat.v4.new_code_cell(source))
        else:
            sys.exit(f"✗ unknown cell kind {kind!r}")
    nbformat.write(nb, out)
    print(f"✓ built {out.name} ({len(nb.cells)} cells)")
    return out


def build_instructor(n: int) -> Path:
    out = REPO / "notebooks" / "instructor" / instructor_filename(n)
    cells = normalize_pause_regions(load_cells(NOTEBOOKS[n][0]), n)
    return _write_instructor(cells, out, frames_nb=n)


def build_ms_instructor(n: int) -> Path:
    out = REPO / "notebooks" / "instructor" / ms_instructor_filename(n)
    return _write_instructor(load_cells(MS_NOTEBOOKS[n][0]), out)


def execute(path: Path) -> None:
    nb = nbformat.read(path, as_version=4)
    client = NotebookClient(nb, timeout=300, kernel_name="python3",
                            resources={"metadata": {"path": str(REPO)}})
    client.execute()
    nbformat.write(nb, path)
    n_out = sum(1 for c in nb.cells if c.cell_type == "code" and c.get("outputs"))
    print(f"✓ executed {path.name} — {n_out} code cells produced output")


def stamp_generation(instr: Path) -> None:
    """Record the canonical source's content hash in both generated notebooks.

    `validate_misconceptions.py --local` compares this stamp against the
    current source: a content change without a rebuild fails the gate. An
    mtime heuristic was defeatable by timestamp restoration (round-5 G-D);
    content hashes are not. The generator's own hash is recorded as
    provenance (not checked, so a tooling tweak does not stale every build).
    """
    import hashlib
    stem = instr.stem.replace("_instructor", "")
    src = SOURCES / f"{stem}.py"
    stamp = {
        "src_sha256": hashlib.sha256(src.read_bytes()).hexdigest(),
        "generator_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    student = REPO / "notebooks" / "student" / f"{stem}_student.ipynb"
    for path in (instr, student):
        nb = nbformat.read(path, as_version=4)
        nb.metadata["edrai_generation"] = stamp
        nbformat.write(nb, path)


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    do_exec = "--no-exec" not in sys.argv
    if not args:
        sys.exit("usage: nbbuild.py nbNN|msNN [...]")
    built_topic = False
    for a in args:
        is_ms = a.lower().startswith("ms")
        n = int(re.sub(r"\D", "", a))
        instr = build_ms_instructor(n) if is_ms else build_instructor(n)
        built_topic = built_topic or not is_ms
        if do_exec:
            execute(instr)
        subprocess.run([sys.executable, str(REPO / "scripts" / "make_student.py"),
                        str(instr)], check=True)
        stamp_generation(instr)
        tag = f"ms{n:02d}" if is_ms else f"nb{n:02d}"
        subprocess.run([sys.executable, str(REPO / "scripts" / "validate_notebooks.py"),
                        tag], check=True)
    # Studio (msNN) notebooks carry no schedule badge; refresh only for topics.
    if built_topic and "--no-badges" not in sys.argv:
        subprocess.run([sys.executable,
                        str(REPO / "scripts" / "update_schedule_badges.py")], check=True)
    # A5 misconception gate over the CANONICAL surfaces (round-4 G2): public CI
    # cannot see gitignored sources or instructor notebooks, so the gate runs
    # here — the point where canonical content moves. --no-numbers keeps the
    # seeded simulations out of the notebook-build path; chapter edits run the
    # full evaluator via CI and the pre-render checks.
    subprocess.run([sys.executable,
                    str(REPO / "scripts" / "validate_misconceptions.py"),
                    "--local", "--no-numbers"], check=True)


if __name__ == "__main__":
    main()
