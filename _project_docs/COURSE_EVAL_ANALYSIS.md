# Course Evaluation Analysis

End-of-term workflow: turn the official **anonymous course-evaluation PDFs**
into one readable performance report — quantitative *and* qualitative — for the
instructor. This is a **recurring, every-course task**: the tool is
course-agnostic and ships in every course seed via `scripts/make_seed.sh`.

**Tool:** `scripts/analyze_course_eval.py`

---

## When to run

After Purdue/DSB releases the end-of-term evaluations (you receive a bundle of
PDFs right after submitting grades). Save them to
`_adm_stuff/_course_eval/<Term>/` (e.g. `_adm_stuff/_course_eval/2026Summer/`),
then run the tool.

## The input bundle

The export is several PDFs. Two kinds matter; the tool auto-detects both:

| Kind | How to spot it | Used for |
|---|---|---|
| **Per-respondent** | Filename usually starts with `Response-`; **most pages** (one page per student). | Everything — closed-form answers *and* the free-text comments. The report is built from this file. |
| **Aggregate summary** | Frequency tables; few pages. | Only to recover the official `Response Rate: N/M (xx%)` line, which the per-respondent file omits. Optional. |

The tool picks the per-respondent file as the one whose name starts with
`response` and/or has the most pages. **Focus on that file** — it is the only
one with the qualitative responses.

## Run it

```bash
# Analyze a specific term folder
python3 scripts/analyze_course_eval.py _adm_stuff/_course_eval/2026Summer

# Auto-pick the latest term folder under _adm_stuff/_course_eval/
python3 scripts/analyze_course_eval.py

# Add a Claude-API narrative synthesis (needs ANTHROPIC_API_KEY + `pip install anthropic`)
python3 scripts/analyze_course_eval.py _adm_stuff/_course_eval/2026Summer --llm

# Skip charts (no matplotlib) or the CSV export
python3 scripts/analyze_course_eval.py <folder> --no-charts --no-csv
```

## What it produces

All written **into the same (gitignored) folder** as the PDFs — student data is
private and never published:

| Output | Contents |
|---|---|
| `course_eval_report_<Term>.md` | The report: executive summary, course-performance table, instructor-performance table, per-item Likert distributions, respondent profile (demographics + mean rating by expected grade), qualitative themes with **every verbatim comment grouped by theme**, and a keep/improve synthesis. |
| `report_assets/*.png` | Charts embedded in the report — item means (course vs instructor), Likert distribution, demographics, theme frequency. |
| `course_eval_responses_<Term>.csv` | One tidy row per respondent (demographics + Likert scores + free-text) for any further analysis. |

## How the analysis works

- **Quantitative.** Closed items are split into *course* items (organization,
  assignments, projects, exams) and *instructor* items (the ones whose text
  contains "instructor": communication, responsiveness, care, fairness,
  inclusion). Per item: mean, SD, median, full 1–5 distribution, % favorable
  (Agree + Strongly Agree), % top-box (Strongly Agree). Verified to reproduce
  the official summary PDF's Mean/SD exactly.
- **Qualitative.** A theme taxonomy + sentiment lexicon (top of the script,
  editable) tag every free-text comment; themes are ranked by frequency and
  representative quotes pulled per theme. Rule-based by default (offline,
  deterministic). `--llm` adds a narrative synthesis via the Claude API and
  degrades gracefully if the package/key is missing. Comments are reproduced
  verbatim (only glyph fixes — apostrophes, dashes — are applied), including
  students' original spelling.

## Reusing in a new course

Nothing to change. `scripts/analyze_course_eval.py` hardcodes no course, term,
or instructor — all auto-detected from the PDF header. `make_seed.sh` copies
`scripts/` into every new course (and excludes `_adm_stuff/`, so no old eval
data tags along). Just drop the new term's PDFs into
`_adm_stuff/_course_eval/<Term>/` and run.

## Requirements

- `pdftotext` (poppler): `brew install poppler` / `apt install poppler-utils`.
  Pure-Python fallbacks `pdfplumber` / `pymupdf` are used if installed instead.
- `matplotlib` for charts (`--no-charts` skips it). pandas is used if present,
  not required. `anthropic` only for `--llm`.
