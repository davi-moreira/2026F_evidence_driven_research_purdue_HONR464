# Course milestone M6 — Data and Measurement Governance

<!-- book-milestone-bridge:begin -->
> **Book Milestone bridge** — course milestone **M6**.
> This submission presents **Book Milestone 6 — Your data and measurement, governed** (version 1): work from its [milestone page](https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464/book/studios/milestone06-govern-data-measurement.html#milestone).
<!-- book-milestone-bridge:end -->

## About the Research Project

Your semester project is **individual**: one researcher, one question, carried
from curiosity to a defended, reproducible claim. It runs through milestones
**M1–M17**, peaks publicly at the **Purdue Fall Undergraduate Research Expo
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
This week's two lectures teach how data reach you and what your measures mean,
and Friday is their milestone. What you submit is one **governed-data record**:
provenance documentation, a data-management record, a permission recheck run
against your own acquisition route, and your measurement specification, with
the Contract version that settles the operationalization M4 left provisional.
The written document is what is graded.

| # | File | Description |
|---|---|---|
| 1 | **`lastname_m05_data_governance.pdf`** *or* a shared Colab notebook link | The seven parts below: your acquisition route and provenance record, your data-management record, the route-specific permission recheck, your measurement specification (concept → construct → indicator, with the reliability check's result and the validity argument), the Contract version that settles your operationalization, your AI Research Ledger rows, and your dossier update line. This is the graded artifact. |
| 2 | **EDR\|AI "It is your turn" — ch. 20, ch. 21** | The completed "It is your turn" sections of this milestone's book chapters, worked in their companion Colab notebooks (share the links) or included in your artifact. See "The Book Anchor" below. |

If you submit a notebook link, make sure sharing is set so the instructor can
open it, and that the provenance and measurement tables render when the
notebook is run.

---

## The Book Anchor — "It Is Your Turn"

This milestone is anchored in the course book, **EDR\|AI**. Read the chapters
below as you develop the milestone, and complete each chapter's closing **"It
is your turn"** section in its companion Colab notebook (or carry the same
work inside your project notebook):

- Ch. 20 — [Data Provenance and Data Quality](https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464/book/part4-credible-evidence/17-data-provenance-and-data-quality.html) · [companion notebook](https://colab.research.google.com/github/davi-moreira/2026F_evidence_driven_research_purdue_HONR464/blob/main/notebooks/book/ch17_data_provenance_and_data_quality.ipynb)
- Ch. 21 — [Measurement and Operationalization](https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464/book/part4-credible-evidence/18-measurement-and-operationalization.html) · [companion notebook](https://colab.research.google.com/github/davi-moreira/2026F_evidence_driven_research_purdue_HONR464/blob/main/notebooks/book/ch18_measurement_and_operationalization.ipynb)

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

What you hand in is one **governed-data record** with four pieces: provenance
documentation, a data-management record, a permission recheck run against your
own acquisition route, and your measurement specification. Assemble them as
one document, in that order, so a reader can follow a number from the place it
was produced to the concept it is asked to stand for.

Governance starts before the first column, with the question no earlier week
settled: how do data actually reach you? You answer it in writing, as an
**acquisition route**, the declared path by which your data come to exist,
decided by your M4 permission status. Cleared means you name your frame and
plan for the units you cannot reach. Pending means you build and wait without
touching people. No permission means aggregates, open data, or simulation,
with the cost stated. Then every source gets **provenance**, the documented
origin of a dataset: who produced it, how, when, and under what terms.
"Downloaded from the county election office's results portal, open-data
licence, October 1" is provenance; "found a CSV online" is not.

The second half settles what M4 deliberately left provisional: your
**operationalization**, the exact path from each concept you care about to
the indicator you actually record. You climb the concept → construct →
indicator ladder for every measured concept. You check **reliability**,
whether your instrument reads consistently, on its items rather than on your
respondents. You argue **validity**, whether your scores support the
interpretation you put on them, as a property of interpretation and use
rather than a stamp the instrument carries. And because a changed measure
changes what your estimand refers to, the settled operationalization ships as
the next version of your Research Contract.

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
AI assistant can hunt licences, draft tables, and attack your re-identification
recheck, but whether a measure measures your concept is a judgment you own.
One trap governs the whole week: an assistant can describe a dataset it has
never seen, fluently and wrongly, so every AI claim about your data is
verified against the file itself.

### 1. The acquisition route and the provenance record

Settle acquisition first, in writing, before anything below it.

- **The route, declared.** Which of the three routes your M4 permission
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
- **A retrieval date on every entry.** Sources get revised without notice.
  The date you retrieved a file is what lets a reader tell whether they are
  looking at the version your numbers came from.
- **Unknown written as unknown.** Where a link in the chain is missing, write
  "unknown" instead of filling the gap with a plausible guess. An unknown
  producer is a finding about your evidence, and it belongs on the page.

### 2. The data-management record

Provenance says where your data came from. The **data-management record**
says where they live now and who can reach them. Keep it short and concrete,
one small section a stranger could act on.

- **Location and access.** Where the raw file sits, where the working copy
  sits, who besides you can open either, and how the two are kept distinct.
  A working copy you overwrite is a file you can no longer check yourself
  against.
- **The columns you kept.** Hold every column that actually arrived against
  the analysis your Contract declares. A column with no analysis behind it is
  risk carried for nothing. Record what you dropped or coarsened since your
  M4 plan, and why.
- **The re-identification recheck.** The check is not new: you ran it on your
  planned columns while you were designing. A **re-identification check** asks
  whether someone could combine your kept columns to pick out an individual,
  and hall, major, and hometown can be one person. Run it again on the columns
  that actually arrived, then report what it found and what you changed.

### 3. The route-specific permission recheck

Hold your M4 determination against the data as they actually arrived, not as
you planned them. Data that arrive differently from the plan can carry
permissions the plan did not cover. What you recheck depends on the route you
declared in part 1.

- **Cleared.** Did the units you actually reached stay inside what you were
  cleared to collect, and did any new field appear that your determination
  never covered?
- **Pending.** Did anything you did this week touch a person? Pilot work on
  yourself and simulated data stay open to you; recruitment does not.
- **No permission.** Do the aggregates, open data, or simulated data you used
  carry terms that permit your use, and did you state what the route costs
  your claim?

Close with one declared outcome: still cleared, or what changed and what you
did about it. If the answer is that your status moved to **not authorized**,
the blocking gate applies and you stop and come to me.

### 4. The measurement specification

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
- **Reliability, checked on items and actually run.** **Reliability** is
  whether your instrument reads consistently. Check it on the instrument's
  items — agreement among the items of a scale, the same unit read twice, or
  two coders scoring the same material. Never split your respondents into
  halves and compare group summaries; that measures sampling, not your
  instrument. Run the check on the evidence you actually have and report its
  result. If your indicator is a single item measured once, "no defensible
  reliability check is available for this measure and use" is an honest
  finding: write it down, then narrow the claim or change the instrument.
- **Validity, argued as interpretation and use.** **Validity** is whether
  your scores support the interpretation you put on them, for the use you
  put them to. It is not a stamp the instrument carries. State the
  interpretation, state the use, then name the **strongest rival reading**:
  what else could produce the same number? Close with the boundary that
  follows, one sentence on what your indicator does not capture and who it
  never reaches.

### 5. The Contract version

Your operationalization was provisional at M4 by design. It is provisional no
longer. You open this revisit in class this week, when your Contract comes
back out beside your new measurement specification, and you close it here.
Issue the settled specification as the next dated, numbered version of your
**Research Contract** (v2, if M5 issued v1), with a reason a reader could use
to reconstruct your thinking. Any measurement change is a Contract version,
because it changes what your estimand refers to. Three lines are mandatory in
the revision:

- **The measurement fields, settled.** The indicator, its meaning sentence,
  and the reliability check with its result, written into the Contract.
- **The provisional flag, removed.** Say plainly which M4 field stops being
  provisional here, and whether the settled version differs from what you
  wrote then. A silent swap is the failure; a versioned change with a reason
  is the discipline.
- **Measurement error as uncertainty.** State measurement error alongside
  your sampling uncertainty, not instead of it. A perfectly computed
  interval around a poorly measured quantity is still a poorly measured
  quantity.

### 6. AI Research Ledger rows

Every use of AI in building this record gets a row in your **AI Research
Ledger** (the eight fixed fields: task delegated · tool used · prompt ·
output summary · decision · verification method · remaining concern ·
responsible researcher). Hunting a licence, drafting the provenance table,
proposing indicator wordings, listing what an indicator fails to capture, and
red-teaming your re-identification recheck are all delegable tasks. Each one
you delegated needs a row naming how you verified the result against the
actual file or page, because the verification is the only part a reader can
check. "No AI used" is a legitimate entry if it is true.

**A missing ledger is not a minor lapse.** Per the course rule, a missing AI
Research Ledger entry scores the Craft criterion **0** and the submission is
**returned** for completion before it is graded.

### 7. Dossier update line

End with one line recording what this milestone finalizes in your **Research
Project Dossier**: your **data and measurement documentation** component now
exists — acquisition route, provenance record, data-management record,
measurement specification, permission recheck, and the Contract version that
settled your operationalization. Name the file or section in your dossier
where each now lives.

---

## Definition of Done

You are done when your submission carries all of the following. Use this as a
pre-submission checklist.

| Item | Specification |
|---|---|
| **Acquisition route** | One of the three routes declared in writing (cleared / pending / no permission), with its reason and, where it applies, its stated cost |
| **Provenance record** | One entry per dataset and borrowed number: who produced it, how, when, under what terms, with a retrieval date; the primary source behind your headline claim opened and read; missing links written as "unknown" |
| **Data-management record** | Where the raw and working files live and who can open them; every kept column tied to the declared analysis; the re-identification recheck run on the columns that actually arrived, with its result |
| **Permission recheck** | The M4 determination held against the data as they actually arrived, in the form your route requires; one declared outcome |
| **Measurement ladder** | Concept → construct → indicator for every measured concept; each rung narrows; the construct–indicator gap named |
| **Meaning sentences** | One per indicator, saying what a single recorded value asserts |
| **Reliability** | One check run on items, occasions, or raters, never on split respondents; its result reported, or "no defensible check available" written down with what you narrowed |
| **Validity** | Interpretation and use both stated; the strongest rival reading named; the boundary sentence saying what the indicator misses and who it never reaches |
| **Contract version** | The operationalization settled and issued as the next dated, numbered Contract version with a usable reason; the provisional M4 field named; measurement error stated alongside sampling uncertainty |
| **AI Research Ledger** | One row per AI-assisted step; every verification method named, non-vague, and run against the file or page itself |
| **Dossier line** | The data and measurement documentation component located by file or section |
| **Studio work** | Worked at the Friday studio with your AI assistant |
| **Filename** | `lastname_m05_data_governance.pdf` (or a shared Colab link) |
| **Location** | Brightspace → Assignments → M06 |

---

## Grading Rubric (100 points)

Four bands on the course's five shared virtues
(`planning/ASSESSMENT_ARCHITECTURE.md`). The rows also carry what Book
Milestone 6 asks of the artifact: that it be complete and unmistakably yours,
versioned with a reason, owned rather than tool-asserted, carrying the four
rails, and defensible as one governed-data record.

| Criterion | Exemplary | Proficient | Developing | Beginning |
|---|---|---|---|---|
| **Governance correctness (provenance & measurement)** (30) | Acquisition route settled in writing; provenance complete for every source with its terms and retrieval date named; the data-management record says where files live, who can open them, and which columns survived the analysis test; the measurement ladder narrows at every rung; reliability run on items, occasions, or raters; validity argued as interpretation and use with its rival reading (26–30) | All parts present; one rung, one source's terms, or one check thin (21–25) | A governance piece missing or malformed: reliability by respondent-splitting, columns kept with no analysis behind them, or provenance that stops at a link (13–20) | No acquisition route declared, or a measurement specification that never descends below the concept (0–12) |
| **Evidence integrity & provenance** (20) | Every dataset, licence, and borrowed number is real and retrievable; the primary source behind your headline claim was opened and read; missing links written as unknown rather than guessed; a reader can trace each entry to its origin (18–20) | Real and traceable; one provenance entry thin (14–17) | A dataset, licence, or number asserted without a locatable source (8–13) | A cited dataset, licence, or source that does not exist or does not say what you claim (0–7) |
| **Verification of AI-assisted parts** (20) | Every AI claim about your data verified against the file itself; the permission recheck run in the form your route requires; every ledger row's verification method named and non-vague (18–20) | Ledger present; one verification method vague or one step unlogged (14–17) | Ledger thin; AI outputs used but the against-the-file check not named (8–13) | An AI description of your dataset, or an AI-asserted licence, pasted in and never checked against the file (0–7) |
| **Uncertainty & measurement error** (20) | Measurement error stated alongside sampling uncertainty; the construct–indicator gap named with what it could cost the claim; the boundary sentence says who the measure never reaches; the Contract version carries a usable reason (18–20) | Error, gap, and boundary present; one stated loosely, or the version reason thin (14–17) | Measurement error mentioned but not connected to the claim, or the gap declared closed by assertion (8–13) | No measurement-error statement, or a settled operationalization with no version and no reason (0–7) |
| **Craft, ledger & communication** (10) | On-format, on-time; the four pieces assembled as one record a reader can follow; tables complete and readable; complete AI Research Ledger; dossier line present (9–10) | Minor format lapses; ledger complete (7–8) | Missing pieces or a rushed record (4–6) | Missing AI Research Ledger (Craft scored 0, submission returned) (0–3) |

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

**Blocking gate:** no work at or after M4 proceeds past a **not-authorized**
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
- A measurement that changed since M4 without a Contract version: *Uncertainty
  & measurement error* drops to Developing at best, because a silent swap
  changes what your estimand refers to and leaves no record that it happened.
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
   Reliability lives in the items: agreement among the items of a scale,
   repeated readings of the same unit, or two coders scoring the same
   material.
3. **The keep-everything table.** Keeping every column you managed to collect
   "just in case." Every kept column is a promise to protect it and a surface
   for re-identification, and a column with no declared analysis behind it
   buys you nothing. Hold the arrived columns against the Contract, run the
   re-identification recheck, and record what you dropped.
4. **Validity claimed as a property.** Writing that your instrument "is
   valid" because a published paper used it. Validity belongs to an
   interpretation and a use, not to the instrument, and the published
   validation happened on some population for some purpose. Name yours,
   name the distance from theirs, and name the rival reading that would
   produce the same number.
5. **The silent swap.** Changing an indicator between M4 and this week and
   simply writing the new one down. Your estimand now refers to something
   else, and nothing in the record says so. Issue the Contract version, name
   the field that stops being provisional, and give the reason.

---

*Previous: [M05 — Pathway Declaration and Mandated Contrast](milestone_05_observational_descriptive_audit.md) ·
Next: [M07 — First Executable Analysis + URC Abstract Internal Gate](milestone_07_experimental_measurement_protocol.md) —
your governed data and settled measures meet the code that runs your declared
analysis, producing one result you can reproduce from a clean start, with its
uncertainty attached.*
