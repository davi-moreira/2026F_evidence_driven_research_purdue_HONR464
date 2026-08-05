#!/usr/bin/env python3
"""build_station_pages.py — 12 Studio openers + 12 Milestone chapters + workbooks.

D38 made the twelve Studios the book's twelve parts. D40 splits each studio
into TWO generated pages: the OPENER (before the lessons) anticipates the
studio's milestone — the goal, the reasoning, how it connects to the whole
book — and lists the lessons with the piece each one hands the milestone;
the MILESTONE CHAPTER (after the lessons, last in the part) carries the
working details — the practice steps, the versioned record, the four rails,
the rubric, and the workbook. Reader-facing vocabulary is "Studio" and
"Milestone"; the machine layer keeps the immutable station ids and
checkpoint ids. Sources:

  - planning/BOOK_ARCHITECTURE.yml — station identity, rank, checkpoint ids,
    and which lessons belong to the studio (never restated by hand)
  - planning/BOOK_STATIONS.yml — the authored practice content, including
    the D40 milestone fields (milestone_title, milestone_reason,
    hands_forward, contributions)
  - planning/BOOK_ASSESSMENTS.yml — the authored rubric per checkpoint

Old `stations/stationNN-*.html` URLs stay alive through opener aliases, and
the historical `#checkpoint` anchor lands on the opener's milestone
anticipation. Milestones are VERSIONED, not locked passes (D35): every
milestone page says so and every workbook records a version with its reason.

    .venv/bin/python scripts/build_station_pages.py            # write
    .venv/bin/python scripts/build_station_pages.py --check    # CI: fresh?
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
from book_manifest import (active_lessons, load_architecture,  # noqa: E402
                           require_lock)

STATIONS_YML = REPO / "planning" / "BOOK_STATIONS.yml"
ASSESS_YML = REPO / "planning" / "BOOK_ASSESSMENTS.yml"
OUT_DIR = REPO / "book" / "studios"
NB_DIR = REPO / "notebooks" / "book" / "studios"
SITE = "https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464"
COLAB = ("https://colab.research.google.com/github/davi-moreira/"
         "2026F_evidence_driven_research_purdue_HONR464/blob/main/notebooks/book/studios")

# D45: the S1/S2 flip moved studio ranks, and rank lives in the page
# filenames — these stations' pages once lived at other rank-numbered URLs.
# Openers and milestone chapters emit aliases for every legacy rank.
LEGACY_RANKS = {"govern-the-work": [1], "frame-the-inquiry": [2]}

RAILS = {
    "ethics": "Ethics, permissions, and data exposure",
    "evidence": "Evidence, provenance, and reproducibility",
    "ai": "AI activity, verification, and human decisions",
    "uncertainty": "Uncertainty, claim boundary, and revision history",
}

def banner(noun: str) -> str:
    return ('::: {.callout-warning .review-pending title="Under development"}\n'
            f"This {noun} is part of a book in active development and has not\n"
            "yet been through the author's review. Content may change as the\n"
            "review advances.\n"
            ":::\n")


def milestone_rel(st: dict) -> str:
    return f"milestone{st['rank']:02d}-{st['id']}.qmd"


def opener_rel(st: dict) -> str:
    return f"studio{st['rank']:02d}-{st['id']}.qmd"


def rubric_md(entry: dict | None) -> str:
    """The AUTHORED rubric for this milestone (D35 §4 retires the
    auto-derived, first-sentence rubrics)."""
    if not entry:
        return ""
    rows = ["| # | Criterion | 0 | 1 | 2 |", "|---|---|---|---|---|"]
    for i, c in enumerate(entry["criteria"], 1):
        lv = c["levels"]
        rows.append(f"| {i} | {c['text']} | {lv[0]} | {lv[1]} | {lv[2]} |")
    total = 2 * len(entry["criteria"])
    out = ("## How this milestone is assessed\n\n"
           f"Each row scores **0**, **1**, or **2**. **{total} points total.**\n\n"
           + "\n".join(rows) + "\n")
    for gate in entry.get("gates", []):
        out += (f"\n::: {{.callout-important title=\"Blocking gate\"}}\n"
                f"{gate['text']} This is not scored and cannot be averaged "
                f"away.\n:::\n")
    return out


def contribution_lines(spec: dict, lessons: list[dict]) -> str:
    lines = []
    for l in lessons:
        c = spec["contributions"][l["id"]].rstrip(".")
        lines.append(f"- [Lesson {l['display']} — {l['title']}]"
                     f"({SITE}/book/{l['url_path']}): {c}.")
    return "\n".join(lines)


def bring_block(spec: dict, lessons: list[dict], prev_spec: dict | None = None,
                prev_n: int | None = None) -> str:
    """The milestone's "What you bring" checklist, role-aware: core pieces
    are prerequisites; branch/optional pieces bind only when their condition
    is the reader's (skimming a non-matching pathway or overlay is using the
    book correctly — the lesson pointers say so)."""
    core = [l for l in lessons if l.get("role", "core") == "core"]
    cond = [l for l in lessons if l.get("role", "core") != "core"]
    out = []
    if prev_spec is not None:
        out.append(f"You also carry forward the last milestone's artifact: "
                   f"**Milestone {prev_n}: {prev_spec['milestone_title']}**. "
                   f"This one builds on it, and the chain assumes it is "
                   f"versioned and filed.")
    if core:
        out.append("Check you are carrying each of these before you start. "
                   "If one is missing, go back and work that lesson's **It "
                   "is your turn** first; the practice below assumes it.")
        out.append(contribution_lines(spec, core))
    if cond:
        out.append("These pieces are conditional. Bring each one when its "
                   "condition is yours; when it is not, the lesson's own "
                   "drill or a plain skip is the right call, and the "
                   "milestone does not require the piece.")
        out.append(contribution_lines(spec, cond))
    if spec.get("bring_note"):
        out.append(spec["bring_note"].strip())
    return "\n\n".join(out)


def chain_paragraph(stations: list[dict], specs: dict, idx: int) -> str:
    st = stations[idx]
    spec = specs[st["id"]]
    last = stations[-1]
    parts = []
    if idx == 0:
        parts.append("This is the first of the book's twelve milestones.")
    else:
        prev = stations[idx - 1]
        pspec = specs[prev["id"]]
        parts.append(f"You arrived carrying [Milestone {prev['rank']}: "
                     f"{pspec['milestone_title']}]({milestone_rel(prev)}).")
    parts.append(spec["hands_forward"].strip())
    if idx < len(stations) - 1:
        lspec = specs[last["id"]]
        parts.append(f"The chain ends at [Milestone {last['rank']}: "
                     f"{lspec['milestone_title']}]({milestone_rel(last)}), "
                     "where you decide whether your finished research "
                     "artifact leaves your hands.")
    return " ".join(parts)


def opening_block(spec: dict) -> str:
    """D43: the human-only opening move, before any tool and before the
    milestone anticipation."""
    if not spec.get("opening_move"):
        return ""
    return (f"## Start without a tool {{#opening-move}}\n\n"
            f"{spec['opening_move'].strip()}\n\n")


def opener_page(st: dict, spec: dict, lessons: list[dict], n: int) -> str:
    rails_names = " · ".join(RAILS[k] for k in ("ethics", "evidence"))
    slug = st["id"]
    route_block = (f"## Choosing your pathway\n\n{spec['route_guide']}\n\n"
                   if spec.get("route_guide") else "")
    genre_block = (f"## Choosing your format\n\n{spec['genre_guide']}\n\n"
                   if spec.get("genre_guide") else "")
    acq_block = (f"## Before you can work this studio\n\n"
                 f"{spec['acquisition_note']}\n\n"
                 if spec.get("acquisition_note") else "")
    legacy = "".join(f"\n  - /studios/studio{r:02d}-{slug}.html"
                     f"\n  - /stations/station{r:02d}-{slug}.html"
                     for r in LEGACY_RANKS.get(slug, []))
    return f"""---
title: "Studio {n}: {st['title']}"
aliases:
  - /stations/station{n:02d}-{slug}.html{legacy}
---

{banner("studio")}
> **What you can defend when you leave.** {spec['purpose']}

{opening_block(spec)}## The milestone ahead {{#checkpoint}}

{spec['milestone_reason'].strip()}

This studio closes with **[Milestone {n}: {spec['milestone_title']}]({milestone_rel(st)})**, a short chapter of its own after the lessons. **What it asks you to produce.** {spec['produces'].strip()}

{spec['hands_forward'].strip()} The milestone chapter keeps the working details: the practice steps, the versioned record, and how the artifact is assessed.

{route_block}{genre_block}{acq_block}## The lessons in this studio

Read them in order, working each lesson's **It is your turn** as you go. Each one builds a piece of Milestone {n}; beside each lesson is the piece it hands you.

{contribution_lines(spec, lessons)}

When the last lesson closes, the milestone chapter is next. Nothing you write in a lesson is busywork: every piece above is on the milestone's checklist.
"""


def milestone_page(st: dict, spec: dict, lessons: list[dict], n: int,
                   stations: list[dict], specs: dict, idx: int,
                   rubric: dict | None = None) -> str:
    steps = "\n".join(f"{i}. {s}" for i, s in enumerate(spec["steps"], 1))
    rails = "\n".join(f"- **{RAILS[k]}.** {v}" for k, v in spec["rails"].items()
                      if k in RAILS)
    slug = st["id"]
    rubric_block = rubric_md(rubric)
    genre_block = (f"## Choosing your format\n\n{spec['genre_guide']}\n\n"
                   if spec.get("genre_guide") else "")
    legacy = "".join(f"\n  - /studios/milestone{r:02d}-{slug}.html"
                     for r in LEGACY_RANKS.get(slug, []))
    front = (f"---\naliases:{legacy}\n---\n\n" if legacy else "")
    return f"""{front}# Milestone {n}: {spec['milestone_title']} {{.unnumbered}}

{banner("milestone chapter")}
[![](https://colab.research.google.com/assets/colab-badge.svg){{fig-alt="Open In Colab"}}]({COLAB}/studio{n:02d}_{slug.replace('-', '_')}.ipynb){{target="_blank"}}

**This chapter closes [Studio {n}: {st['title']}]({opener_rel(st)}).** Its lessons each ended at **It is your turn**; what you wrote there arrives here as working material, and this is where the pieces become one artifact you can defend.

**What this milestone produces.** {spec['produces'].strip()}

## What you bring

{bring_block(spec, lessons, specs[stations[idx - 1]["id"]] if idx else None, stations[idx - 1]["rank"] if idx else None)}

{genre_block}## The practice {{#milestone}}

{steps}

## A version, not a pass

Your milestone artifact is a dated, numbered **version** with the reason for the version attached. When later evidence changes it, you write the next version rather than editing the last one, because the sequence of changes is itself part of your research record.

## The four rails, here

Four concerns cross every studio in this book. At this milestone they take these specific forms.

{rails}

## Where this milestone sits

{chain_paragraph(stations, specs, idx)}

## What sends you back

{spec['revisit']}

{rubric_block}

## Your workbook

Open the workbook with the badge above. It walks these steps with a cell for
each one, ends by writing your milestone version with its reason, and adds
the rows this studio contributes to your AI Research Ledger and your Research
Dossier.
"""


def workbook(st: dict, spec: dict, n: int, rubric: dict | None = None) -> dict:
    def md(i, s):
        return {"cell_type": "markdown", "id": f"m{i:03d}", "metadata": {},
                "source": s.splitlines(keepends=True)}
    cells = [md(0, f"# Milestone {n}: {spec['milestone_title']}\n\n"
                   f"The milestone chapter of **Studio {n}: {st['title']}**.\n\n"
                   f"**What you can defend when you leave.** {spec['purpose']}\n\n"
                   f"**What this milestone produces.** {spec['produces']}\n\n"
                   f"A milestone is a *version*, not a pass. Date it, number it, "
                   f"and write why this version exists.\n")]
    i = 1
    if spec.get("opening_move"):
        cells.append(md(i, f"## Start without a tool\n\n"
                          f"{spec['opening_move'].strip()}\n"))
        i += 1
        cells.append(md(i, "✍️ **Your opening move.** Double-click this cell "
                          "and write the four lines here, before any other "
                          "cell in this workbook:\n\n"
                          "1. What you genuinely want to understand:\n"
                          "2. Why an answer would matter, and to whom:\n"
                          "3. Your starting belief (not a claim):\n"
                          "4. The evidence that would revise it:\n"))
        i += 1
    if spec.get("genre_guide"):
        cells.append(md(i, f"## Choosing your format\n\n{spec['genre_guide']}\n"))
        i += 1
    kit = spec.get("practice_kit")
    if kit:
        cells.append(md(i, f"## A worked example\n\n{kit['worked_example'].strip()}\n"))
        i += 1
        cells.append(md(i, f"## Now you, half the way\n\n{kit['faded_task'].strip()}\n"))
        i += 1
        cells.append(md(i, "✍️ **Your finish of the faded task.** Double-click "
                          "and complete it here.\n"))
        i += 1
        starter = kit["starter"].strip()
        if "```python" in starter:
            intro, rest = starter.split("```python", 1)
            code, _, tail = rest.partition("```")
            cells.append(md(i, f"## Your starter\n\n{intro.strip()}\n"))
            i += 1
            cells.append({"cell_type": "code", "id": f"k{i:03d}",
                          "metadata": {}, "execution_count": None,
                          "outputs": [],
                          "source": code.strip("\n").splitlines(keepends=True)})
            i += 1
            if tail.strip():
                cells.append(md(i, tail.strip() + "\n")); i += 1
        else:
            cells.append(md(i, f"## Your starter\n\n{starter}\n"))
            i += 1
    for k, step in enumerate(spec["steps"], 1):
        cells.append(md(i, f"## Step {k}\n\n{step}\n")); i += 1
        cells.append(md(i, f"✍️ **Your work for step {k}.** Double-click this "
                           f"cell and write your answer here.\n")); i += 1
    cells.append({"cell_type": "code", "id": "c001", "metadata": {},
                  "execution_count": None, "outputs": [],
                  "source": ["# Scratch space — any code this milestone's steps need.\n"]})
    if kit:
        cells.append(md(i, f"## Check yourself\n\n{kit['verification'].strip()}\n"))
        i += 1
    cps = ", ".join(c["id"] for c in st["checkpoints"])
    cells.append(md(i, f"## Write your milestone version\n\n"
                       f"Milestone record: `{cps}`\n\n"
                       f"Record: the version number, today's date, what this "
                       f"version says, and **why it differs from the previous "
                       f"one**. A first version says why you are starting here.\n"))
    i += 1
    cells.append(md(i, "✍️ **Milestone version.** Double-click and write it here.\n"))
    i += 1
    if rubric:
        cells.append(md(i, rubric_md(rubric))); i += 1
    cells.append(md(i, "## Before you leave\n\nAdd this milestone's rows to your "
                      "**AI Research Ledger** — task, tool, prompt, output "
                      "summary, decision, verification method, remaining "
                      "concern, and you as the responsible researcher — and "
                      "file the artifact above in your **Research Dossier**.\n"))
    return {"cells": cells, "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python",
                       "name": "python3"},
        "language_info": {"name": "python"}},
        "nbformat": 4, "nbformat_minor": 5}


def render_all() -> dict[Path, str]:
    require_lock()
    arch = load_architecture()
    spec_by_id = {s["id"]: s for s in yaml.safe_load(
        STATIONS_YML.read_text())["stations"]}
    rubric_by_station = {r["station"]: r for r in
                         (yaml.safe_load(ASSESS_YML.read_text()).get("stations") or [])}
    lessons = active_lessons(arch)
    for l in lessons:
        src = REPO / "book" / l["source"]
        m = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', src.read_text(), re.M)
        l["title"] = m.group(1) if m else l["id"]
    stations = sorted(arch["stations"], key=lambda s: s["rank"])
    out: dict[Path, str] = {}
    for idx, st in enumerate(stations):
        if st["id"] not in spec_by_id:
            sys.exit(f"✗ station {st['id']} has no entry in BOOK_STATIONS.yml")
        spec = spec_by_id[st["id"]]
        n = st["rank"]
        mine = [l for l in lessons if l["station"] == st["id"]]
        missing = [l["id"] for l in mine if l["id"] not in
                   (spec.get("contributions") or {})]
        if missing:
            sys.exit(f"✗ station {st['id']}: no authored `contributions` "
                     f"entry for lesson(s) {', '.join(missing)}")
        slug = st["id"].replace("-", "_")
        rb = rubric_by_station.get(st["id"])
        out[OUT_DIR / opener_rel(st)] = opener_page(st, spec, mine, n)
        out[OUT_DIR / milestone_rel(st)] = milestone_page(
            st, spec, mine, n, stations, spec_by_id, idx, rb)
        out[NB_DIR / f"studio{n:02d}_{slug}.ipynb"] = json.dumps(
            workbook(st, spec, n, rb), ensure_ascii=False, indent=1) + "\n"
    return out


def main() -> int:
    check = "--check" in sys.argv
    rendered = render_all()
    stale = []
    for path, content in rendered.items():
        if not path.exists() or path.read_text() != content:
            if check:
                stale.append(path.relative_to(REPO).as_posix())
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content)
    if check:
        if stale:
            print(f"✗ station pages are STALE ({len(stale)}): "
                  f"{', '.join(stale[:4])}… — run scripts/build_station_pages.py")
            return 1
        print(f"✓ studio openers, milestone chapters, and workbooks are fresh "
              f"({len(rendered) // 3} studios)")
        return 0
    print(f"✓ {len(rendered) // 3} studio openers + milestone chapters + "
          f"workbooks generated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
