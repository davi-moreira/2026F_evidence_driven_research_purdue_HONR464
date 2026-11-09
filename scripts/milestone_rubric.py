#!/usr/bin/env python3
"""milestone_rubric.py — a milestone brief's rubric, shown band by band.

The poster rubric ships as a grading document (PDF, DOCX and an XLSX grading
sheet, scripts/build_poster_kit.py, D87): every criterion, every band, and the
points each band carries. A milestone rubric lives as a table in its brief, and
the one-page handout PDF used to reduce it to a line of weights. This module
gives a milestone the poster rubric's treatment WITHOUT a second copy of the
text: the brief's table stays the single source, and this module reads it.

  * `handout_markdown(key)` is the band-by-band table the handout PDF prints
    wherever its additions carry TOKEN (scripts/build_handout_pdfs.py).
  * `build(key)` writes the standalone rubric documents, in the poster rubric's
    format, to `_research_project/2026Fall/rubrics/`.

Edit the rubric in the BRIEF, then rerun this script and the handout builder.
Never edit the generated documents.

Every band cell in the brief ends with its point range, "(14–15)" or "(10)".
The parser refuses a table whose criteria do not sum to the heading's total, or
whose bands are not contiguous from the criterion's points down to zero, so a
typo in the brief fails here instead of shipping a broken rubric.

Usage:
    .venv/bin/python scripts/milestone_rubric.py m12          # build the documents
    .venv/bin/python scripts/milestone_rubric.py m12 --print  # show the parsed table
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRIEFS = ROOT / "_research_project" / "2026Fall"
OUT_DIR = BRIEFS / "rubrics"

#: Where a handout's additions_markdown wants the band-by-band table.
TOKEN = "{{RUBRIC_TABLE}}"

HEADING_RE = re.compile(r"^##\s+(.*?)\((\d+) points\)\s*$")
CRIT_RE = re.compile(r"^\*\*(.+?)\*\*\s*\((\d+)\)\s*$")
RANGE_RE = re.compile(r"\s*\((\d+)(?:[–-](\d+))?\)\s*$")


@dataclass
class Criterion:
    name: str
    points: int
    bands: list[tuple[int, int, str]]  # (low, high, text), best band first


@dataclass
class Rubric:
    key: str
    number: int
    topic: str
    heading: str
    total: int
    band_names: list[str]
    criteria: list[Criterion]
    notes: list[str]  # revision paragraph, then the penalty bullets

    @property
    def stem(self) -> str:
        return f"Evidence_Driven_Research_M{self.number}_Rubric"

    @property
    def title(self) -> str:
        return f"Evidence-Driven Research {self.topic} Rubric (Course Milestone M{self.number})"


def _norm(key: str | int) -> int:
    m = re.fullmatch(r"[mM]?0*(\d+)", str(key).strip())
    if not m:
        raise SystemExit(f"✗ not a milestone key: {key!r}")
    return int(m.group(1))


def brief_path(key: str | int) -> Path:
    n = _norm(key)
    hits = sorted(BRIEFS.glob(f"milestone_{n:02d}_*.md"))
    if len(hits) != 1:
        raise SystemExit(f"✗ M{n}: expected one brief, found {len(hits)}")
    return hits[0]


def _cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _band(cell: str, where: str) -> tuple[int, int, str]:
    m = RANGE_RE.search(cell)
    if not m:
        raise SystemExit(f"✗ {where}: band cell has no point range: {cell!r}")
    lo = int(m.group(1))
    hi = int(m.group(2)) if m.group(2) else lo
    return lo, hi, cell[: m.start()].strip()


def parse(key: str | int) -> Rubric:
    n = _norm(key)
    path = brief_path(n)
    lines = path.read_text(encoding="utf-8").splitlines()
    h1 = next((ln for ln in lines if ln.startswith("# ")), "")
    topic = re.sub(r"^#\s+Course milestone M\d+\s+[—-]\s+", "", h1).split(":")[0].strip()

    i = next((k for k, ln in enumerate(lines) if HEADING_RE.match(ln)), None)
    if i is None:
        raise SystemExit(f"✗ M{n}: no '## … (N points)' rubric heading in {path.name}")
    hm = HEADING_RE.match(lines[i])
    heading, total = hm.group(1).strip(), int(hm.group(2))

    j = next((k for k in range(i + 1, len(lines))
              if lines[k].startswith("| Criterion")), None)
    if j is None:
        raise SystemExit(f"✗ M{n}: no '| Criterion |' table under '{heading}'")
    band_names = _cells(lines[j])[1:]
    criteria: list[Criterion] = []
    k = j + 2  # skip the separator row
    while k < len(lines) and lines[k].startswith("|"):
        cells = _cells(lines[k])
        cm = CRIT_RE.match(cells[0])
        if not cm or len(cells) != len(band_names) + 1:
            raise SystemExit(f"✗ M{n}: unreadable rubric row: {lines[k][:80]!r}")
        name, pts = cm.group(1), int(cm.group(2))
        bands = [_band(c, f"M{n} {name}") for c in cells[1:]]
        expect_hi = pts
        for lo, hi, _ in bands:  # contiguous from the points down to zero
            if hi != expect_hi or lo > hi:
                raise SystemExit(f"✗ M{n} {name}: bands are not contiguous "
                                 f"({[(b[0], b[1]) for b in bands]})")
            expect_hi = lo - 1
        if expect_hi != -1:
            raise SystemExit(f"✗ M{n} {name}: the lowest band does not reach 0")
        criteria.append(Criterion(name, pts, bands))
        k += 1
    if sum(c.points for c in criteria) != total:
        raise SystemExit(f"✗ M{n}: criteria sum to {sum(c.points for c in criteria)}, "
                         f"heading says {total}")

    # Notes: the paragraphs between the table and the next rule, then the
    # bullets of a "## Penalties" section if one follows.
    notes: list[str] = []
    para: list[str] = []
    while k < len(lines) and lines[k].strip() != "---" and not lines[k].startswith("## "):
        if lines[k].strip():
            para.append(lines[k].strip())
        elif para:
            notes.append(" ".join(para))
            para = []
        k += 1
    if para:
        notes.append(" ".join(para))
    pen = next((p for p in range(k, len(lines)) if lines[p].strip() == "## Penalties"), None)
    if pen is not None:
        item: list[str] = []
        for ln in lines[pen + 1:]:
            if ln.startswith("## ") or ln.strip() == "---":
                break
            if ln.startswith("- "):
                if item:
                    notes.append(" ".join(item))
                item = [ln[2:].strip()]
            elif ln.strip() and item:
                item.append(ln.strip())
        if item:
            notes.append(" ".join(item))
    return Rubric(f"M{n}", n, topic, heading, total, band_names, criteria, notes)


def _plain(md: str) -> str:
    """Markdown emphasis and code marks off, for the DOCX and XLSX cells."""
    return re.sub(r"\*\*|(?<!\w)\*(?!\s)|(?<!\s)\*(?!\w)|`", "", md)


def _pts(lo: int, hi: int) -> str:
    return f"{lo}–{hi} pts" if lo != hi else f"{lo} pts"


# ---------------------------------------------------------------------------
# the handout table
# ---------------------------------------------------------------------------
def handout_markdown(key: str | int) -> str:
    r = parse(key)
    head = "| Criterion | " + " | ".join(r.band_names) + " |"
    # Pipe-table dash counts set the relative column widths in the PDF.
    sep = "|:" + "-" * 18 + "|" + "|".join(":" + "-" * w for w in (29, 21, 19, 18)[: len(r.band_names)]) + "|"
    rows = [head, sep]
    for c in r.criteria:
        cells = [f"**{c.name}** ({c.points} pts)"]
        cells += [f"**{_pts(lo, hi)}:** {text}" for lo, hi, text in c.bands]
        rows.append("| " + " | ".join(cells) + " |")
    rows.append("| **Total** | **" + str(r.total) + " points** |"
                + " |" * (len(r.band_names) - 1))
    return "\n".join(rows)


# ---------------------------------------------------------------------------
# the standalone documents, in the poster rubric's format
# ---------------------------------------------------------------------------
def build_docx(r: Rubric, path: Path) -> None:
    from docx import Document
    from docx.enum.section import WD_ORIENT
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Inches, Pt, RGBColor

    doc = Document()
    sec = doc.sections[0]
    sec.orientation = WD_ORIENT.LANDSCAPE
    sec.page_width, sec.page_height = Inches(11), Inches(8.5)  # US letter, landscape
    for side in ("left_margin", "right_margin"):
        setattr(sec, side, Inches(0.5))
    sec.top_margin = sec.bottom_margin = Inches(0.4)

    style = doc.styles["Normal"]
    style.font.name = "Arial"
    style.element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
    style.font.size = Pt(8.5)
    style.paragraph_format.space_after = Pt(2)

    def para(text, size=8.5, bold=False, after=2):
        p = doc.add_paragraph()
        run = p.add_run(text)
        run.font.size, run.bold = Pt(size), bold
        p.paragraph_format.space_after = Pt(after)
        return p

    para(r.title, 14, bold=True, after=1)
    para(f"{r.total} points. Each criterion is scored in one band; the band's "
         f"points are a range, and the grader places the score inside it.", 8.5, after=4)

    headers = ["#", "Criterion", "Pts"] + r.band_names + ["Score"]
    widths = [0.3, 1.45, 0.4, 2.55, 1.85, 1.6, 1.35, 0.5]  # 10.0 in
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    for gc, w in zip(t._tbl.tblGrid.findall(qn("w:gridCol")), widths):
        gc.set(qn("w:w"), str(int(w * 1440)))

    def shade(cell, hexcolor):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"), hexcolor)
        tcPr.append(shd)

    def fill(cell, runs, size=9):
        cell.text = ""
        p = cell.paragraphs[0]
        for text, bold in runs:
            run = p.add_run(text)
            run.font.size, run.bold = Pt(size), bold
        p.paragraph_format.space_after = Pt(0)

    for j, h in enumerate(headers):
        c = t.rows[0].cells[j]
        fill(c, [(h, True)], 9)
        c.paragraphs[0].runs[0].font.color.rgb = RGBColor.from_string("CFB991")
        shade(c, "000000")
    trPr = t.rows[0]._tr.get_or_add_trPr()
    hdr = OxmlElement("w:tblHeader")
    hdr.set(qn("w:val"), "true")
    trPr.append(hdr)

    for i, crit in enumerate(r.criteria, 1):
        cells = t.add_row().cells
        fill(cells[0], [(str(i), True)])
        fill(cells[1], [(crit.name, True)])
        fill(cells[2], [(str(crit.points), True)])
        for k, (lo, hi, text) in enumerate(crit.bands):
            fill(cells[3 + k], [(f"{_pts(lo, hi)}: ", True), (_plain(text), False)])
        fill(cells[-1], [("", False)])
        shade(cells[1], "EDEDED")
    total = t.add_row().cells
    fill(total[1], [("Total", True)])
    fill(total[2], [(str(r.total), True)])
    for row in t.rows:
        for j, w in enumerate(widths):
            row.cells[j].width = Inches(w)
        trPr = row._tr.get_or_add_trPr()
        cant = OxmlElement("w:cantSplit")
        cant.set(qn("w:val"), "true")
        trPr.append(cant)

    if r.notes:
        para("", after=2)
        para("Revision and penalties", 9, bold=True, after=1)
        for note in r.notes:
            p = para("", after=1)
            p.style = doc.styles["List Bullet"]
            run = p.add_run(_plain(note))
            run.font.size = Pt(8.5)
    doc.core_properties.title = r.title
    doc.core_properties.author = "Davi Moreira"
    doc.save(path)


def build_xlsx(r: Rubric, path: Path) -> None:
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

    wb = Workbook()
    ws = wb.active
    ws.title = "Rubric"
    ws.append(["#", "Criterion", "Points"] + r.band_names + ["Score", "Comment"])
    thin = Side(style="thin", color="999999")
    for i, c in enumerate(r.criteria, 1):
        ws.append([i, c.name, c.points]
                  + [f"{_pts(lo, hi)}: {_plain(text)}" for lo, hi, text in c.bands]
                  + [None, None])
    n = len(r.criteria)
    score_col = chr(ord("A") + 3 + len(r.band_names))
    ws.append([None, "Total", f"=SUM(C2:C{n + 1})"] + [None] * len(r.band_names)
              + [f"=SUM({score_col}2:{score_col}{n + 1})", None])
    if r.notes:
        ws.append([])
        ws.append([None, "Revision and penalties"])
        for note in r.notes:
            ws.append([None, _plain(note)])
    widths = {"A": 4, "B": 30, "C": 8}
    for k in range(len(r.band_names)):
        widths[chr(ord("D") + k)] = 50 if k == 0 else 40
    widths[score_col] = 9
    widths[chr(ord(score_col) + 1)] = 40
    for col, w in widths.items():
        ws.column_dimensions[col].width = w
    for row in ws.iter_rows(min_row=1, max_row=n + 2):
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, vertical="top")
            cell.border = Border(left=thin, right=thin, top=thin, bottom=thin)
    for cell in ws[1]:
        cell.font = Font(bold=True, color="CFB991")
        cell.fill = PatternFill("solid", fgColor="000000")
    for cell in ws[n + 2]:
        cell.font = Font(bold=True)
    ws.freeze_panes = "B2"
    wb.save(path)


def build(key: str | int) -> list[Path]:
    from build_poster_kit import to_pdf  # the poster rubric's DOCX -> PDF route

    r = parse(key)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    docx = OUT_DIR / f"{r.stem}.docx"
    xlsx = OUT_DIR / f"{r.stem}.xlsx"
    build_docx(r, docx)
    build_xlsx(r, xlsx)
    pdf = to_pdf(docx, OUT_DIR)
    return [pdf, docx, xlsx]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("milestones", nargs="+", help="e.g. m12")
    ap.add_argument("--print", action="store_true", help="show the parsed table, build nothing")
    a = ap.parse_args()
    sys.path.insert(0, str(ROOT / "scripts"))
    for key in a.milestones:
        if a.print:
            print(handout_markdown(key))
            for note in parse(key).notes:
                print("·", note)
            continue
        for p in build(key):
            print(f"✓ {p.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
