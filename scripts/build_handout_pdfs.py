#!/usr/bin/env python3
"""build_handout_pdfs.py — the Brightspace PDFs, built BOOK-FIRST.

Two families of student-facing instructions are handed to students as PDFs:

  * the seventeen course milestones  -> _research_project/2026Fall/*.pdf
  * the Student Research Lead suite  -> project/srl/*.pdf

Each PDF sits in the SAME FOLDER as the source it is developed from, named with
the same stem, so the pair is always obvious.

THE MILESTONE RULE (instructor ruling, 2026-08-23)
--------------------------------------------------
A course milestone is, in the normal case, simply its Book Milestone. When that
is true the PDF follows the book's own milestone page and nothing else. Keep it
simple: no restatement, no elaboration, no parallel rubric. The course schedule
links straight to that book page.

Only where the COURSE adds something the book does not ask for does the PDF
carry an extra section, "What this course adds", placed before the book content.
Those additions are authored once in

    _research_project/milestone_course_additions.yml

under `classification` / `additions_markdown`.

WHAT COUNTS AS AN ADDITION (instructor ruling, 2026-08-23, narrowed): ONLY what
the Undergraduate Research Expo itself requires and the book milestone does not
carry. Applying, the published abstract, the peer review of the boards, the
printed poster and its lock, the spoken pitches, the invitation, presenting, and
evidencing that you presented. Course logistics, classroom drills, reproducibility
packaging, rubric wording and analysis-craft practice are NOT additions, however
much the course values them: they belong in the milestone brief on the course
platform, not in this PDF. Their authored text is preserved in the additions file
under `retired_additions_markdown`.

`schedule_mark` in that same file drives the schedule plus. Under the narrowed
rule the two coincide: a milestone carries a section exactly when it is marked.

WHAT IS ENFORCED
----------------
  * NO em dashes anywhere in a PDF (instructor ruling). Normalized on the way
    out, exactly as the schedule page is, so upstream prose keeps its own style.
  * NO calendar dates, clock times or semester labels, so the PDFs are reusable
    in any future edition. Brightspace carries every real deadline. A document
    that still has one is a HARD FAILURE and does not render.
  * EVERY milestone PDF closes with "Making the PDF you hand in", authored once
    in scripts/submission_pdf_howto.py and shared with the briefs, because the
    file every milestone asks for has to be produced from a Colab notebook and
    Colab has no export button.
  * ONE submission file per milestone, `lastname_mNN.pdf`. Anything that used to
    be a separate PDF is a section inside it. Artifacts that genuinely cannot
    live inside a PDF are declared per milestone in the additions file.

FUTURE EDITIONS: change SITE_SLUG and rerun. That is the only edition-specific
thing left in these documents.

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
sys.path.insert(0, str(REPO / "scripts"))

from milestone_map import additions, milestone_map  # noqa: E402
from submission_pdf_howto import POINTER, markdown as howto_markdown  # noqa: E402

STUDIOS = REPO / "book" / "studios"
SRL = REPO / "project" / "srl"

SITE_SLUG = "2026F_evidence_driven_research_purdue_HONR464"
SITE = f"https://davi-moreira.github.io/{SITE_SLUG}"
COURSE = "HONR 46400 · Evidence-Driven Research"

QUARTO = "/Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto"
if not Path(QUARTO).exists():
    QUARTO = shutil.which("quarto") or "quarto"

#: SRL documents that are STUDENT-facing. Two of the suite's documents are
#: deliberately absent, both because they are written to the instructor and both
#: because a lead who reads them prepares for the wrong thing:
#: `instructor_intervention_protocol.md` (how the instructor rescues a stalling
#: lecture, so a lead who reads it leads to the protocol instead of to the room)
#: and `absent_lead_protocol.md` (how a standby is drawn when a lead no-shows,
#: which is an instructor decision and reads as a way out to the student).
SRL_DOCS = [
    "srl_handbook.md",
    "srl_submission_instructions.md",
    "srl_prep_template.md",
    "srl_rubric.md",
    "srl_ai_integration_guide.md",
    "socratic_question_bank.md",
    "srl_peer_feedback_form.md",
]

# ---------------------------------------------------------------------------
# em dashes

EM = "—"

#: Ordered, most specific first; the last rule is the net, so an em dash a
#: future edit introduces becomes a colon rather than reaching a student.
#: The exceptions below are the places where a colon would be ungrammatical:
#: before a conjunction, or where the dash opens a parenthetical pair.
DASH_RULES: list[tuple[object, str]] = [
    (re.compile(rf"\[(Lesson \d+|Ch\. \d+|Milestone \d+) {EM} "), r"[\1: "),
    # dash pairs: the sentence resumes after the second dash
    (f"the package {EM} a number", "the package (a number"),
    (f"a stranger would follow {EM} makes", "a stranger would follow) makes"),
    (f"calls tools {EM} and never", "calls tools, and never"),
    # a colon cannot precede a conjunction
    (f"declaration {EM} or the defended", "declaration, or the defended"),
    (f"uncertainty statement {EM} plus the", "uncertainty statement, plus the"),
    (f"documentation {EM} and freeze", "documentation, and freeze"),
    (f"together {EM} carrying", ", carrying"),
    (f"version's reason {EM} not a", "version's reason, not a"),
    (f"the tool gets {EM} the choice", "the tool gets, the choice"),
    (f"uncertainty {EM} name which", "uncertainty; name which"),
    # the net
    (f" {EM} ", ": "),
    (EM, ": "),
]


def no_em_dash(text: str) -> str:
    for find, repl in DASH_RULES:
        text = find.sub(repl, text) if hasattr(find, "sub") else text.replace(find, repl)
    if EM in text:                                  # unreachable via the net
        raise SystemExit("✗ em dash survived normalization")
    return text


# ---------------------------------------------------------------------------
# date scanning

#: Masked before scanning: fenced code, inline code, link targets, bare URLs.
#: A year inside a repository slug is a URL, not a date.
MASKS = [
    re.compile(r"```.*?```", re.S),
    re.compile(r"`[^`\n]*`"),
    re.compile(r"\]\([^)\n]*\)"),
    re.compile(r"https?://\S+"),
]

FATAL = [
    (re.compile(r"\b(January|February|March|April|June|July|August|September"
                r"|October|November|December)\b"), "month name"),
    (re.compile(r"\bMay\s+\d{1,2}\b"), "month name"),
    (re.compile(r"\b(Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sept?|Oct|Nov|Dec)\.?\s+\d{1,2}\b"),
     "abbreviated date"),
    (re.compile(r"\b\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)\b"), "deadline clock time"),
    (re.compile(r"\b(?:Fall|Spring|Summer|Autumn|Winter)\s+\d{4}\b"), "semester label"),
]

WARN = [(re.compile(r"\b(?:19|20)\d{2}\b"), "bare year (check it is an example)")]


def scan(text: str, label: str) -> tuple[list[str], list[str]]:
    masked = text
    for m in MASKS:
        masked = m.sub(lambda mo: " " * len(mo.group(0)), masked)
    raw = text.split("\n")
    fatal, warn = [], []
    for i, line in enumerate(masked.split("\n"), 1):
        for pat, why in FATAL:
            for mo in pat.finditer(line):
                fatal.append(f"  {label}:{i} {why}: {mo.group(0)!r}  |  {raw[i-1].strip()[:100]}")
        for pat, why in WARN:
            for mo in pat.finditer(line):
                warn.append(f"  {label}:{i} {why}: {mo.group(0)!r}  |  {raw[i-1].strip()[:100]}")
    return fatal, warn


# ---------------------------------------------------------------------------
# book milestone page -> printable markdown

REVIEW_BANNER = re.compile(
    r"::: \{\.callout-warning \.review-pending[^}]*\}.*?:::\s*\n", re.S)
BADGE = re.compile(r"\[!\[\]\((?:[^)]*)\)\{[^}]*\}\]\((?P<url>[^)]+)\)\{[^}]*\}")


def book_page(path: Path) -> tuple[str, str]:
    """(title, body) of a book milestone page, cleaned for print."""
    t = path.read_text()
    t = re.sub(r"\A---\n.*?\n---\n", "", t, flags=re.S)      # aliases front matter
    t = REVIEW_BANNER.sub("", t)                             # book-development banner
    m = re.search(r"^# (.+?)(?:\s*\{[^}]*\})?\s*$", t, re.M)
    title = m.group(1).strip() if m else path.stem
    t = t[:m.start()] + t[m.end():] if m else t
    t = BADGE.sub(lambda mo: f"**[Open the milestone workbook in Colab]({mo.group('url')})**", t)
    t = re.sub(r"\]\((?!https?:)([a-z0-9-]+)\.qmd([^)]*)\)",
               rf"]({SITE}/book/studios/\1.html)", t)
    t = t.replace('{target="_blank"}', "").replace("{#milestone}", "")
    # the badge became a text link, so the book's own cross-reference to it must
    # follow, or "the badge above" points at nothing on the page
    t = t.replace("with the badge above", "with the link above")
    t = re.sub(r"\n{3,}", "\n\n", t).strip()
    return title, t


def _short(title: str) -> str:
    """"Milestone 6: Your data and measurement, governed" -> the part after the
    colon, so "Book Milestone 6: Milestone 6: ..." never doubles up."""
    return re.sub(r"^Milestone \d+:\s*", "", title)


def demote(body: str, by: int = 1) -> str:
    """Push every ATX heading down `by` levels so it nests under a wrapper."""
    return re.sub(r"^(#{1,5}) ", lambda m: "#" * (len(m.group(1)) + by) + " ",
                  body, flags=re.M)


# ---------------------------------------------------------------------------
# one milestone document

def milestone_doc(key: str, info: dict, add: dict) -> tuple[str, str]:
    """(title, markdown body) for one course milestone PDF."""
    n = int(info["num"])
    title = f"Course milestone M{n}: {info['topic']}"
    extras = add.get("extra_artifacts") or []

    main = f"`lastname_m{info['num']}.pdf`"
    lead = (f"One file, {main}. Everything this milestone asks for goes inside "
            f"it, as sections in the order below.")
    if extras:
        lead = (f"One document, {main}. Everything this milestone asks for goes "
                f"inside it, as sections in the order below. "
                f"{'One artifact travels' if len(extras) == 1 else 'These artifacts travel'} "
                f"beside it, because {'it' if len(extras) == 1 else 'they'} cannot "
                f"live inside a PDF:")

    head = [
        "## What to submit",
        "",
        lead,
        "",
        f"Submit it on Brightspace, under **Assignments** then **M{info['num']}**. "
        f"Brightspace carries the deadline.",
        "",
        POINTER,
        "",
        "This milestone presents "
        + " and ".join(f"**Book Milestone {b['n']}: {_short(b['title'])}** "
                       f"({b['relationship']}, {b['version_label']})"
                       for b in info["books"])
        + " of the course book, EDR\\|AI.",
        "",
    ]
    for e in extras:
        head.append(f"- `{e['name']}`: {e['why']}")
    if extras:
        head.append("")

    body = ["\n".join(head)]

    if add.get("additions_markdown"):
        body.append("## What this course adds\n")
        body.append(add["additions_markdown"].strip() + "\n")

    for i, page in enumerate(info["pages"]):
        ptitle, pbody = book_page(page)
        if add.get("additions_markdown") or len(info["pages"]) > 1:
            body.append(f"## {ptitle}\n")
            body.append(demote(pbody) + "\n")
        else:
            body.append(pbody + "\n")

    # The one place the course says how a Colab notebook becomes the PDF this
    # milestone collects. Last, because it is a routine you need once and then
    # know; POINTER (above) sends the first-time reader here.
    body.append(howto_markdown())
    return title, "\n".join(body)


# ---------------------------------------------------------------------------
# render

#: Typst preamble goes through `include-in-header`: a `#set page(...)` reached
#: mid-document starts a NEW page in typst, which costs a blank first page.
#: Hyphenation is off because the wide rubric tables otherwise break words
#: across three lines.
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
        '    section-numbering: ""\n'
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
        shutil.copy(pdf, out_pdf)


# ---------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", default=None,
                    help="job keys or families: m01 .. m17, srl, milestones")
    ap.add_argument("--check", action="store_true", help="scan only, do not render")
    args = ap.parse_args()

    adds = additions()
    mmap = milestone_map()

    jobs = []
    for key, info in sorted(mmap.items()):
        add = adds.get(key, {})
        title, body = milestone_doc(key, info, add)
        jobs.append((f"m{info['num']}", info["brief"].name, title, body,
                     info["brief"].with_suffix(".pdf"),
                     f"{COURSE} · Milestone M{int(info['num'])}"))
    for name in SRL_DOCS:
        src = SRL / name
        t = src.read_text()
        m = re.search(r"^# (.+)$", t, re.M)
        title = m.group(1).strip() if m else src.stem
        body = (t[:m.start()] + t[m.end():]).strip() if m else t
        jobs.append((f"srl:{src.stem}", name, title, body,
                     src.with_suffix(".pdf"),
                     f"{COURSE} · Student Research Lead"))

    if args.only:
        want = set(args.only)
        jobs = [j for j in jobs
                if j[0] in want
                or ("srl" in want and j[0].startswith("srl"))
                or ("milestones" in want and not j[0].startswith("srl"))]
        if not jobs:
            raise SystemExit(f"✗ nothing matched {sorted(want)}")

    all_fatal, all_warn, built = [], [], 0
    for key, label, title, body, dest, footer in jobs:
        body = no_em_dash(body)
        title = no_em_dash(title)
        fatal, warn = scan(body, label)
        all_fatal += fatal
        all_warn += warn
        if fatal or args.check:
            continue
        render(title, body, dest, footer)
        built += 1
        print(f"  ✓ {dest.relative_to(REPO)}")

    if all_warn:
        print(f"\n⚠️  {len(all_warn)} bare year(s) left in place:")
        for w in all_warn:
            print(w)
    if all_fatal:
        print(f"\n✗ {len(all_fatal)} date(s) reached a handout: nothing rendered "
              f"for those documents:")
        for f in all_fatal:
            print(f)
        sys.exit(1)
    if args.check:
        print(f"\n✓ {len(jobs)} document(s) scanned clean: no dates, no clock "
              f"times, no semester labels, no em dashes")
        return
    print(f"\n✓ {built} PDF(s) written beside their sources")


if __name__ == "__main__":
    main()
