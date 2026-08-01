#!/usr/bin/env python3
"""build_station_pointers.py — every lesson names the station it feeds.

Cold-pilot finding (A1): the practice grain was undiscoverable. A solo reader
met 39 lessons, each ending with "It is your turn", and nothing told them the
twelve stations existed or which one their work fed into. The stations looked
like a parallel book.

This inserts (and keeps in sync) one generated line at the top of each
lesson's "It is your turn" section:

    > **This work feeds [Station N: Title](...).** <one line on the checkpoint>

Managed between HTML markers so it is rewritten, never duplicated.

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
IYT_RE = re.compile(r"^## It is your turn\s*$", re.M)
BLOCK_RE = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n\n?", re.S)


def pointer(station: dict, n: int) -> str:
    rel = f"../stations/station{n:02d}-{station['id']}.qmd"
    return (f"{BEGIN}\n"
            f"> **This work feeds [Station {n}: {station['title']}]({rel}).**\n"
            f"> Keep what you write here; the station is where it joins the "
            f"other lessons' pieces into one artifact you can defend.\n"
            f"{END}\n\n")


def render_all() -> dict[Path, str]:
    require_lock()
    arch = load_architecture()
    stations = {s["id"]: s for s in arch["stations"]}
    out: dict[Path, str] = {}
    for lesson in active_lessons(arch):
        path = REPO / "book" / lesson["source"]
        text = path.read_text()
        st = stations[lesson["station"]]
        text = BLOCK_RE.sub("", text)
        m = IYT_RE.search(text)
        if not m:
            continue                      # lesson without an IYT section
        insert_at = m.end() + 1
        while insert_at < len(text) and text[insert_at] == "\n":
            insert_at += 1
        text = text[:insert_at] + pointer(st, st["rank"]) + text[insert_at:]
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
            print(f"✗ station pointers are STALE in {len(stale)} lesson(s): "
                  f"{', '.join(stale[:3])}… — run scripts/build_station_pointers.py")
            return 1
        print(f"✓ station pointers are fresh ({len(rendered)} lessons)")
        return 0
    print(f"✓ station pointers written into {len(rendered)} lessons")
    return 0


if __name__ == "__main__":
    sys.exit(main())
