# Course milestone M7 — Clean-Restart Verified Analysis

<!-- book-milestone-bridge:begin -->
> **Book Milestone bridge (D41)** — course milestone **M7**.
> This submission presents **Book Milestone 8 — Your robustness audit** (version 1): work from its [milestone page](https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464/book/studios/milestone08-stress-test.html#milestone).
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

Due: **Friday, October 16, 11:59 PM** (you work on it at that Friday's studio).
That studio is a **clean-restart verification exchange**: you rerun your
pipeline in a fresh runtime, chase every number that moved, and run the
required **Prediction & Leakage Auditor** before you submit.

| # | File | Description |
|---|---|---|
| 1 | **A shared Colab notebook link** *(the verified pipeline notebook)* | The seven-part record below, carried in the notebook's markdown or in an optional companion **`lastname_m07_verified_analysis.pdf`**: your clean-restart record, your claim-to-output trace, the reproduced uncertainty, two independent re-derivations, the leakage audit with the auditor's flags and your written fixes, your AI Research Ledger rows, and your dossier line. This is the graded artifact. |
| 2 | **EDR\|AI "It is your turn" — ch. 24, ch. 25, ch. 26, ch. 27** | The completed "It is your turn" sections of this milestone's book chapters, worked in their companion Colab notebooks (share the links) or included in your artifact. See "The Book Anchor" below. |

Set sharing so the instructor can open **and rerun** the notebook. The rerun is
the milestone: confirm it reproduces before you submit.

---

## The Book Anchor — "It Is Your Turn"

This milestone is anchored in the course book, **EDR\|AI**. Read the chapters
below as you develop the milestone, and complete each chapter's closing **"It
is your turn"** section in its companion Colab notebook (or carry the same
work inside your project notebook):

- Ch. 24 — [Robustness and Sensitivity](https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464/book/part4-credible-evidence/21-robustness-and-sensitivity.html) · [companion notebook](https://colab.research.google.com/github/davi-moreira/2026F_evidence_driven_research_purdue_HONR464/blob/main/notebooks/book/ch21_robustness_and_sensitivity.ipynb)
- Ch. 25 — [Diagnostics and Negative Tests](https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464/book/part4-credible-evidence/22-diagnostics-and-negative-tests.html) · [companion notebook](https://colab.research.google.com/github/davi-moreira/2026F_evidence_driven_research_purdue_HONR464/blob/main/notebooks/book/ch22_diagnostics_and_negative_tests.ipynb)
- Ch. 26 — [AI as Adversarial Reviewer](https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464/book/part4-credible-evidence/23-ai-as-adversarial-reviewer.html) · [companion notebook](https://colab.research.google.com/github/davi-moreira/2026F_evidence_driven_research_purdue_HONR464/blob/main/notebooks/book/ch23_ai_as_adversarial_reviewer.ipynb)
- Ch. 27 — [Recognizing False Confidence](https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464/book/part4-credible-evidence/24-recognizing-false-confidence.html) · [companion notebook](https://colab.research.google.com/github/davi-moreira/2026F_evidence_driven_research_purdue_HONR464/blob/main/notebooks/book/ch24_recognizing_false_confidence.ipynb)

These sections are the point of the reading, not extra work: across the
semester, the book's "It is your turn" sections — one per lesson, collected by the twelve Book Milestones — chain into your final
research chapter, so what you complete here is a draft piece of your final
artifact. Include the completed sections in this milestone's submission (see
the submission table above) and carry them forward in your Research Project
Dossier.

---

## Purpose

At M6 your declared analysis became a pipeline and produced its first number.
The declaring came first for a reason: your route's precommitments fixed (for prediction routes: target, baseline, and metric; for the other routes: estimand, estimator, and uncertainty form) and a
metric chosen before any score could flatter you is the only method a reader
has to trust. Your pipeline kept that pre-commitment. This week decides whether
its output deserves the word **verified**: a result that survives checks you
did not design it to pass.

The central move is the **clean restart**: a rerun from a fresh runtime, with
all memory cleared, using Restart & Run All from the top. It matters because
notebooks accumulate **hidden state** — values left in memory by cells you
edited or ran out of order, silently feeding later results. You rename a
column, but the old one still lives in memory; every cell below keeps working,
and every number below may be wrong. A notebook that ran once is a draft. A
notebook that runs from nothing is evidence.

Verification here is five checks, not one. The restart must match. Every claim
must trace to its cell. The uncertainty itself must reproduce. One key number
must survive two independent re-derivations. And a required auditor must find no
leak and no unlicensed generalization in what you plan to say. If any number
moves on the restart, the pipeline is the finding: you explain and fix every
discrepancy before any claim goes forward.

> **A question that often comes up here:** *"My numbers matched on the first
> restart. Am I done?"* A match is the entry ticket, not the milestone. A
> pipeline can reproduce a wrong number perfectly, run after run. The
> claim-to-output trace catches the number you misquoted, the re-derivation
> catches the bug both runs shared, and the leakage audit catches the sentence
> that quietly claims more than the pipeline computed. All five checks together
> are what "verified" means here.

## Components

### 1. The clean-restart record

Restart your runtime so memory is empty, then Restart & Run All. Record three
things: the environment you ran in (one cell that prints your Python and
library versions), the headline numbers before and after, and the verdict. If
the numbers match, say so, to the digit you report. If any number moves,
explain the discrepancy, fix its cause, and restart again until the pipeline is
stable. "Close enough" is not a category. A moved digit has a cause: hidden
state, an out-of-order cell, or an unseeded draw. Finding it is a real result
about your own evidence machine.

### 2. The claim-to-output trace

Build the **claim-to-output trace**: a table pointing every number you plan to
report to the specific cell that produces it. One row per number: the sentence
it appears in, the number, the cell. This is what lets a reader (and a future
you) audit your writing against your code in minutes. A figure with no cell
behind it is an **untraceable number**, and it caps your Verification score.

### 3. The uncertainty, verified

The interval must reproduce, not just the point estimate. Rerun from the clean
start and confirm that the uncertainty statement your Contract specified (the
interval, spread, or standard error) comes back to the same values. If your
interval comes from resampling or simulation, the seed (`SEED = 464`) is what
makes that possible. A result whose uncertainty does not reproduce is not
verified, and a result without uncertainty is not yet a result.

### 4. Two independent re-derivations

Do this for TWO key numbers, not one — the week's notebook and the
studio both practice the pair.

Recompute one key number by a route that shares none of the original code: by
hand from a small table, with a different library, or from the raw definition
in a fresh cell. That is an **independent re-derivation** — the same number
reached twice by unrelated paths. For example, recompute your pipeline's
difference in means from two group averages you calculate with plain
arithmetic. If the routes agree, your belief in the number no longer rests on
one script. If they disagree, you just found the bug this milestone exists to
catch, and the fix goes in the clean-restart record.

### 5. The leakage audit (required reviewer role)

Submit your verified draft to the **Prediction & Leakage Auditor** (the
required GenAI Studio reviewer role for M7; full briefing in
`genai_studio/roles/prediction_leakage_auditor.md`). Its focus depends on your
route.

- **If your route predicts**, the auditor hunts **data leakage**: a feature
  whose value is only settled at or after the outcome it is supposed to
  predict. Settle each flag with two checks in your own pipeline — the **timing
  check** (is the feature's value known before the prediction moment?) and the
  **correlation check** (does the feature track the outcome so tightly it is
  almost a copy of the answer?). A feature that fails the timing check is
  dropped or re-timed, no matter how much it helps the score.
- **For every other route**, the auditor's focus is your language: it hunts any
  **out-of-sample or generalization claim** — a sentence that quietly extends
  your result to units, times, or populations your design never reached. Every
  flagged sentence gets bounded or cut.

For every flag, write your fix or your refutation, each settled by a check in
your own pipeline. The auditor can miss a real leak and invent a false one; its
flags are hypotheses to test, never verdicts.

### 6. AI Research Ledger rows

Every use of AI in this verification gets a row in your **AI Research Ledger**
(the eight-field table: task delegated · tool used · prompt · output summary ·
decision · verification method · remaining concern · responsible researcher).
Writing the environment-record cell, proposing re-derivation routes, and
running the Prediction & Leakage Auditor are all delegable tasks, and each one
you delegated needs a row naming how you verified the result. "No AI used" is a
legitimate entry if it is true.

**A missing ledger is not a minor lapse.** Per the course rule, a missing AI
Research Ledger entry scores the Craft criterion **0** and the submission is
**returned** for completion before it is graded.

### 7. The dossier update line and the version line

Open the artifact with its version line: **Book Milestone 7, version 2
(clean-restart verified)**, dated, with the reason: what changed since version
1, and why. Then end with one line recording what this milestone finalizes in
your **Research Project Dossier**: the **reproducible Colab notebook**
component now exists, verified rather than merely executable, together with its
claim-to-output trace. Name the file or section where each now lives.

---

## Definition of Done

You are done when your submission carries all of the following. Use this as a
pre-submission checklist.

| Item | Specification |
|---|---|
| **Clean-restart record** | Fresh runtime; Restart & Run All; environment recorded; numbers match to the digit reported, or every discrepancy explained and fixed |
| **Claim-to-output trace** | Every number you plan to report pointed to the cell that produces it |
| **Uncertainty** | The interval itself reproduces from the clean start, seeded (`SEED = 464`) |
| **Re-derivation** | One key number recomputed by an independent route; the agreement, or the bug it exposed, reported |
| **Leakage audit** | Prediction & Leakage Auditor run; every flag fixed or refuted by a check in your own pipeline |
| **Version line** | Book Milestone 7, version 2, dated, with a reason a reader could reconstruct |
| **Permission status** | Your permission determination is still authorized; blocked work does not proceed |
| **AI Research Ledger** | One row per AI-assisted step; every verification method named and non-vague |
| **Dossier line** | The verified reproducible notebook and its trace located by file or section |
| **Studio work** | Worked at the Friday studio (Oct 16) with your AI assistant; required auditor review logged; submitted the same day |
| **Filename** | A shared Colab link (required); optional `lastname_m07_verified_analysis.pdf` companion |
| **Location** | Brightspace → Assignments → M07 |

---

## Grading Rubric (100 points)

Four bands on the course's five shared virtues
(`planning/ASSESSMENT_ARCHITECTURE.md`), grounded in the studio's authored
criteria for this checkpoint (`planning/BOOK_ASSESSMENTS.yml`,
`first-analysis-v1`, version 2).

| Criterion | Exemplary | Proficient | Developing | Beginning |
|---|---|---|---|---|
| **Compass & pathway alignment** (15) | The verified result still answers the declared question in the declared form; no out-of-sample or generalization language survives past the route's licence (13–15) | Aligned; one boundary sentence loose (10–12) | The result drifts from the declared form, or one flagged generalization is left unbounded (5–9) | The claim answers a different question than the project declared, or keeps a generalization the audit flagged (0–4) |
| **Evidence integrity & provenance** (20) | Every reported number traces to its cell; the environment and data source are recorded; a reader can follow every figure to its origin (18–20) | Traceable; one trace row or the environment record thin (14–17) | A reported figure whose cell takes real effort to locate, or an incomplete trace (8–13) | A number with no path back to the notebook, or a source that does not exist (0–7) |
| **Verification** (30) | The clean restart is run and recorded; every discrepancy explained and fixed; both re-derivations are genuinely independent; every auditor flag settled by a named check; every AI-assisted step ledgered with a non-vague verification (27–30) | All five checks present; one recorded loosely (21–26) | A restart claimed but not recorded, a re-derivation that reuses the original code, or a flag answered without a check (14–20) | No clean restart, a discrepancy left unexplained, or an auditor flag pasted in or dismissed unverified (0–13) |
| **Uncertainty & claim boundary** (20) | The interval reproduces and is read correctly; the result is never worded as settled certainty; the claim stops where the evidence stops (18–20) | Interval reproduces; one reading or boundary sentence loose (14–17) | Only the point estimate verified, or uncertainty reported but never read (8–13) | No uncertainty, or a verified point estimate narrated as a certain finding (0–7) |
| **Craft, ledger & communication** (15) | Versioned with its reason, on-format, on-time, complete AI Research Ledger, dossier line present (13–15) | Minor format lapses; ledger complete (10–12) | Missing pieces or a rushed record (5–9) | Missing AI Research Ledger (Craft scored 0, submission returned) (0–4) |

**Hard caps (a single failure caps the row regardless of the rest):**

- A **fabricated or unretrievable source** caps *Evidence integrity &
  provenance* at Beginning.
- An **untraceable number** — a reported figure with no path back to your
  notebook — caps *Verification* at Beginning.
- A **non-reproducing result** — a headline number or interval that does not
  rerun from a fresh runtime — caps *Verification* at Beginning.
- A **missing AI Research Ledger entry** scores *Craft, ledger & communication*
  **0** and the submission is **returned** unread until it is supplied.

**Revision:** eligible under the standing policy — a revised submission within 7
days of feedback recovers up to half the lost points.

## Penalties

- Late: −10 points per day, up to 3 days; not accepted after (documented
  emergencies: talk to me first, per the syllabus).
- Any dataset, feature, or source you cite that turns out not to exist or not
  to be what you claim: *Evidence integrity & provenance* scores Beginning
  regardless of the rest — the course's evidence-integrity rule with teeth.
- A headline number or interval that does not rerun from a fresh runtime:
  *Verification* scores Beginning — a number you cannot regenerate is not
  evidence.
- Missing AI Research Ledger entry: *Craft* scores 0 and the submission is
  returned for completion before grading.

## Common Pitfalls

1. **The restart that never happened.** Trusting the in-session numbers because
   the notebook "just ran." Hidden state — an edited cell, an out-of-order run,
   an unseeded draw — can keep a wrong number alive for weeks. Restart from a
   clean runtime, run everything, and record what printed.
2. **The discrepancy waved past.** A number moves on the restart and you call
   it "close enough." Every moved digit has a cause, and until you find it you
   do not know which of the two numbers is yours. Explain it, fix it, and
   restart again; if the numbers move, the pipeline is the finding.
3. **The auditor treated as a verdict, or as noise.** Pasting the auditor's
   flags into your record unexamined, or dismissing them unexamined, are the
   same mistake. Each flag is a hypothesis; only a timing check, a correlation
   check, or a boundary rewrite in your own pipeline settles it.

---

*Previous: [M06 — First Executable Analysis (+ URC Abstract Internal Gate)](milestone_06_experimental_measurement_protocol.md) ·
Next: [M08 — Robustness Audit](milestone_08_minimum_viable_analysis.md) —
your verified result now gets attacked on purpose: pre-listed checks, a named
negative test, and an adversarial review decide what survives.*
