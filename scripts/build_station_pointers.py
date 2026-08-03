#!/usr/bin/env python3
"""build_station_pointers.py — every lesson names the studio it works inside.

Cold-pilot finding (A1): the practice grain was undiscoverable. D38 then made
the twelve Studios the book's parts, so each lesson now sits INSIDE its
studio. This keeps two generated blocks in sync across the 39 lessons:

  1. At the top of "It is your turn": a role-aware pointer —
       core     -> "You are working inside Studio N"
       branch   -> the same, plus its pathway/genre and the skim permission
       optional -> the same, plus "work it when your project needs it"
  2. At the end of the studio's LAST lesson: the checkpoint return —
     back to the studio page's `#checkpoint` anchor to produce the artifact.

Managed between HTML markers so they are rewritten, never duplicated. (The
marker strings keep the historical "station" token — they are machine-layer,
invisible to readers, and changing them would churn 39 files for nothing.)

    .venv/bin/python scripts/build_station_pointers.py            # write
    .venv/bin/python scripts/build_station_pointers.py --check    # CI: fresh?
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
from book_manifest import active_lessons, load_architecture, require_lock  # noqa: E402

BEGIN = "<!-- station-pointer:begin -->"
END = "<!-- station-pointer:end -->"
CBEGIN = "<!-- studio-continue:begin -->"
CEND = "<!-- studio-continue:end -->"
IYT_RE = re.compile(r"^## It is your turn\s*$", re.M)
BLOCK_RE = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n\n?", re.S)
CBLOCK_RE = re.compile(r"\n*" + re.escape(CBEGIN) + r".*?" + re.escape(CEND) + r"\n?",
                       re.S)

ROUTE_WORDS = {
    "observational-descriptive": "observational-descriptive",
    "observational-causal": "observational-causal",
    "experimental-descriptive": "experimental-descriptive",
    "experimental-causal": "experimental-causal",
    "prediction": "prediction",
}


def pointer(lesson: dict, station: dict, n: int) -> str:
    rel = f"../studios/studio{n:02d}-{station['id']}.qmd"
    head = f"> **You are working inside [Studio {n}: {station['title']}]({rel}).**"
    if lesson.get("role") == "branch" and lesson.get("route"):
        tail = (f"> This lesson serves the **{ROUTE_WORDS[lesson['route']]}**\n"
                f"> pathway. If your declared pathway is different, skim it and\n"
                f"> work the lesson that matches; the studio page routes you.")
    elif lesson.get("role") == "branch" and lesson.get("genre"):
        tail = (f"> This lesson adapts your work to the **{lesson['genre']}**\n"
                f"> format. Work the format your venue actually asks for; the\n"
                f"> studio page routes you.")
    elif lesson.get("role") == "optional":
        tail = ("> This lesson is an optional overlay: work it when your\n"
                "> project needs it, and skip it without guilt when it does not.")
    else:
        tail = ("> Keep what you write here; the studio is where it joins the\n"
                "> other lessons' pieces into one artifact you can defend.")
    return f"{BEGIN}\n{head}\n{tail}\n{END}\n\n"


def continue_block(station: dict, n: int) -> str:
    rel = f"../studios/studio{n:02d}-{station['id']}.qmd"
    return (f"\n\n{CBEGIN}\n"
            f"> **Checkpoint.** This was the last lesson of Studio {n}. Return\n"
            f"> to [the studio's practice]({rel}#checkpoint) and produce its\n"
            f"> versioned artifact before you move on.\n"
            f"{CEND}\n")


def render_all() -> dict[Path, str]:
    require_lock()
    arch = load_architecture()
    stations = {s["id"]: s for s in arch["stations"]}
    lessons = active_lessons(arch)
    last_in_station = {}
    for l in lessons:                       # rank order -> last one wins
        last_in_station[l["station"]] = l["id"]
    out: dict[Path, str] = {}
    for lesson in lessons:
        path = REPO / "book" / lesson["source"]
        text = path.read_text()
        st = stations[lesson["station"]]
        n = st["rank"]
        text = BLOCK_RE.sub("", text)
        text = CBLOCK_RE.sub("", text)
        m = IYT_RE.search(text)
        if not m:
            continue                      # lesson without an IYT section
        insert_at = m.end() + 1
        while insert_at < len(text) and text[insert_at] == "\n":
            insert_at += 1
        text = (text[:insert_at] + pointer(lesson, st, n) + text[insert_at:])
        if last_in_station[lesson["station"]] == lesson["id"]:
            text = text.rstrip("\n") + continue_block(st, n)
        out[path] = text
    return out


def main() -> int:
    check = "--check" in sys.argv
    rendered = render_all()
    stale = []
    for path, content in rendered.items():
        if path.read_text() != content:
            if check:
                stale.append(path.relative_to(REPO).as_posix())
            else:
                path.write_text(content)
    if check:
        if stale:
            print(f"✗ studio pointers are STALE in {len(stale)} lesson(s): "
                  f"{', '.join(stale[:3])}… — run scripts/build_station_pointers.py")
            return 1
        print(f"✓ studio pointers are fresh ({len(rendered)} lessons)")
        return 0
    print(f"✓ studio pointers written into {len(rendered)} lessons")
    return 0


if __name__ == "__main__":
    sys.exit(main())
