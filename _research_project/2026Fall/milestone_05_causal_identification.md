# Course milestone M5 — Data and Measurement Governance

<!-- book-milestone-bridge:begin -->
> **Book Milestone bridge (D41)** — course milestone **M5**.
> This submission presents **Book Milestone 6 — Your data and measurement, governed** (version 1): work from its [milestone page](https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464/book/studios/milestone06-govern-data-measurement.html#milestone).
> *(D41 rebuild note: this brief's artifact spec is being rebuilt to the Studio structure and is updated before its kickoff.)*
<!-- book-milestone-bridge:end -->

## About the Research Project

Your semester project is **individual**: one researcher, one question, carried
from curiosity to a defended, reproducible claim. It runs through milestones
**M0–M15**, peaks publicly at the **Purdue Fall Undergraduate Research Expo
poster session (Tuesday, November 17 — required)**, and closes with an oral
**Evidence Defense** and a final research chapter in December. Every milestone
follows the same cadence: **Friday-studio kickoff → develop across the week →
submit → revise (where eligible)**. Every milestone also updates your
cumulative **Research Project Dossier** and appends at least one row to your
**AI Research Ledger** — the running record of what you handed to AI and how you
checked it. Milestone weights live in the syllabus;
instructions and rubrics live one page per milestone, like this one.

---

## What to Submit on Brightspace

Due: **Friday, October 2, 11:59 PM** (you work on it at that Friday's studio).

| # | File | Description |
|---|---|---|
| 1 | **`lastname_m05_data_governance.pdf`** *or* a shared Colab notebook link | The six parts below: your acquisition and provenance record with the permission recheck, your measurement plan (the concept → construct → indicator table with its reliability and validity case), your column minimization with the re-identification check, the Contract revision that settles your operationalization, your AI Research Ledger rows, and your dossier update line. This is the graded artifact. |
| 2 | **EDR\|AI "It is your turn" — ch. 19, ch. 20** | The completed "It is your turn" sections of this milestone's book chapters, worked in their companion Colab notebooks (share the links) or included in your artifact. See "The Book Anchor" below. |

If you submit a notebook link, make sure sharing is set so the instructor can
open it, and that the provenance and measurement tables render when the
notebook is run.

---

## The Book Anchor — "It Is Your Turn"

This milestone is anchored in the course book, **EDR\|AI**. Read the chapters
below as you develop the milestone, and complete each chapter's closing **"It
is your turn"** section in its companion Colab notebook (or carry the same
work inside your project notebook):

- Ch. 19 — [Data Provenance and Data Quality](https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464/book/part4-credible-evidence/17-data-provenance-and-data-quality.html) · [companion notebook](https://colab.research.google.com/github/davi-moreira/2026F_evidence_driven_research_purdue_HONR464/blob/main/notebooks/book/ch17_data_provenance_and_data_quality.ipynb)
- Ch. 20 — [Measurement and Operationalization](https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464/book/part4-credible-evidence/18-measurement-and-operationalization.html) · [companion notebook](https://colab.research.google.com/github/davi-moreira/2026F_evidence_driven_research_purdue_HONR464/blob/main/notebooks/book/ch18_measurement_and_operationalization.ipynb)

These sections are the point of the reading, not extra work: across the
semester, the book's "It is your turn" sections — one per lesson, collected by the twelve Book Milestones — chain into your final
research chapter, so what you complete here is a draft piece of your final
artifact. Include the completed sections in this milestone's submission (see
the submission table above) and carry them forward in your Research Project
Dossier.

---

## Purpose

Last week you declared your pathway. This week you govern what it runs on.
**Data and measurement governance** is written control over your evidence's
raw material: where every dataset comes from, what you are permitted to do
with it, and whether each measure captures the concept you claim it does.
Results inherit the quality of the data and the measures beneath them, and no
later check can repair what goes wrong here. The work is deliberately
unglamorous. It is also where more projects quietly fail than anywhere else
in the course.

Governance starts before the first column, with the question no earlier week
settled: how do data actually reach you? You answer it in writing, as an
**acquisition route** — the declared path by which your data come to exist,
decided by your M3 permission status. Cleared means you name your frame and
plan for the units you cannot reach. Pending means you build and wait without
touching people. No permission means aggregates, open data, or simulation,
with the cost stated. Then every source gets **provenance**, the documented
origin of a dataset: who produced it, how, when, and under what terms.
"Downloaded from the county election office's results portal, open-data
licence, October 1" is provenance; "found a CSV online" is not.

The second half settles what M3 deliberately left provisional: your
**operationalization**, the exact path from each concept you care about to
the indicator you actually record. You climb the concept → construct →
indicator ladder for every measured concept. You check **reliability**,
whether your instrument reads consistently, on its items. You argue
**validity**, whether your scores support the interpretation you put on them,
as a property of interpretation and use rather than a stamp on the
instrument. And because a changed measure changes what your estimand refers
to, the settled operationalization ships as a new Contract version.

> **A question that often comes up here:** *"My data have not arrived yet, or
> I have no permission to collect any. How do I govern data I do not have?"*
> You govern the route your permission status assigns. Pending means you
> pilot the instrument on yourself and write your analysis code against
> simulated data of the shape you expect, while you wait. No authority to ask
> means the no-permission route, which reaches every method in this course:
> published aggregate statistics, an openly licensed dataset with no
> individual records, or data you simulate yourself. Write down which you
> chose and what it costs you. A simulated dataset can demonstrate a method,
> but it cannot support a claim about the world.

## Components

Choosing measures and judging data quality is a never-delegate decision. Your
AI assistant can hunt licences, draft tables, and attack your privacy check,
but whether a measure measures your concept is a judgment you own. One trap
governs the whole week: an assistant can describe a dataset it has never
seen, fluently and wrongly, so every AI claim about your data is verified
against the file itself.

### 1. The acquisition and provenance record

Settle acquisition first, in writing, before anything below it.

- **The route, declared.** Which of the three routes your M3 permission
  status assigns, and why. **Cleared** (or formal determination granted):
  name your sampling frame, how you will reach those units, and what you
  will do about the ones you cannot reach; non-response is a design fact,
  not an accident. **Pending**: do everything that does not touch people —
  build and pilot the instrument on yourself, write the analysis code
  against simulated data of the expected shape, and wait. **No authority to
  ask, or not authorized**: take the no-permission route and state its cost.
- **Provenance for every source.** One entry per dataset and per borrowed
  number: who produced it, how, when, and under what terms — the licence or
  terms of use, named, not assumed. Open and read the primary source behind
  your headline claim, not a summary of it.
- **The permission recheck.** Hold your M3 determination against the data as
  they actually arrived, not as you planned them. Data that arrive
  differently from the plan can carry permissions the plan did not cover.
  Declare one outcome: still cleared, or what changed and what you did
  about it.

### 2. The measurement plan

Climb the **concept → construct → indicator** ladder for every concept your
analysis measures, one table row each.

- **The ladder itself.** Concept (the abstract idea), construct (the
  specific, targetable version of it), indicator (the concrete thing you
  record). Each rung must visibly narrow the one above it, and the **gap**
  between construct and indicator is named, not smoothed over.
- **A meaning sentence per number.** For each indicator, one sentence saying
  what a single recorded value actually asserts (for example, *"a 4 on this
  item asserts that this respondent, on this day, placed their floor
  community at 4 of 5 on belonging"*). If you cannot write the sentence, you
  do not yet know what your number means.
- **Reliability, checked on items.** **Reliability** is whether your
  instrument reads consistently. Check it on the instrument's items —
  agreement among the items of a scale, or repeated readings of the same
  unit — never by splitting your respondents into halves and comparing
  group summaries, which measures sampling, not your instrument. Plan one
  reliability check you can actually run on the evidence you have.
- **Validity, argued as interpretation and use.** **Validity** is whether
  your scores support the interpretation you put on them, for the use you
  put them to. It is not a stamp the instrument carries. State the
  interpretation, state the use, and name where the construct–indicator gap
  could break them.

### 3. Column minimization and the re-identification check

Govern what you keep, not just what you gather.

- **Minimize against the declared analysis.** **Data minimization** means
  keeping only the columns your declared analysis needs. Hold every column
  in your dataset against the analysis your Contract declares; a column
  with no analysis behind it is risk carried for nothing. Record what you
  dropped or coarsened.
- **Run the re-identification check.** A **re-identification check** asks
  whether someone could plausibly combine your kept columns to pick out an
  individual. A table with no names can still identify a person when a few
  columns intersect: hall, major, and hometown can be one student. Report
  the check's result and what you changed because of it.

### 4. The Contract revision

Your operationalization was provisional at M3 by design. It is provisional no
longer. Issue the settled measurement plan as a new, dated, numbered version
of your **Research Contract**, with a reason a reader could use to
reconstruct your thinking. Any measurement change is a Contract version,
because it changes what your estimand refers to. Two lines are mandatory in
the revision:

- **The measurement fields, settled.** The indicator, its meaning sentence,
  and the planned reliability check, written into the Contract.
- **Measurement error as uncertainty.** State measurement error alongside
  your sampling uncertainty, not instead of it. A perfectly computed
  interval around a poorly measured quantity is still a poorly measured
  quantity.

### 5. AI Research Ledger rows

Every use of AI in building this record gets a row in your **AI Research
Ledger** (the eight fixed fields: task delegated · tool used · prompt ·
output summary · decision · verification method · remaining concern ·
responsible researcher). Hunting a licence, drafting the provenance table,
proposing indicator wordings, and red-teaming your re-identification check
are all delegable tasks, and each one you delegated needs a row naming how
you verified the result against the actual file or page. "No AI used" is a
legitimate entry if it is true.

**A missing ledger is not a minor lapse.** Per the course rule, a missing AI
Research Ledger entry scores the Craft criterion **0** and the submission is
**returned** for completion before it is graded.

### 6. Dossier update line

End with one line recording what this milestone finalizes in your **Research
Project Dossier**: your **data and measurement documentation** component now
exists — acquisition route, provenance record, measurement specification,
permission recheck, and the settled Contract revision. Name the file or
section in your dossier where each now lives.

---

## Definition of Done

You are done when your submission carries all of the following. Use this as a
pre-submission checklist.

| Item | Specification |
|---|---|
| **Acquisition route** | One of the three routes declared in writing (cleared / pending / no permission), with its reason and, where it applies, its stated cost |
| **Provenance record** | One entry per dataset and borrowed number: who produced it, how, when, under what terms; the primary source behind your headline claim opened and read |
| **Permission recheck** | The M3 determination held against the data as they actually arrived; one declared outcome |
| **Measurement ladder** | Concept → construct → indicator for every measured concept; each rung narrows; the construct–indicator gap named |
| **Meaning sentences** | One per indicator, saying what a single recorded value asserts |
| **Reliability & validity** | One reliability check planned on items, never on split respondents; validity argued as interpretation and use |
| **Minimization & re-identification** | Every kept column tied to the declared analysis; the re-identification check run and its result reported |
| **Contract revision** | The operationalization settled and issued as a dated, numbered Contract version with a usable reason; measurement error stated alongside sampling uncertainty |
| **AI Research Ledger** | One row per AI-assisted step; every verification method named and non-vague |
| **Dossier line** | The data and measurement documentation component located by file or section |
| **Studio work** | Worked at the Friday studio with your AI assistant |
| **Filename** | `lastname_m05_data_governance.pdf` (or a shared Colab link) |
| **Location** | Brightspace → Assignments → M05 |

---

## Grading Rubric (100 points)

Four bands on the course's five shared virtues
(`planning/ASSESSMENT_ARCHITECTURE.md`).

| Criterion | Exemplary | Proficient | Developing | Beginning |
|---|---|---|---|---|
| **Governance correctness (provenance & measurement)** (30) | Acquisition route settled in writing; provenance complete for every source with its terms named; the measurement ladder narrows at every rung; reliability planned on items; validity argued as interpretation and use; minimization tied to the declared analysis and the re-identification check run (26–30) | All parts present; one rung, one source's terms, or one check thin (21–25) | A governance piece missing or malformed: reliability by respondent-splitting, columns kept with no analysis behind them, or provenance that stops at a link (13–20) | No acquisition route declared, or a measurement plan that never descends below the concept (0–12) |
| **Evidence integrity & provenance** (20) | Every dataset, licence, and borrowed number is real and retrievable; the primary source behind your headline claim was opened and read; a reader can trace each entry to its origin (18–20) | Real and traceable; one provenance entry thin (14–17) | A dataset, licence, or number asserted without a locatable source (8–13) | A cited dataset, licence, or source that does not exist or does not say what you claim (0–7) |
| **Verification of AI-assisted parts** (20) | Every AI claim about your data verified against the file itself; every ledger row's verification method named and non-vague (18–20) | Ledger present; one verification method vague or one step unlogged (14–17) | Ledger thin; AI outputs used but the against-the-file check not named (8–13) | An AI description of your dataset, or an AI-asserted licence, pasted in and never checked against the file (0–7) |
| **Uncertainty & measurement error** (20) | Measurement error stated alongside sampling uncertainty; the construct–indicator gap named with what it could cost the claim; the Contract revision versioned with a usable reason (18–20) | Error and gap present; one stated loosely, or the version reason thin (14–17) | Measurement error mentioned but not connected to the claim, or the gap declared closed by assertion (8–13) | No measurement-error statement, or a revision with no version and no reason (0–7) |
| **Craft, ledger & communication** (10) | On-format, on-time; tables complete and readable; complete AI Research Ledger; dossier line present (9–10) | Minor format lapses; ledger complete (7–8) | Missing pieces or a rushed record (4–6) | Missing AI Research Ledger (Craft scored 0, submission returned) (0–3) |

**Hard caps (a single failure caps the row regardless of the rest):**

- A **fabricated or unretrievable source** — a dataset, licence, or number
  that does not exist or does not say what you claim — caps *Evidence
  integrity & provenance* at Beginning.
- An **unchecked AI description** — any claim about your data taken from an
  assistant and never verified against the file — caps *Verification of
  AI-assisted parts* at Beginning.
- A **missing AI Research Ledger entry** scores *Craft, ledger &
  communication* **0** and the submission is **returned** unread until it is
  supplied.

**Blocking gate:** no work at or after M3 proceeds past a **not-authorized**
permission determination. A record that does is returned ungraded until the
determination is resolved; this is a gate, not a deduction.

**Revision:** eligible under the standing policy — a revised submission within 7
days of feedback recovers up to half the lost points.

## Penalties

- Late: −10 points per day, up to 3 days; not accepted after (documented
  emergencies: talk to me first, per the syllabus).
- Any dataset, licence, or source you cite that turns out not to exist or not
  to say what you claim: *Evidence integrity & provenance* scores Beginning
  regardless of the rest — the course's evidence-integrity rule with teeth.
- Work that proceeds past a **not-authorized** permission determination is
  returned ungraded until the determination is resolved — the blocking gate,
  not a point deduction.
- Missing AI Research Ledger entry: *Craft* scores 0 and the submission is
  returned for completion before grading.

## Common Pitfalls

1. **The dataset described by an assistant that never saw it.** Asking AI
   what a dataset contains, what its licence allows, or how a variable is
   coded, and writing the answer down. An assistant can describe a dataset it
   has never seen, in confident detail. Open the file: count the rows, read
   the codebook, read the licence page. Then log how you checked.
2. **Reliability by splitting respondents.** Splitting your sample into
   halves, comparing the two groups' summaries, and calling the agreement
   reliability. That measures sampling variation, not your instrument.
   Reliability lives in the items: agreement among the items of a scale, or
   repeated readings of the same unit.
3. **The keep-everything table.** Keeping every column you managed to collect
   "just in case." Every kept column is a promise to protect it and a surface
   for re-identification, and a column with no declared analysis behind it
   buys you nothing. Minimize against the Contract, run the re-identification
   check, and record what you dropped.

---

*Previous: [M04 — Pathway Declaration and Mandated Contrast](milestone_04_observational_descriptive_audit.md) ·
Next: [M06 — First Executable Analysis + URC Abstract Internal Gate](milestone_06_experimental_measurement_protocol.md) —
your governed data and settled measures meet the code that executes your
declared analysis and produces your first result, with its uncertainty
attached.*
