#!/usr/bin/env python3
"""build_milestone_anchors.py — milestone Book Anchors as GENERATED projections.

Round-9 N1's remediation: "Generate both the submission row and the entire
Book Anchor list from lesson IDs." Until now both surfaces were hand-edited,
so they drifted from the crosswalk (and from each other) whenever an anchor
moved — and Phase-3 lesson insertion would silently invalidate every display
number in every brief.

This script rewrites, in each `_research_project/2026Fall/milestone_NN_*.md`:

  1. the EDR|AI submission-table row's chapter list, and
  2. the `- Ch. N — [title](url) · [companion notebook](url)` bullet list
     inside the "## The Book Anchor" section,

from COURSE_BOOK_CROSSWALK.yml home anchors + BOOK_ARCHITECTURE.yml identity
(display numbers derived from rank; links from url_path and companion).
Everything else in the brief is left byte-for-byte alone.

    .venv/bin/python scripts/build_milestone_anchors.py            # write
    .venv/bin/python scripts/build_milestone_anchors.py --check    # CI: fresh?
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
from book_manifest import (active_lessons, load_crosswalk,  # noqa: E402
                           require_lock)

BRIEFS = REPO / "_research_project" / "2026Fall"
SITE = "https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464"
COLAB = ("https://colab.research.google.com/github/davi-moreira/"
         "2026F_evidence_driven_research_purdue_HONR464/blob/main/notebooks/book")


def anchors_by_milestone() -> dict[str, list[dict]]:
    lessons = {l["id"]: l for l in active_lessons()}
    out: dict[str, list[dict]] = {}
    for r in load_crosswalk()["rows"]:
        if not r.get("milestone"):          # D54: teaching-only rows (Week 16)
            continue
        picked = [lessons[a["lesson"]] for a in r.get("assignments", [])
                  if a.get("home_anchor") and a["lesson"] in lessons]
        out[r["milestone"]] = sorted(picked, key=lambda l: l["display"])
    return out


def title_of(lesson: dict) -> str:
    src = REPO / "book" / lesson["source"]
    m = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', src.read_text(), re.M)
    return m.group(1) if m else lesson.get("title_en", lesson["id"])


BRIDGE_BEGIN = "<!-- book-milestone-bridge:begin -->"
BRIDGE_END = "<!-- book-milestone-bridge:end -->"
BRIDGE_RE = re.compile(re.escape(BRIDGE_BEGIN) + r".*?" + re.escape(BRIDGE_END),
                       re.S)


def station_info() -> dict[str, dict]:
    """station id -> {rank, milestone_title} from the two manifests."""
    import yaml
    arch = yaml.safe_load((REPO / "planning" / "BOOK_ARCHITECTURE.yml").read_text())
    spec = yaml.safe_load((REPO / "planning" / "BOOK_STATIONS.yml").read_text())
    titles = {s["id"]: s.get("milestone_title", s["id"]) for s in spec["stations"]}
    return {s["id"]: {"rank": s["rank"], "title": titles.get(s["id"], s["id"])}
            for s in arch["stations"]}


def bridge_block(row: dict, stations: dict[str, dict]) -> str:
    """The naming-bridge projection for one course milestone (D40/D41; D49 mapping).

    Line discipline: no line may start with '- Ch. ' and no line may contain
    the string 'EDR' — both are anchor-surface parse tokens in
    validate_book_architecture's brief checker.
    """
    mi = row["milestone"]
    lines = [BRIDGE_BEGIN,
             f"> **Book Milestone bridge** — course milestone **{mi}**."]
    for b in row.get("book_milestones", []):
        st = stations[b["station"]]
        page = (f"{SITE}/book/studios/"
                f"milestone{st['rank']:02d}-{b['station']}.html#milestone")
        lines.append(f"> This submission presents **Book Milestone "
                     f"{st['rank']} — {st['title']}** ({b['version_label']}): "
                     f"work from its [milestone page]({page}).")
        if b.get("relationship") == "revisit":
            lines.append("> It is a *revisit*: the next version of an "
                         "artifact whose first version already exists.")
    if row.get("route_selection"):
        lines.append("> **Route-conditional reading:** complete YOUR declared "
                     "route's chapter plus the instructor-assigned contrast; "
                     "the other route chapters are jigsaw material, and the "
                     "hybrid/complex overlay applies only when your design "
                     "has stages.")
    for sg in row.get("supporting_gate_milestones", []):
        st = stations[sg["station"]]
        lines.append(f"> **Gate work (no artifact presented):** Book "
                     f"Milestone {st['rank']} — {st['title']} "
                     f"({sg['use'].replace('-', ' ')}).")
    lines.append(BRIDGE_END)
    return "\n".join(lines)


def apply_bridge(text: str, block: str) -> str:
    if BRIDGE_RE.search(text):
        return BRIDGE_RE.sub(block, text)
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("# "):
            return "\n".join(lines[:i + 1] + ["", block] + lines[i + 1:])
    return text + "\n\n" + block + "\n"


def render(text: str, picked: list[dict]) -> str:
    if not picked:
        return text
    chs = ", ".join(f"ch. {l['display']}" for l in picked)
    # 1. the submission-table row
    text = re.sub(r'(\*\*EDR\\\|AI "It is your turn" — )ch\. [^*]+(\*\*)',
                  lambda m: m.group(1) + chs + m.group(2), text, count=1)
    # 2. the bullet list (contiguous block of "- Ch. " lines)
    bullets = [
        f"- Ch. {l['display']} — [{title_of(l)}]({SITE}/book/{l['url_path']})"
        f" · [companion notebook]({COLAB}/{l['companion']})"
        for l in picked]
    lines = text.split("\n")
    idx = [i for i, l in enumerate(lines) if l.startswith("- Ch. ")]
    if idx:
        lines = lines[:idx[0]] + bullets + lines[idx[-1] + 1:]
    return "\n".join(lines)


def main() -> int:
    check = "--check" in sys.argv
    require_lock()
    anchors = anchors_by_milestone()
    stations = station_info()
    rows = {r["milestone"]: r for r in load_crosswalk()["rows"]
            if r.get("milestone")}
    stale, written = [], 0
    for brief in sorted(BRIEFS.glob("milestone_*.md")):
        m = re.match(r"milestone_(\d+)_", brief.name)
        if not m:
            continue
        mi = f"M{int(m.group(1))}"
        picked = anchors.get(mi, [])
        src = brief.read_text()
        if picked and check and not re.search(r"^- Ch\. ", src, re.M):
            stale.append(f"{brief.name} (bullet surface missing)")
            continue
        new = render(src, picked)
        if mi in rows:
            new = apply_bridge(new, bridge_block(rows[mi], stations))
        if new == src:
            continue
        if check:
            stale.append(brief.name)
        else:
            brief.write_text(new)
            written += 1
    if check:
        if stale:
            print(f"✗ milestone anchors are STALE in {len(stale)} brief(s): "
                  f"{', '.join(stale)} — run scripts/build_milestone_anchors.py")
            return 1
        print("✓ milestone Book Anchors are fresh against the crosswalk")
        return 0
    print(f"✓ milestone Book Anchors regenerated — {written} brief(s) updated, "
          f"{len(anchors)} milestones projected")
    return 0


if __name__ == "__main__":
    sys.exit(main())
