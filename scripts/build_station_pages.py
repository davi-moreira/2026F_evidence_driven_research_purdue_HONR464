#!/usr/bin/env python3
"""build_station_pages.py — the 12 practice-station pages + workbooks (D35 §3).

Two grains: lessons are reading units, stations are PRACTICE units. This
generator writes one page per station into `book/stations/` and one workbook
notebook into `notebooks/book/stations/`, from:

  - planning/BOOK_ARCHITECTURE.yml — station identity, rank, checkpoint ids,
    and which lessons belong to the station (never restated by hand)
  - planning/BOOK_STATIONS.yml — the authored practice content

Checkpoints are VERSIONED, not locked passes (D35): every station page says so
and every workbook records a version with its reason.

    .venv/bin/python scripts/build_station_pages.py            # write
    .venv/bin/python scripts/build_station_pages.py --check    # CI: fresh?
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
from book_manifest import (active_lessons, load_architecture,  # noqa: E402
                           require_lock)

STATIONS_YML = REPO / "planning" / "BOOK_STATIONS.yml"
ASSESS_YML = REPO / "planning" / "BOOK_ASSESSMENTS.yml"
OUT_DIR = REPO / "book" / "stations"
NB_DIR = REPO / "notebooks" / "book" / "stations"
SITE = "https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464"
COLAB = ("https://colab.research.google.com/github/davi-moreira/"
         "2026F_evidence_driven_research_purdue_HONR464/blob/main/notebooks/book/stations")

RAILS = {
    "ethics": "Ethics, permissions, and data exposure",
    "evidence": "Evidence, provenance, and reproducibility",
    "ai": "AI activity, verification, and human decisions",
    "uncertainty": "Uncertainty, claim boundary, and revision history",
}

BANNER = ('::: {.callout-warning .review-pending title="Under development"}\n'
          "This station is part of a book in active development and has not yet\n"
          "been through the author's review. Content may change as the review\n"
          "advances.\n"
          ":::\n")


def rubric_md(entry: dict | None) -> str:
    """The AUTHORED rubric for this checkpoint (D35 §4 retires the
    auto-derived, first-sentence rubrics)."""
    if not entry:
        return ""
    rows = ["| # | Criterion | 0 | 1 | 2 |", "|---|---|---|---|---|"]
    for i, c in enumerate(entry["criteria"], 1):
        lv = c["levels"]
        rows.append(f"| {i} | {c['text']} | {lv[0]} | {lv[1]} | {lv[2]} |")
    total = 2 * len(entry["criteria"])
    out = ("## How this checkpoint is assessed\n\n"
           f"Each row scores **0**, **1**, or **2**. **{total} points total.**\n\n"
           + "\n".join(rows) + "\n")
    for gate in entry.get("gates", []):
        out += (f"\n::: {{.callout-important title=\"Blocking gate\"}}\n"
                f"{gate['text']} This is not scored and cannot be averaged "
                f"away.\n:::\n")
    return out


def station_page(st: dict, spec: dict, lessons: list[dict], n: int,
                 rubric: dict | None = None) -> str:
    cps = ", ".join(f"`{c['id']}`" for c in st["checkpoints"])
    reading = "\n".join(
        f"- [Ch. {l['display']} — {l['title']}]({SITE}/book/{l['url_path']})"
        for l in lessons)
    steps = "\n".join(f"{i}. {s}" for i, s in enumerate(spec["steps"], 1))
    rails = "\n".join(f"- **{RAILS[k]}.** {v}" for k, v in spec["rails"].items()
                      if k in RAILS)
    slug = st["id"]
    route_block = (f"## Choosing your pathway\n\n{spec['route_guide']}\n"
                   if spec.get("route_guide") else "")
    rubric_block = rubric_md(rubric)
    return f"""---
title: "Station {n}: {st['title']}"
---

{BANNER}
[![](https://colab.research.google.com/assets/colab-badge.svg){{fig-alt="Open In Colab"}}]({COLAB}/station{n:02d}_{slug.replace('-', '_')}.ipynb){{target="_blank"}}

> **What you can defend when you leave.** {spec['purpose']}

## What this station produces

{spec['produces']}

This is a **versioned checkpoint**, not a pass. You date it, number it, and
attach the reason for the version. When later evidence changes it, you write
the next version rather than editing the last one, because the sequence of
changes is itself part of your research record.

{route_block}## The reading behind it

{reading}

Read these before you work the station. The station is where you do the thing
the lessons describe, on your own project.

## The practice

{steps}

## The four rails, here

Four concerns cross every station in this book. At this station they take
these specific forms.

{rails}

## What sends you back

{spec['revisit']}

{rubric_block}

## Your workbook

Open the workbook with the badge above. It walks these steps with a cell for
each one, ends by writing your checkpoint version with its reason, and adds
the rows this station contributes to your AI Research Ledger and your Research
Dossier.
"""


def workbook(st: dict, spec: dict, n: int, rubric: dict | None = None) -> dict:
    def md(i, s):
        return {"cell_type": "markdown", "id": f"m{i:03d}", "metadata": {},
                "source": s.splitlines(keepends=True)}
    cells = [md(0, f"# Station {n}: {st['title']}\n\n"
                   f"**What you can defend when you leave.** {spec['purpose']}\n\n"
                   f"**This station produces.** {spec['produces']}\n\n"
                   f"A checkpoint is a *version*, not a pass. Date it, number it, "
                   f"and write why this version exists.\n")]
    i = 1
    for k, step in enumerate(spec["steps"], 1):
        cells.append(md(i, f"## Step {k}\n\n{step}\n")); i += 1
        cells.append(md(i, f"✍️ **Your work for step {k}.** Double-click this "
                           f"cell and write your answer here.\n")); i += 1
    cells.append({"cell_type": "code", "id": "c001", "metadata": {},
                  "execution_count": None, "outputs": [],
                  "source": ["# Scratch space — any code this station's steps need.\n"]})
    cps = ", ".join(c["id"] for c in st["checkpoints"])
    cells.append(md(i, f"## Write your checkpoint version\n\n"
                       f"Checkpoint: `{cps}`\n\n"
                       f"Record: the version number, today's date, what this "
                       f"version says, and **why it differs from the previous "
                       f"one**. A first version says why you are starting here.\n"))
    i += 1
    cells.append(md(i, "✍️ **Checkpoint version.** Double-click and write it here.\n"))
    i += 1
    if rubric:
        cells.append(md(i, rubric_md(rubric))); i += 1
    cells.append(md(i, "## Before you leave\n\nAdd this station's rows to your "
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
    titles = {}
    for l in lessons:
        src = REPO / "book" / l["source"]
        import re
        m = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', src.read_text(), re.M)
        titles[l["id"]] = m.group(1) if m else l["id"]
        l["title"] = titles[l["id"]]
    out: dict[Path, str] = {}
    for st in sorted(arch["stations"], key=lambda s: s["rank"]):
        if st["id"] not in spec_by_id:
            sys.exit(f"✗ station {st['id']} has no entry in BOOK_STATIONS.yml")
        spec = spec_by_id[st["id"]]
        n = st["rank"]
        mine = [l for l in lessons if l["station"] == st["id"]]
        slug = st["id"].replace("-", "_")
        rb = rubric_by_station.get(st["id"])
        out[OUT_DIR / f"station{n:02d}-{st['id']}.qmd"] = station_page(
            st, spec, mine, n, rb)
        out[NB_DIR / f"station{n:02d}_{slug}.ipynb"] = json.dumps(
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
        print(f"✓ station pages and workbooks are fresh ({len(rendered) // 2} stations)")
        return 0
    print(f"✓ {len(rendered) // 2} station pages + workbooks generated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
