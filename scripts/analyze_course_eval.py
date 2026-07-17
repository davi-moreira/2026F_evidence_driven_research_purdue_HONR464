#!/usr/bin/env python3
"""
Course Evaluation Analyzer
==========================

Turns Purdue / DSB anonymous end-of-term course-evaluation PDFs into a single,
readable performance report — quantitative *and* qualitative — for the
instructor.

This is a **portable, course-agnostic** tool. It hardcodes no course name,
term, or instructor: everything is auto-detected from the PDF header, so the
same script drops into every course repository unchanged. Point it at the
folder where you saved the evaluation PDFs and it does the rest.

What it reads
-------------
The official export is a *bundle* of PDFs. Two kinds matter:

  * The per-respondent file (name usually starts with ``Response-``). One page
    per student, with the full closed-form answers AND the free-text comments.
    This is the richest source and the one the report is built from. The tool
    auto-picks the PDF with the most pages as the per-respondent file.
  * The aggregate summary file(s) — frequency tables. Used only to recover the
    official "Response Rate: 36/41 (87.80%)" line, which the per-respondent
    file omits. Optional; the report still works without it.

What it produces  (all written into the SAME folder as the PDFs)
----------------------------------------------------------------
  * ``course_eval_report_<term>.md``  — the report (executive summary,
    course-performance tables, instructor-performance tables, Likert
    distributions, respondent profile, qualitative themes with every verbatim
    comment grouped by theme, and a "keep / improve" synthesis).
  * ``report_assets/*.png``            — charts embedded in the report
    (item means, Likert distributions, demographics, theme frequencies).
  * ``course_eval_responses_<term>.csv`` — one tidy row per respondent for
    any further analysis you want to do yourself.

The eval folder is expected to be gitignored (it holds student data); this
script lives in ``scripts/`` and IS committed so it travels between courses.

Qualitative analysis
--------------------
Rule-based by default (offline, deterministic, identical every semester): a
theme taxonomy + sentiment lexicon tag every comment, themes are ranked by
frequency, and representative quotes are pulled per theme. Pass ``--llm`` to
additionally generate a narrative synthesis with the Claude API (needs the
``anthropic`` package and an ``ANTHROPIC_API_KEY``; degrades gracefully if
either is missing).

Usage
-----
    python3 scripts/analyze_course_eval.py _adm_stuff/_course_eval/2026Summer
    python3 scripts/analyze_course_eval.py            # auto-pick latest term folder
    python3 scripts/analyze_course_eval.py <folder> --llm
    python3 scripts/analyze_course_eval.py <folder> --no-charts

Requirements
------------
    * ``pdftotext`` on PATH  (poppler:  brew install poppler  /  apt install poppler-utils)
      — or the pure-Python fallbacks ``pdfplumber`` / ``pymupdf`` if installed.
    * matplotlib  (only for charts; ``--no-charts`` skips it)
    * Standard library otherwise. pandas is used if present, not required.
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import shutil
import statistics
import subprocess
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

# --------------------------------------------------------------------------- #
# Configuration (the only things you'd ever tweak for a different institution) #
# --------------------------------------------------------------------------- #

# The five-point agreement scale used by Purdue/DSB Likert items. A closed item
# whose answer label is one of these is treated as a Likert (1-5) question;
# anything else (Sr, A, DSB, ...) is treated as a demographic question.
LIKERT_LABELS = {
    "Strongly Disagree": 1,
    "Disagree": 2,
    "Neither Agree nor Disagree": 3,
    "Agree": 4,
    "Strongly Agree": 5,
}
LIKERT_MAX = 5
LIKERT_MIDPOINT = 3
FAVORABLE_MIN = 4  # Agree or Strongly Agree counts as "favorable"

# Theme taxonomy for the qualitative pass. Each theme maps to a list of
# case-insensitive regex fragments; a comment is tagged with every theme it
# matches. Tuned to the language students actually use in course evals.
THEMES: dict[str, list[str]] = {
    "Organization & structure": [
        r"organi[sz]", r"well[- ]?organized", r"structure", r"easy to follow",
        r"straightforward", r"lay ?out", r"lining out", r"direction", r"clear path",
    ],
    "Communication & clarity": [
        r"communicat", r"\bclear\b", r"clarity", r"clearly", r"explain",
        r"instruction", r"understand what to do",
    ],
    "Responsiveness & availability": [
        r"responsive", r"\bprompt", r"\bquick", r"\bemail", r"office hour",
        r"synchronous", r"\breach", r"available", r"accessible", r"announcement",
        r"\bupdates?\b", r"get a hold", r"communication with students",
    ],
    "Care & encouragement": [
        r"\bcares?\b", r"caring", r"\bsupport", r"encourag", r"thoughtful",
        r"considerate", r"about (his|our|my|their|student).{0,15}learning",
    ],
    "Feedback & fairness": [
        r"feedback", r"\bfair\b", r"detailed (notes|feedback)", r"grading scheme",
        r"evaluat", r"\bgrade[ds]?\b", r"grading",
    ],
    "Videos & learning materials": [
        r"\bvideo", r"walkthrough", r"notebook", r"brightspace", r"resource",
        r"\bslides?\b", r"lecture material", r"textbook", r"\bmaterials?\b",
        r"micro[- ]?video",
    ],
    "Pace, schedule & workload": [
        r"condensed", r"accelerat", r"\bpac(e|ing)\b", r"schedule", r"workload",
        r"manageable", r"overwhelm", r"four[- ]week", r"\b4[- ]?week", r"8[- ]?week",
        r"eight[- ]week", r"due date", r"time span", r"\bload\b", r"deadline",
    ],
    "Assignments & exercises": [
        r"assign", r"pause[- ]and[- ]do", r"\bexercise", r"extra credit",
        r"kaggle", r"homework", r"quiz",
    ],
    "Projects & group work": [
        r"\bproject", r"\bgroup", r"case competition", r"\bteam", r"milestone",
        r"divvy", r"group[- ]?mate", r"classmate",
    ],
    "AI-generated content": [
        r"\bA\.?I\.?\b", r"artificial intelligence", r"generated", r"chatgpt",
    ],
    "Difficulty & confusion": [
        r"confus", r"unfair", r"difficult", r"\bhard\b", r"challenging",
        r"simplif", r"simpler", r"more simple", r"ambitious", r"cut off",
        r"insufficient", r"not.{0,10}sufficient", r"obstacle",
    ],
}

# Lightweight sentiment lexicon. The two open-text prompts are inherently
# framed (one asks for praise, one for suggestions), so polarity is a secondary
# signal — reported, but the themes lead.
POSITIVE_WORDS = {
    "great", "wonderful", "helpful", "enjoy", "enjoyed", "appreciate",
    "appreciated", "fair", "clear", "organized", "best", "nice", "manageable",
    "responsive", "thoughtful", "considerate", "good", "love", "loved", "like",
    "liked", "easy", "encouragement", "straightforward", "excellent", "amazing",
    "enjoyable", "honest", "well",
}
NEGATIVE_WORDS = {
    "confused", "confusing", "unfair", "difficult", "hard", "problem",
    "problems", "issue", "issues", "overwhelmed", "overwhelming", "lacking",
    "insufficient", "ambitious", "challenging", "obstacle", "obstacles",
    "unclear", "frustrating", "frustrated", "disorganized", "boring", "poor",
}

# Header regexes (general across Purdue/DSB exports).
RE_COURSE = re.compile(r"Course:\s*(.+?)\s*$", re.M)
RE_INSTRUCTOR = re.compile(r"Instructor:\s*(.+?)\s*\*?\s*$", re.M)
RE_PERIOD = re.compile(r"^\s*(.*Release.*)$", re.M)
RE_RESPONSE_RATE = re.compile(r"Response Rate:\s*(\d+)\s*/\s*(\d+)\s*\(\s*([\d.]+)\s*%\)")

# A closed item line:  "5. The course is well organized.        Strongly Agree (5)"
RE_CLOSED = re.compile(r"^\s*(\d+)\.\s+(.+?)\s{2,}(\S.*?)\s*\((\d+)\)\s*$")
# Any numbered prompt (used to find free-text question starts / boundaries).
RE_NUMBERED = re.compile(r"^\s*(\d+)\.\s+\S")


# --------------------------------------------------------------------------- #
# Text cleaning                                                                #
# --------------------------------------------------------------------------- #

# pdftotext mis-decodes a few glyphs in these exports. Map them back.
_MOJIBAKE = {
    "͛": "'",   # COMBINING ZIGZAG ABOVE  ->  apostrophe  (could?ve)
    "Ͷ": "—",  # GREEK CAPITAL LETTER PAMPHYLIAN DIGAMMA -> em dash
    "’": "'", "‘": "'", "“": '"', "”": '"',
    "–": "-", "—": "—", "ﬁ": "fi", "ﬂ": "fl",
    " ": " ",
}


def clean_text(text: str) -> str:
    """Normalize mojibake and whitespace in extracted text."""
    for bad, good in _MOJIBAKE.items():
        text = text.replace(bad, good)
    text = unicodedata.normalize("NFKC", text)
    # Drop any stray non-printable / leftover combining marks.
    text = "".join(ch for ch in text if ch == "\n" or ch == "\t" or ord(ch) >= 32)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


# --------------------------------------------------------------------------- #
# PDF -> text                                                                 #
# --------------------------------------------------------------------------- #

def pdf_to_text(path: Path) -> str:
    """Extract layout-preserving text. pdftotext first; pdfplumber/fitz fallback."""
    if shutil.which("pdftotext"):
        out = subprocess.run(
            ["pdftotext", "-layout", str(path), "-"],
            capture_output=True, text=True,
        )
        if out.returncode == 0 and out.stdout.strip():
            return out.stdout
    try:  # pragma: no cover - optional dependency
        import pdfplumber
        with pdfplumber.open(str(path)) as pdf:
            return "\f".join((pg.extract_text() or "") for pg in pdf.pages)
    except Exception:
        pass
    try:  # pragma: no cover - optional dependency
        import fitz
        doc = fitz.open(str(path))
        return "\f".join(pg.get_text() for pg in doc)
    except Exception:
        pass
    sys.exit(
        f"ERROR: cannot read {path.name}. Install poppler (`brew install poppler` "
        f"or `apt install poppler-utils`) or `pip install pdfplumber`."
    )


def pages_of(text: str) -> list[str]:
    """Split into per-page blocks, keeping only real evaluation pages."""
    return [p for p in text.split("\f") if "Purdue University" in p or RE_CLOSED.search(p)]


# --------------------------------------------------------------------------- #
# Parsing                                                                      #
# --------------------------------------------------------------------------- #

class Survey:
    """Everything parsed from the evaluation bundle."""

    def __init__(self):
        self.course = ""
        self.instructor = ""
        self.period = ""
        self.n_responses = 0
        self.n_enrolled = None        # from summary PDF, if found
        self.response_rate = None     # float percent, if found
        self.questions: dict[int, dict] = {}  # qnum -> {text, kind}
        self.respondents: list[dict] = []     # list of per-page records


def detect_header(text: str, survey: Survey) -> None:
    m = RE_COURSE.search(text)
    if m:
        survey.course = clean_text(m.group(1))
    m = RE_INSTRUCTOR.search(text)
    if m:
        survey.instructor = clean_text(m.group(1)).rstrip(" *")
    m = RE_PERIOD.search(text)
    if m:
        survey.period = clean_text(m.group(1))


def instructor_surname(survey: Survey) -> str:
    parts = survey.instructor.split()
    return parts[-1] if parts else ""


def classify_likert(question_text: str) -> str:
    """Course-level vs instructor-level Likert item."""
    return "instructor" if re.search(r"instructor", question_text, re.I) else "course"


def parse_respondent_pdf(text: str, survey: Survey) -> None:
    surname = instructor_surname(survey)
    pages = pages_of(text)
    free_text_qnums: set[int] = set()

    for page in pages:
        lines = page.splitlines()
        record = {"demographics": {}, "likert": {}, "free_text": {}}

        # 1) closed items (demographics + Likert)
        for ln in lines:
            m = RE_CLOSED.match(ln)
            if not m:
                continue
            qnum = int(m.group(1))
            qtext = clean_text(m.group(2))
            label = clean_text(m.group(3))
            weight = int(m.group(4))
            if label in LIKERT_LABELS:
                kind = classify_likert(qtext)
                record["likert"][qnum] = weight
                survey.questions.setdefault(qnum, {"text": qtext, "kind": kind})
            else:
                record["demographics"][qnum] = label
                survey.questions.setdefault(qnum, {"text": qtext, "kind": "demographic"})

        # 2) free-text questions: numbered prompts with no (weight)
        numbered_idx = [
            (i, int(RE_NUMBERED.match(l).group(1)))
            for i, l in enumerate(lines) if RE_NUMBERED.match(l)
        ]
        closed_qnums = set(record["likert"]) | set(record["demographics"])
        for pos, (line_i, qnum) in enumerate(numbered_idx):
            if qnum in closed_qnums:
                continue
            # boundary = next numbered prompt (closed or open), else end of page
            end_i = numbered_idx[pos + 1][0] if pos + 1 < len(numbered_idx) else len(lines)
            block = lines[line_i:end_i]
            # prompt ends at the first line carrying the instructor surname
            name_at = next((j for j, l in enumerate(block) if surname and surname in l), 0)
            prompt_lines = block[: name_at + 1] if name_at else block[:1]
            answer_lines = block[name_at + 1:] if name_at else block[1:]
            answer = [l.strip() for l in answer_lines
                      if l.strip() and not re.fullmatch(r"\d+", l.strip())]
            prompt = clean_text(" ".join(prompt_lines))
            prompt = re.sub(r"^\d+\.\s*", "", prompt)
            prompt = re.sub(rf"\s*-\s*{re.escape(survey.instructor)}\s*$", "", prompt).strip()
            survey.questions.setdefault(qnum, {"text": prompt, "kind": "free_text"})
            free_text_qnums.add(qnum)
            ans = clean_text(" ".join(answer))
            if ans:
                record["free_text"][qnum] = ans

        if record["likert"] or record["demographics"] or record["free_text"]:
            survey.respondents.append(record)

    survey.n_responses = len(survey.respondents)
    survey.free_text_qnums = sorted(free_text_qnums)


def parse_response_rate(summary_texts: list[str], survey: Survey) -> None:
    for text in summary_texts:
        m = RE_RESPONSE_RATE.search(text)
        if m:
            survey.n_enrolled = int(m.group(2))
            survey.response_rate = float(m.group(3))
            return


# --------------------------------------------------------------------------- #
# Quantitative analysis                                                        #
# --------------------------------------------------------------------------- #

def item_stats(scores: list[int]) -> dict:
    n = len(scores)
    dist = Counter(scores)
    favorable = sum(v for k, v in dist.items() if k >= FAVORABLE_MIN)
    return {
        "n": n,
        "mean": statistics.mean(scores) if n else float("nan"),
        "sd": statistics.stdev(scores) if n > 1 else 0.0,
        "median": statistics.median(scores) if n else float("nan"),
        "dist": {k: dist.get(k, 0) for k in range(1, LIKERT_MAX + 1)},
        "pct_favorable": 100 * favorable / n if n else float("nan"),
        "pct_top_box": 100 * dist.get(LIKERT_MAX, 0) / n if n else float("nan"),
    }


def compute_quant(survey: Survey) -> dict:
    likert_q = [q for q, meta in sorted(survey.questions.items())
                if meta["kind"] in ("course", "instructor")]
    per_item = {}
    for q in likert_q:
        scores = [r["likert"][q] for r in survey.respondents if q in r["likert"]]
        per_item[q] = item_stats(scores)

    def index_for(kind: str) -> dict:
        qs = [q for q in likert_q if survey.questions[q]["kind"] == kind]
        all_scores = [s for q in qs for s in
                      [r["likert"][q] for r in survey.respondents if q in r["likert"]]]
        item_means = [per_item[q]["mean"] for q in qs]
        return {
            "items": qs,
            "mean_of_items": statistics.mean(item_means) if item_means else float("nan"),
            "pooled_mean": statistics.mean(all_scores) if all_scores else float("nan"),
            "pct_favorable": (100 * sum(s >= FAVORABLE_MIN for s in all_scores) / len(all_scores))
            if all_scores else float("nan"),
        }

    all_likert = [s for q in likert_q for s in
                  [r["likert"][q] for r in survey.respondents if q in r["likert"]]]

    # demographics
    demo = {}
    for q, meta in sorted(survey.questions.items()):
        if meta["kind"] != "demographic":
            continue
        c = Counter(r["demographics"][q] for r in survey.respondents if q in r["demographics"])
        demo[q] = {"text": meta["text"], "counts": c, "n": sum(c.values())}

    # mean overall rating by expected-grade bucket (small-N, exploratory)
    grade_q = next((q for q, m in survey.questions.items()
                    if m["kind"] == "demographic" and re.search(r"grade", m["text"], re.I)), None)
    by_grade = {}
    if grade_q is not None:
        bucket = defaultdict(list)
        for r in survey.respondents:
            g = r["demographics"].get(grade_q)
            if g is None:
                continue
            scores = list(r["likert"].values())
            if scores:
                bucket[g].append(statistics.mean(scores))
        by_grade = {g: (statistics.mean(v), len(v)) for g, v in bucket.items()}

    return {
        "per_item": per_item,
        "course_index": index_for("course"),
        "instructor_index": index_for("instructor"),
        "overall_mean": statistics.mean(all_likert) if all_likert else float("nan"),
        "demographics": demo,
        "by_grade": by_grade,
        "grade_q": grade_q,
    }


# --------------------------------------------------------------------------- #
# Qualitative analysis                                                         #
# --------------------------------------------------------------------------- #

_COMPILED_THEMES = {name: [re.compile(p, re.I) for p in pats] for name, pats in THEMES.items()}


def tag_themes(comment: str) -> list[str]:
    return [name for name, pats in _COMPILED_THEMES.items()
            if any(p.search(comment) for p in pats)]


def sentiment(comment: str) -> tuple[float, int, int]:
    words = re.findall(r"[a-z']+", comment.lower())
    pos = sum(w in POSITIVE_WORDS for w in words)
    neg = sum(w in NEGATIVE_WORDS for w in words)
    score = (pos - neg) / (pos + neg) if (pos + neg) else 0.0
    return score, pos, neg


def analyze_qual(survey: Survey) -> dict:
    out = {}
    for q in survey.free_text_qnums:
        comments = []
        for i, r in enumerate(survey.respondents):
            text = r["free_text"].get(q)
            if not text:
                continue
            s, pos, neg = sentiment(text)
            comments.append({
                "respondent": i + 1,
                "text": text,
                "themes": tag_themes(text),
                "sentiment": s,
                "words": len(text.split()),
            })
        theme_counts = Counter(t for c in comments for t in c["themes"])
        out[q] = {
            "text": survey.questions[q]["text"],
            "comments": comments,
            "n_comments": len(comments),
            "theme_counts": theme_counts,
        }
    return out


# --------------------------------------------------------------------------- #
# Optional LLM narrative                                                       #
# --------------------------------------------------------------------------- #

LLM_MODEL = "claude-opus-4-8"


def llm_synthesis(survey: Survey, qual: dict, model: str) -> str | None:
    try:
        from anthropic import Anthropic
    except Exception:
        print("  [--llm] anthropic package not installed; skipping LLM synthesis.")
        return None
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("  [--llm] ANTHROPIC_API_KEY not set; skipping LLM synthesis.")
        return None

    blocks = []
    for q in survey.free_text_qnums:
        blocks.append(f"### Prompt: {qual[q]['text']}")
        for c in qual[q]["comments"]:
            blocks.append(f"- {c['text']}")
    prompt = (
        "You are helping a university instructor read their anonymous end-of-term "
        "course evaluations. Below are the verbatim free-text comments. Write a "
        "concise, candid synthesis (Markdown, ~400 words) with three parts: "
        "(1) **What students valued most** — the strongest recurring positives; "
        "(2) **What to improve** — the most actionable, highest-leverage suggestions, "
        "ranked; (3) **One thing I'd prioritize next term** — a single concrete "
        "recommendation. Be specific and quote sparingly. Do not invent themes that "
        "aren't in the comments.\n\n" + "\n".join(blocks)
    )
    try:
        client = Anthropic()
        msg = client.messages.create(
            model=model, max_tokens=1500,
            messages=[{"role": "user", "content": prompt}],
        )
        return "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")
    except Exception as e:  # pragma: no cover
        print(f"  [--llm] API call failed ({e}); skipping LLM synthesis.")
        return None


# --------------------------------------------------------------------------- #
# Charts                                                                       #
# --------------------------------------------------------------------------- #

def make_charts(survey: Survey, quant: dict, qual: dict, assets: Path) -> dict:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        print("  matplotlib not available; skipping charts.")
        return {}
    assets.mkdir(parents=True, exist_ok=True)
    plt.rcParams["figure.figsize"] = (10, 6)
    charts = {}

    # 1) item means
    likert_q = sorted(quant["per_item"])
    labels = [f"Q{q}" for q in likert_q]
    means = [quant["per_item"][q]["mean"] for q in likert_q]
    colors = ["#2c7fb8" if survey.questions[q]["kind"] == "course" else "#d95f0e"
              for q in likert_q]
    fig, ax = plt.subplots()
    ax.barh(labels, means, color=colors)
    ax.set_xlim(1, LIKERT_MAX)
    ax.axvline(LIKERT_MIDPOINT, color="grey", ls="--", lw=1)
    for i, m in enumerate(means):
        ax.text(m + 0.03, i, f"{m:.2f}", va="center", fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel(f"Mean rating (1-{LIKERT_MAX})")
    ax.set_title("Item means — blue = course, orange = instructor")
    fig.tight_layout()
    p = assets / "item_means.png"
    fig.savefig(p, dpi=130); plt.close(fig)
    charts["item_means"] = p.name

    # 2) Likert distribution (stacked)
    fig, ax = plt.subplots()
    palette = {1: "#d7191c", 2: "#fdae61", 3: "#ffffbf", 4: "#a6d96a", 5: "#1a9641"}
    left = [0] * len(likert_q)
    for score in range(1, LIKERT_MAX + 1):
        vals = [quant["per_item"][q]["dist"][score] for q in likert_q]
        ax.barh(labels, vals, left=left, color=palette[score],
                label={1: "Strongly Disagree", 2: "Disagree", 3: "Neutral",
                       4: "Agree", 5: "Strongly Agree"}[score])
        left = [a + b for a, b in zip(left, vals)]
    ax.invert_yaxis()
    ax.set_xlabel("Number of respondents")
    ax.set_title("Response distribution per item")
    ax.legend(ncol=5, fontsize=7, loc="upper center", bbox_to_anchor=(0.5, -0.08))
    fig.tight_layout()
    p = assets / "likert_distribution.png"
    fig.savefig(p, dpi=130); plt.close(fig)
    charts["likert_distribution"] = p.name

    # 3) demographics (expected grade + class standing if present)
    demo_items = list(quant["demographics"].items())[:2]
    if demo_items:
        fig, axes = plt.subplots(1, len(demo_items), figsize=(12, 5))
        if len(demo_items) == 1:
            axes = [axes]
        for ax, (q, d) in zip(axes, demo_items):
            items = d["counts"].most_common()
            ax.bar([k for k, _ in items], [v for _, v in items], color="#2c7fb8")
            ax.set_title(d["text"][:40])
            ax.tick_params(axis="x", rotation=30, labelsize=8)
        fig.tight_layout()
        p = assets / "demographics.png"
        fig.savefig(p, dpi=130); plt.close(fig)
        charts["demographics"] = p.name

    # 4) theme frequency across all comments
    all_themes = Counter()
    for q in qual:
        all_themes.update(qual[q]["theme_counts"])
    if all_themes:
        fig, ax = plt.subplots()
        items = all_themes.most_common()
        ax.barh([k for k, _ in items][::-1], [v for _, v in items][::-1], color="#756bb1")
        ax.set_xlabel("Comments mentioning theme")
        ax.set_title("Qualitative theme frequency (all comments)")
        fig.tight_layout()
        p = assets / "themes.png"
        fig.savefig(p, dpi=130); plt.close(fig)
        charts["themes"] = p.name

    return charts


# --------------------------------------------------------------------------- #
# Report rendering                                                             #
# --------------------------------------------------------------------------- #

def _fav_word(pct: float) -> str:
    return f"{pct:.0f}%"


def render_report(survey: Survey, quant: dict, qual: dict, charts: dict,
                  llm_text: str | None, term: str) -> str:
    L: list[str] = []
    add = L.append

    add(f"# Course Evaluation Report — {survey.course or 'Course'}")
    add("")
    add(f"**Instructor:** {survey.instructor or 'N/A'}  ")
    if survey.period:
        add(f"**Evaluation period:** {survey.period}  ")
    add(f"**Term folder:** `{term}`  ")
    if survey.response_rate is not None:
        add(f"**Response rate:** {survey.n_responses}/{survey.n_enrolled} "
            f"({survey.response_rate:.1f}%)  ")
    add(f"**Respondents analyzed:** {survey.n_responses}  ")
    add("")
    add("> Generated by `scripts/analyze_course_eval.py`. Quantitative results are "
        "computed from the per-respondent export; qualitative themes are rule-based "
        "tags over the verbatim comments. This report stays in the (gitignored) "
        "evaluation folder — it is not published.")
    add("")
    add("---")
    add("")

    # ---- Executive summary ------------------------------------------------- #
    ci, ii = quant["course_index"], quant["instructor_index"]
    per = quant["per_item"]
    likert_q = sorted(per)
    strongest = max(likert_q, key=lambda q: per[q]["mean"])
    weakest = min(likert_q, key=lambda q: per[q]["mean"])
    top_strength = None
    top_improve = None
    well_q = survey.free_text_qnums[0] if survey.free_text_qnums else None
    improve_q = survey.free_text_qnums[1] if len(survey.free_text_qnums) > 1 else None
    if well_q is not None and qual[well_q]["theme_counts"]:
        top_strength = qual[well_q]["theme_counts"].most_common(1)[0]
    if improve_q is not None and qual[improve_q]["theme_counts"]:
        top_improve = qual[improve_q]["theme_counts"].most_common(1)[0]

    add("## Executive summary")
    add("")
    add(f"- **Overall mean rating:** **{quant['overall_mean']:.2f} / {LIKERT_MAX}** "
        f"across {len(likert_q)} Likert items.")
    add(f"- **Course items** (organization, assignments, projects, exams): mean "
        f"**{ci['mean_of_items']:.2f}**, {_fav_word(ci['pct_favorable'])} favorable "
        f"(Agree / Strongly Agree).")
    add(f"- **Instructor items** (communication, responsiveness, care, fairness, "
        f"inclusion): mean **{ii['mean_of_items']:.2f}**, "
        f"{_fav_word(ii['pct_favorable'])} favorable.")
    add(f"- **Strongest item:** Q{strongest} — *{survey.questions[strongest]['text']}* "
        f"(mean {per[strongest]['mean']:.2f}).")
    add(f"- **Lowest item:** Q{weakest} — *{survey.questions[weakest]['text']}* "
        f"(mean {per[weakest]['mean']:.2f}). Relatively lowest, not necessarily weak.")
    if top_strength:
        add(f"- **Most-praised theme:** {top_strength[0]} "
            f"({top_strength[1]} comments).")
    if top_improve:
        add(f"- **Top improvement request:** {top_improve[0]} "
            f"({top_improve[1]} comments).")
    add("")
    add("---")
    add("")

    # ---- Charts ------------------------------------------------------------ #
    if charts:
        add("## At a glance")
        add("")
        if "item_means" in charts:
            add(f"![Item means](report_assets/{charts['item_means']})")
            add("")
        if "likert_distribution" in charts:
            add(f"![Likert distribution](report_assets/{charts['likert_distribution']})")
            add("")
        add("---")
        add("")

    # ---- Quantitative tables ---------------------------------------------- #
    def item_table(kind: str, heading: str, blurb: str):
        qs = [q for q in likert_q if survey.questions[q]["kind"] == kind]
        if not qs:
            return
        add(f"## {heading}")
        add("")
        add(blurb)
        add("")
        add("| # | Item | Mean | SD | % Favorable | % Top box |")
        add("|---|------|------|----|-------------|-----------|")
        for q in qs:
            s = per[q]
            add(f"| {q} | {survey.questions[q]['text']} | {s['mean']:.2f} | "
                f"{s['sd']:.2f} | {s['pct_favorable']:.0f}% | {s['pct_top_box']:.0f}% |")
        idx = quant["course_index"] if kind == "course" else quant["instructor_index"]
        add(f"| | **Index (mean of items)** | **{idx['mean_of_items']:.2f}** | | "
            f"**{idx['pct_favorable']:.0f}%** | |")
        add("")

    item_table("course", "Course performance",
               "Closed-form items about the course design — organization, "
               "assignments, projects, and exams. *% Favorable* = Agree or "
               "Strongly Agree; *% Top box* = Strongly Agree.")
    item_table("instructor", "Instructor performance",
               "Closed-form items about the instructor — communication, "
               "responsiveness, care for learning, fairness, and inclusion.")

    # ---- Distribution detail ---------------------------------------------- #
    add("## Response distribution (per item)")
    add("")
    add("| # | Item | SD↓1 | D↓2 | N·3 | A·4 | SA·5 |")
    add("|---|------|----|----|----|----|----|")
    for q in likert_q:
        d = per[q]["dist"]
        add(f"| {q} | {survey.questions[q]['text']} | {d[1]} | {d[2]} | {d[3]} | "
            f"{d[4]} | {d[5]} |")
    add("")
    add("*Scale: 1 = Strongly Disagree, 2 = Disagree, 3 = Neither, 4 = Agree, "
        "5 = Strongly Agree.*")
    add("")
    add("---")
    add("")

    # ---- Respondent profile ----------------------------------------------- #
    add("## Respondent profile")
    add("")
    if "demographics" in charts:
        add(f"![Demographics](report_assets/{charts['demographics']})")
        add("")
    for q, d in quant["demographics"].items():
        add(f"**{d['text']}** (n={d['n']})  ")
        parts = [f"{label}: {cnt} ({100*cnt/d['n']:.0f}%)"
                 for label, cnt in d["counts"].most_common()]
        add("- " + "; ".join(parts))
        add("")
    if quant["by_grade"]:
        add("**Mean overall rating by expected grade** (exploratory — small cells):  ")
        add("")
        add("| Expected grade | Mean overall rating | n |")
        add("|---|---|---|")
        for g, (m, n) in sorted(quant["by_grade"].items(), key=lambda x: -x[1][0]):
            add(f"| {g} | {m:.2f} | {n} |")
        add("")
    add("---")
    add("")

    # ---- Qualitative ------------------------------------------------------- #
    add("## Qualitative analysis")
    add("")
    if "themes" in charts:
        add(f"![Theme frequency](report_assets/{charts['themes']})")
        add("")

    labels_for_q = {}
    if survey.free_text_qnums:
        labels_for_q[survey.free_text_qnums[0]] = "What students say the instructor does well"
    if len(survey.free_text_qnums) > 1:
        labels_for_q[survey.free_text_qnums[1]] = "Suggestions for improvement"

    for q in survey.free_text_qnums:
        head = labels_for_q.get(q, f"Open-text question {q}")
        block = qual[q]
        add(f"### {head}")
        add("")
        add(f"*Prompt (Q{q}):* {block['text']}  ")
        add(f"*{block['n_comments']} of {survey.n_responses} respondents commented.*")
        add("")
        if block["theme_counts"]:
            add("**Themes mentioned:**  ")
            add("")
            add("| Theme | Comments |")
            add("|---|---|")
            for theme, cnt in block["theme_counts"].most_common():
                add(f"| {theme} | {cnt} |")
            add("")
        # comments grouped by their dominant (most common across this question) theme
        add("**Verbatim comments**")
        add("")
        ordered_themes = [t for t, _ in block["theme_counts"].most_common()]
        printed = set()
        for theme in ordered_themes:
            members = [c for c in block["comments"]
                       if theme in c["themes"] and c["respondent"] not in printed]
            if not members:
                continue
            add(f"*{theme}:*")
            for c in members:
                printed.add(c["respondent"])
                add(f"> {c['text']}")
                add("")
        leftover = [c for c in block["comments"] if c["respondent"] not in printed]
        if leftover:
            add("*Other:*")
            for c in leftover:
                add(f"> {c['text']}")
                add("")
        add("---")
        add("")

    # ---- Synthesis --------------------------------------------------------- #
    add("## Synthesis — keep / improve")
    add("")
    if well_q is not None and qual[well_q]["theme_counts"]:
        add("**Strengths to keep doing** (by how often students named them):")
        for theme, cnt in qual[well_q]["theme_counts"].most_common(5):
            add(f"- **{theme}** — {cnt} mention(s)")
        add("")
    if improve_q is not None and qual[improve_q]["theme_counts"]:
        add("**Priority improvements** (by how often students raised them):")
        for theme, cnt in qual[improve_q]["theme_counts"].most_common(6):
            add(f"- **{theme}** — {cnt} mention(s)")
        add("")

    if llm_text:
        add("### Narrative synthesis (Claude)")
        add("")
        add(llm_text.strip())
        add("")

    add("---")
    add("")
    add("## Methodology & provenance")
    add("")
    add(f"- **Source (qualitative + quantitative):** the per-respondent export "
        f"({survey.n_responses} respondent pages).")
    if survey.response_rate is not None:
        add(f"- **Response rate** read from the aggregate summary export: "
            f"{survey.n_responses}/{survey.n_enrolled} ({survey.response_rate:.1f}%).")
    add(f"- **Likert scale:** 1 (Strongly Disagree) – {LIKERT_MAX} (Strongly Agree). "
        f"*Favorable* = 4–5; *Top box* = 5.")
    add("- **Themes** are rule-based keyword tags; a comment can carry several. "
        "Counts indicate how many comments touched a theme, not intensity.")
    add("- Free-text glyph fixes (apostrophes, dashes) applied during extraction; "
        "wording is otherwise verbatim, including students' original spelling.")
    add("")
    return "\n".join(L)


# --------------------------------------------------------------------------- #
# CSV export                                                                   #
# --------------------------------------------------------------------------- #

def write_csv(survey: Survey, path: Path) -> None:
    demo_qs = [q for q, m in sorted(survey.questions.items()) if m["kind"] == "demographic"]
    likert_qs = [q for q, m in sorted(survey.questions.items())
                 if m["kind"] in ("course", "instructor")]
    ft_qs = survey.free_text_qnums
    header = (["respondent"]
              + [f"Q{q}_demo" for q in demo_qs]
              + [f"Q{q}_likert" for q in likert_qs]
              + [f"Q{q}_text" for q in ft_qs])
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        for i, r in enumerate(survey.respondents, 1):
            row = ([i]
                   + [r["demographics"].get(q, "") for q in demo_qs]
                   + [r["likert"].get(q, "") for q in likert_qs]
                   + [r["free_text"].get(q, "") for q in ft_qs])
            w.writerow(row)


# --------------------------------------------------------------------------- #
# PDF discovery                                                                #
# --------------------------------------------------------------------------- #

def find_pdfs(folder: Path) -> tuple[Path, list[Path]]:
    pdfs = sorted(folder.glob("*.pdf"))
    if not pdfs:
        sys.exit(f"ERROR: no PDF files in {folder}")
    # respondent file = most pages (explicit 'Response-' name wins ties)
    def page_count(p: Path) -> int:
        try:
            out = subprocess.run(["pdfinfo", str(p)], capture_output=True, text=True)
            m = re.search(r"Pages:\s*(\d+)", out.stdout)
            return int(m.group(1)) if m else 0
        except Exception:
            return 0
    ranked = sorted(pdfs, key=lambda p: (p.name.lower().startswith("response"),
                                         page_count(p)), reverse=True)
    respondent_pdf = ranked[0]
    summaries = [p for p in pdfs if p != respondent_pdf]
    return respondent_pdf, summaries


def default_folder(repo_root: Path) -> Path:
    base = repo_root / "_adm_stuff" / "_course_eval"
    if base.is_dir():
        terms = sorted([d for d in base.iterdir() if d.is_dir()])
        if terms:
            return terms[-1]
    sys.exit("ERROR: no folder given and none found under _adm_stuff/_course_eval/.")


# --------------------------------------------------------------------------- #
# Main                                                                         #
# --------------------------------------------------------------------------- #

def main() -> None:
    ap = argparse.ArgumentParser(description="Analyze anonymous course-evaluation PDFs.")
    ap.add_argument("folder", nargs="?", help="Folder containing the evaluation PDFs.")
    ap.add_argument("--term", help="Term label for output filenames (default: folder name).")
    ap.add_argument("--no-charts", action="store_true", help="Skip PNG charts.")
    ap.add_argument("--no-csv", action="store_true", help="Skip the tidy CSV export.")
    ap.add_argument("--llm", action="store_true",
                    help="Add a Claude-API narrative synthesis (needs ANTHROPIC_API_KEY).")
    ap.add_argument("--llm-model", default=LLM_MODEL, help=f"LLM model (default {LLM_MODEL}).")
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    folder = Path(args.folder).resolve() if args.folder else default_folder(repo_root)
    if not folder.is_dir():
        sys.exit(f"ERROR: not a folder: {folder}")
    term = args.term or folder.name

    print(f"Folder: {folder}")
    respondent_pdf, summaries = find_pdfs(folder)
    print(f"Per-respondent PDF: {respondent_pdf.name}")
    if summaries:
        print(f"Summary PDFs: {', '.join(p.name for p in summaries)}")

    survey = Survey()
    resp_text = pdf_to_text(respondent_pdf)
    detect_header(resp_text, survey)
    parse_respondent_pdf(resp_text, survey)
    parse_response_rate([pdf_to_text(p) for p in summaries], survey)

    if not survey.respondents:
        sys.exit("ERROR: parsed 0 respondents — check the PDF format.")
    print(f"Parsed {survey.n_responses} respondents, "
          f"{len([q for q,m in survey.questions.items() if m['kind'] in ('course','instructor')])} "
          f"Likert items, {len(survey.free_text_qnums)} open-text questions.")

    quant = compute_quant(survey)
    qual = analyze_qual(survey)

    charts = {}
    if not args.no_charts:
        charts = make_charts(survey, quant, qual, folder / "report_assets")

    llm_text = None
    if args.llm:
        print("  Requesting LLM narrative synthesis...")
        llm_text = llm_synthesis(survey, qual, args.llm_model)

    report = render_report(survey, quant, qual, charts, llm_text, term)
    report_path = folder / f"course_eval_report_{term}.md"
    report_path.write_text(report, encoding="utf-8")
    print(f"Report written: {report_path}")

    if not args.no_csv:
        csv_path = folder / f"course_eval_responses_{term}.csv"
        write_csv(survey, csv_path)
        print(f"CSV written: {csv_path}")


if __name__ == "__main__":
    main()
