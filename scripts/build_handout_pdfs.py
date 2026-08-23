#!/usr/bin/env python3
"""build_handout_pdfs.py — the Brightspace handout PDFs, date-free and reusable.

Two families of student-facing instructions get uploaded to Brightspace as PDFs:

  * the seventeen milestone briefs  (_research_project/2026Fall/milestone_NN_*.md)
  * the Student Research Lead suite (project/srl/*.md)

Those PDFs must be reusable in ANY future edition of the course, so they carry
NO calendar dates, NO deadline clock times and NO semester labels. Every real
date lives on the course Brightspace page instead.

The dated briefs stay the single source of truth. This script never edits them:
it applies the ordered, exact-string rewrites in
`_research_project/handout_rewrites.yml`, normalizes the markdown for print,
scans the result for anything date-shaped, and only then renders.

A rewrite whose `find` no longer matches exactly once is a HARD FAILURE. That is
the point: it is the signal that a brief changed under a rule and the rule needs
rewriting too.

FUTURE EDITIONS: the only edition-specific thing left in the PDFs is the site /
repository slug inside links. Change SITE_SLUG below and rerun.

Usage:
    .venv/bin/python scripts/build_handout_pdfs.py                 # everything
    .venv/bin/python scripts/build_handout_pdfs.py --only m11 srl  # a subset
    .venv/bin/python scripts/build_handout_pdfs.py --check         # scan, no render
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
BRIEFS = REPO / "_research_project" / "2026Fall"
SRL = REPO / "project" / "srl"
REWRITES = REPO / "_research_project" / "handout_rewrites.yml"
OUT = REPO / "_handouts"

SITE_SLUG = "2026F_evidence_driven_research_purdue_HONR464"
COURSE = "HONR 46400 · Evidence-Driven Research"

QUARTO = "/Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto"
if not Path(QUARTO).exists():
    QUARTO = shutil.which("quarto") or "quarto"

#: SRL documents that are STUDENT-facing. `instructor_intervention_protocol.md`
#: is deliberately absent: it is how the instructor rescues a stalling lecture,
#: and a lead who reads it leads to the protocol instead of to the room.
SRL_DOCS = [
    ("srl_handbook.md", "Student Research Lead Handbook"),
    ("srl_prep_template.md", "SRL Preparation Template"),
    ("srl_rubric.md", "SRL Performance Rubric"),
    ("srl_ai_integration_guide.md", "SRL Guide: Directing AI in Front of the Room"),
    ("socratic_question_bank.md", "SRL Socratic Question Bank"),
    ("srl_peer_feedback_form.md", "SRL Peer Feedback Form"),
    ("absent_lead_protocol.md", "SRL Protocol: When a Lead Cannot Be There"),
]

# ---------------------------------------------------------------------------
# date scanning

#: Masked before scanning: fenced code, inline code, link targets, bare URLs.
#: A year inside `…/2026F_evidence…/…` is a URL slug, not a date.
MASKS = [
    re.compile(r"```.*?```", re.S),
    re.compile(r"`[^`\n]*`"),
    re.compile(r"\]\([^)\n]*\)"),
    re.compile(r"https?://\S+"),
]

#: Hard failures. These pin a handout to one offering of the course.
FATAL = [
    (re.compile(r"\b(January|February|March|April|June|July|August|September"
                r"|October|November|December)\b"), "month name"),
    (re.compile(r"\bMay\s+\d{1,2}\b"), "month name"),
    (re.compile(r"\b(Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sept?|Oct|Nov|Dec)\.?\s+\d{1,2}\b"),
     "abbreviated date"),
    (re.compile(r"\b\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)\b"), "deadline clock time"),
    (re.compile(r"\b(?:Fall|Spring|Summer|Autumn|Winter)\s+\d{4}\b"), "semester label"),
]

#: Reported, never fatal. Bare years in these briefs are illustrative examples
#: ("prices from 2019 to 2025") or bibliographic citations, not course dates.
WARN = [(re.compile(r"\b(?:19|20)\d{2}\b"), "bare year (check it is an example, not a date)")]


def mask(text: str) -> str:
    for m in MASKS:
        text = m.sub(lambda mo: " " * len(mo.group(0)), text)
    return text


def scan(text: str, label: str) -> tuple[list[str], list[str]]:
    masked = mask(text)
    lines = masked.split("\n")
    raw = text.split("\n")
    fatal, warn = [], []
    for i, line in enumerate(lines, 1):
        for pat, why in FATAL:
            for mo in pat.finditer(line):
                fatal.append(f"  {label}:{i} {why}: {mo.group(0)!r}  |  {raw[i-1].strip()[:110]}")
        for pat, why in WARN:
            for mo in pat.finditer(line):
                warn.append(f"  {label}:{i} {why}: {mo.group(0)!r}  |  {raw[i-1].strip()[:110]}")
    return fatal, warn


# ---------------------------------------------------------------------------
# markdown -> print

#: Three conference-block milestones anchor no new chapter, so their Book Anchor
#: list is empty and the lead-in sentence points at nothing. On the page a reader
#: can see the gap; in a PDF handout it reads as a missing list, so say it plainly.
ANCHOR_LEAD = re.compile(
    r"This milestone is anchored in the course book, \*\*EDR\\\|AI\*\*\. Read the chapters\s*\n"
    r"below as you develop the milestone, and complete each chapter's closing \*\*\"It\s*\n"
    r"is your turn\"\*\* section in its companion Colab notebook \(or carry the same\s*\n"
    r"work inside your project notebook\):\s*\n")

ANCHOR_NONE = (
    "This milestone anchors no new chapter of the course book, **EDR\\|AI**. It "
    "carries forward the \"It is your turn\" work you have already completed, so "
    "bring those sections with you rather than starting new ones.\n")


def normalize(text: str) -> str:
    """Turn a site-facing brief into a self-contained printed handout."""
    # 1. HTML comments (the generated bridge markers) never print
    text = re.sub(r"<!--.*?-->\n?", "", text, flags=re.S)
    # 2. an empty Book Anchor list would print a lead-in pointing at nothing
    if "- Ch. " not in text and ANCHOR_LEAD.search(text):
        text = ANCHOR_LEAD.sub(ANCHOR_NONE, text)
    # 3. links to sibling markdown files are dead in a PDF: keep the words
    text = re.sub(r"\[([^\]]+)\]\((?!https?:)[^)]*\.md[^)]*\)", r"**\1**", text)
    # 4. Quarto link attributes are not markdown
    text = text.replace('{target="_blank"}', "")
    # 5. a future edition changes one constant, not 17 documents
    text = text.replace("2026F_evidence_driven_research_purdue_HONR464", SITE_SLUG)
    return text


def split_title(text: str, fallback: str) -> tuple[str, str]:
    """The H1 becomes the PDF title; the body starts under it."""
    m = re.match(r"#\s+(.+?)\n", text)
    if not m:
        return fallback, text
    title = m.group(1).strip()
    title = title.replace("Course milestone ", "").replace("—", "·")
    title = re.sub(r"\s+", " ", title).strip()
    return title, text[m.end():].lstrip("\n")


#: Typst preamble, passed via `include-in-header` rather than as a body block:
#: a `#set page(...)` reached mid-document starts a NEW page in typst, which
#: cost every handout a blank first page. In the preamble it just applies.
#: Hyphenation off because the five-column rubric tables otherwise break words
#: like "architec-ture" across three lines.
TYPST_HEADER = """#set text(hyphenate: false)
#show table: set text(size: 8.6pt)
#show heading.where(level: 2): set block(above: 1.4em, below: 0.6em)
#set page(footer: context [
  #set text(7.6pt, fill: luma(120))
  #grid(columns: (1fr, auto),
    align: (left, right),
    [{footer}],
    [#counter(page).display()])
])
"""


def render(title: str, body: str, out_pdf: Path, footer: str) -> None:
    front = (
        "---\n"
        f'title: "{title}"\n'
        f'subtitle: "{COURSE}"\n'
        "format:\n"
        "  typst:\n"
        "    papersize: us-letter\n"
        "    margin: {x: 1.9cm, y: 2.1cm}\n"
        "    fontsize: 10pt\n"
        "    section-numbering: \"\"\n"
        "    toc: false\n"
        "    include-in-header: header.typ\n"
        "---\n\n"
    )
    with tempfile.TemporaryDirectory() as td:
        (Path(td) / "header.typ").write_text(TYPST_HEADER.format(footer=footer))
        qmd = Path(td) / "handout.qmd"
        qmd.write_text(front + body)
        r = subprocess.run([QUARTO, "render", str(qmd), "--to", "typst"],
                           capture_output=True, text=True, cwd=td)
        pdf = Path(td) / "handout.pdf"
        if r.returncode or not pdf.exists():
            sys.stderr.write(r.stdout[-4000:] + r.stderr[-4000:])
            raise SystemExit(f"✗ quarto failed for {out_pdf.name}")
        out_pdf.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(pdf, out_pdf)


# ---------------------------------------------------------------------------

def milestone_jobs(rules: dict) -> list[tuple[str, Path, Path, str]]:
    jobs = []
    for src in sorted(BRIEFS.glob("milestone_*.md")):
        num = src.name.split("_")[1]
        slug = src.stem.split("_", 2)[2]
        jobs.append((f"m{num}", src,
                     OUT / "milestones" / f"HONR46400_M{num}_{slug}.pdf",
                     f"{COURSE} · Milestone M{int(num)}"))
    return jobs


def srl_jobs() -> list[tuple[str, Path, Path, str]]:
    jobs = []
    for i, (name, label) in enumerate(SRL_DOCS, 1):
        jobs.append((f"srl{i}", SRL / name,
                     OUT / "srl" / f"HONR46400_SRL_{i:02d}_{Path(name).stem}.pdf",
                     f"{COURSE} · Student Research Lead"))
    return jobs


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", default=None,
                    help="job keys or families: m01 … m17, srl, milestones")
    ap.add_argument("--check", action="store_true", help="scan only, do not render")
    args = ap.parse_args()

    rules = yaml.safe_load(REWRITES.read_text())["files"]
    jobs = milestone_jobs(rules) + srl_jobs()
    if args.only:
        want = set(args.only)
        jobs = [j for j in jobs
                if j[0] in want
                or ("srl" in want and j[0].startswith("srl"))
                or ("milestones" in want and j[0].startswith("m") and not j[0].startswith("srl"))]
        if not jobs:
            raise SystemExit(f"✗ nothing matched {sorted(want)}")

    all_fatal, all_warn, built = [], [], 0
    for key, src, dest, footer in jobs:
        text = src.read_text()
        for r in rules.get(src.name, {}).get("rules", []):
            n = text.count(r["find"])
            if n != 1:
                raise SystemExit(
                    f"✗ {src.name}: rewrite matched {n} times, expected 1.\n"
                    f"  The brief changed under this rule. Fix it in {REWRITES.name}.\n"
                    f"  find: {r['find'][:160]!r}")
            text = text.replace(r["find"], r["replace"])
        text = normalize(text)
        fatal, warn = scan(text, src.name)
        all_fatal += fatal
        all_warn += warn
        if fatal or args.check:
            continue
        title, body = split_title(text, src.stem)
        render(title, body, dest, footer)
        built += 1
        print(f"  ✓ {dest.relative_to(REPO)}")

    if all_warn:
        print(f"\n⚠️  {len(all_warn)} bare year(s) left in place (examples and citations):")
        for w in all_warn:
            print(w)
    if all_fatal:
        print(f"\n✗ {len(all_fatal)} date(s) survived the rewrites — nothing rendered "
              f"for those documents:")
        for f in all_fatal:
            print(f)
        sys.exit(1)
    if args.check:
        print(f"\n✓ {len(jobs)} document(s) scanned clean — no dates, no clock times, "
              f"no semester labels")
        return
    print(f"\n✓ {built} handout PDF(s) in {OUT.relative_to(REPO)}/")


if __name__ == "__main__":
    main()
