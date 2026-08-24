#!/usr/bin/env python3
"""build_brightspace_schedule.py — the paste-ready Schedule for Brightspace.

Brightspace's description fields cap at 65,535 characters "including any hidden
formatting characters". The rendered course page does not fit that field, and it
would not work there even if it did:

  * it carries ~18 KB of Quarto chrome (head, navbar, sidebar, search, the
    after-body script) that a description field has no use for;
  * its links are RELATIVE (`book/studios/...`), so every one of them 404s once
    the markup lives on brightspace.purdue.edu;
  * its table CSS lives in `styles.css`, which does not travel with a paste, so
    the eight columns collapse;
  * its new-tab behaviour is set by a `<script>`, and Brightspace strips scripts.

So this builds a SEPARATE edition for that field: the schedule table and its
notes, nothing else, with absolute URLs, the table CSS inlined, `target="_blank"`
back on every link as a real attribute, and inter-tag whitespace collapsed.

The rendered page is the source of truth: this reads `docs/schedule.html` rather
than re-deriving the table, so the two editions cannot drift. Render the site
first.

Output is `brightspace/schedule.html` (gitignored, like the rest of the kit).
Open it, select all, and paste into the Brightspace HTML editor.

Run:  .venv/bin/python scripts/build_brightspace_schedule.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RENDERED = REPO / "docs" / "schedule.html"
STYLES = REPO / "styles.css"
OUT = REPO / "brightspace" / "schedule.html"

SITE = ("https://davi-moreira.github.io/"
        "2026F_evidence_driven_research_purdue_HONR464/")

#: The same ceiling the course page is held to, applied to the same four counts.
CEILING = 65535


#: Column widths, matching styles.css's .overflow-table rules. They go on the
#: eight header cells as inline `style` attributes rather than into a <style>
#: block: Brightspace's sanitiser strips <style> from pasted content in some
#: configurations, and a browser propagates a column width from the first row
#: anyway. Inline is both more robust here and cheaper, 8 attributes against a
#: 925-byte rule block.
COL_WIDTHS = ["3%", "7%", "5%", "13%", "19%", "7%", "12%", "34%"]

TABLE_STYLE = ("width:100%;font-size:.85rem;line-height:1.2;"
               "border-collapse:collapse")
CELL_STYLE = "padding:.3rem;text-align:left;vertical-align:top"


def table_css() -> str:
    """The .overflow-table rules from styles.css, minified, to travel inline."""
    css = STYLES.read_text()
    block = re.search(r'/\* ---- Schedule page table.*?(?=\n/\*|\Z)', css, re.S)
    rules = block.group(0) if block else ""
    rules = re.sub(r'/\*.*?\*/', '', rules, flags=re.S)
    rules = re.sub(r'\s+', ' ', rules)
    rules = re.sub(r'\s*([{}:;,])\s*', r'\1', rules)
    return rules.strip()


def widen(frag: str) -> str:
    """Put the layout on the table and its header cells, inline."""
    frag = frag.replace("<table", f'<table style="{TABLE_STYLE}"', 1)
    cols = iter(COL_WIDTHS)
    def one_th(_m):
        try:
            return f'<th style="{CELL_STYLE};width:{next(cols)}">'
        except StopIteration:
            return "<th>"
    frag = re.sub(r"<th>", one_th, frag)
    return frag


def sizes(text: str) -> dict[str, int]:
    """Every way a 65,535 limit could count this fragment."""
    return {
        "utf-8 bytes": len(text.encode("utf-8")),
        "characters": len(text),
        "utf-16 units": len(text.encode("utf-16-le")) // 2,
        "characters, CRLF": len(text) + text.count("\n"),
    }


def build() -> str:
    if not RENDERED.exists():
        raise SystemExit(f"✗ {RENDERED.relative_to(REPO)} not rendered yet — "
                         f"run quarto render first")
    page = RENDERED.read_text(encoding="utf-8")

    m = re.search(r'<section id="course-schedule".*</section>', page, re.S)
    if not m:
        raise SystemExit("✗ could not find the course-schedule section in the "
                         "rendered page; did the generator's structure change?")
    frag = m.group(0)

    # Relative hrefs point at the course site, not at Brightspace.
    frag = re.sub(r'(href|src)="(?!https?:|mailto:|#)([^"]*)"',
                  lambda mm: f'{mm.group(1)}="{SITE}{mm.group(2)}"', frag)

    # Brightspace strips <script>, so the new-tab behaviour goes back onto each
    # link as a real attribute. No rel="noopener": every browser has implied it
    # for target="_blank" since 2021, and 233 copies of it cost 3.5 KB of a
    # budget this fragment does not have to spare.
    frag = re.sub(r'<a href="', '<a target="_blank" href="', frag)

    # styles.css does not travel with a paste. The rules ride along as one small
    # block, and the column widths ALSO go inline on the eight header cells, so
    # the table still lays out if Brightspace strips the block.
    frag = f"<style>{table_css()}</style>{widen(frag)}"

    # Whitespace is charged against the limit like any other character.
    frag = re.sub(r'>\s+<', '><', frag)
    frag = re.sub(r'[ \t]{2,}', ' ', frag)
    return frag.strip()


def main() -> None:
    frag = build()
    counts = sizes(frag)
    worst_name, worst = max(counts.items(), key=lambda kv: kv[1])

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(frag, encoding="utf-8")

    detail = "  ".join(f"{k} {v:,}" for k, v in counts.items())
    if worst > CEILING:
        raise SystemExit(
            f"✗ {OUT.relative_to(REPO)} is {worst:,} on '{worst_name}' — over "
            f"the {CEILING:,} Brightspace ceiling by {worst - CEILING:,}.\n"
            f"  {detail}\n"
            f"  Shrink the course page in its generators; this edition follows it.")

    pct = 100 * (CEILING - worst) / CEILING
    print(f"✓ wrote {OUT.relative_to(REPO)}")
    print(f"  {detail}")
    print(f"  worst count '{worst_name}' {worst:,} — {CEILING - worst:,} under "
          f"the {CEILING:,} Brightspace ceiling ({pct:.1f}% margin)")
    print(f"  {len(re.findall(r'href=\"https?:', frag))} links, all absolute; "
          f"layout inlined; no <script>")
    print("  Open it, select all, paste into the Brightspace HTML editor.")


if __name__ == "__main__":
    sys.exit(main())
