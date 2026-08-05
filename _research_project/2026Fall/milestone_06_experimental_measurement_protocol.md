# Course milestone M6 — First Executable Analysis (+ URC Abstract Internal Gate)

<!-- book-milestone-bridge:begin -->
> **Book Milestone bridge (D41)** — course milestone **M6**.
> This submission presents **Book Milestone 7 — Your first reproducible analysis** (version 1 — executable first run): work from its [milestone page](https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464/book/studios/milestone07-first-analysis.html#milestone).
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

Due: **Friday, October 9, 11:59 PM**. That Friday is a **pipeline clinic and
abstract workshop**: you bring your running notebook, walk your first result and
your AI-code verification record past your AI assistant's review, and clear the
internal gate on your URC abstract before it can go out. You polish from the
clinic notes and submit by the same-day deadline.

| # | File | Description |
|---|---|---|
| 1 | **A shared Colab notebook link** *or* **`lastname_m06_first_analysis.ipynb`** | The pipeline notebook carrying the six-part deliverable below: the seeded pipeline itself, your first result with its uncertainty (labeled provisional), your AI-code verification record, your URC abstract draft, your AI Research Ledger rows, and your dossier line. If you prefer the written parts as a PDF, attach **`lastname_m06_first_analysis.pdf`** alongside; the notebook is still required. This is the graded artifact. |
| 2 | **EDR\|AI "It is your turn" — ch. 22** | The completed "It is your turn" sections of this milestone's book chapters, worked in their companion Colab notebooks (share the links) or included in your artifact. See "The Book Anchor" below. |

Set sharing so the instructor can open **and rerun** the notebook. Confirm the
result in your write-up matches what the notebook prints when run top to bottom.

---

## The Book Anchor — "It Is Your Turn"

This milestone is anchored in the course book, **EDR\|AI**. Read the chapters
below as you develop the milestone, and complete each chapter's closing **"It
is your turn"** section in its companion Colab notebook (or carry the same
work inside your project notebook):

- Ch. 22 — [AI as Programmer](https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464/book/part4-credible-evidence/19-ai-as-programmer.html) · [companion notebook](https://colab.research.google.com/github/davi-moreira/2026F_evidence_driven_research_purdue_HONR464/blob/main/notebooks/book/ch19_ai_as_programmer.ipynb)

These sections are the point of the reading, not extra work: across the
semester, the book's "It is your turn" sections — one per lesson, collected by the twelve Book Milestones — chain into your final
research chapter, so what you complete here is a draft piece of your final
artifact. Include the completed sections in this milestone's submission (see
the submission table above) and carry them forward in your Research Project
Dossier.

---

## Purpose

Everything your project has said so far, it has said in words. Your Contract
names the question, your route declaration names the design, and your
measurement plan names how each concept becomes a column. This week the words
become running code, and your project produces its first number.

The artifact is a **pipeline notebook**: a seeded notebook that starts at your
raw data and runs top to bottom to your reported result, with no step done by
hand in between. Its one discipline is simple to state and hard to keep: it
implements the analysis you **declared**, and nothing else. You fixed that
analysis before you could see any results, because a method chosen after seeing
which one flatters your data proves nothing. The pipeline is where that
pre-commitment gets kept, in code a reader can run.

The number the pipeline produces this week is a **provisional result**: a result
you report while its verification is still pending. You attach its uncertainty
and you label it provisional, because next week's clean restart (M7) decides
whether it deserves the word verified. Reporting it now, honestly labeled, is
how research actually moves; reporting it as settled would be the overclaim.

The same Friday carries a second, fixed anchor: the **URC abstract internal
gate**. The abstract is the short public description of your project, and it
leaves the course on the conference's calendar, not on your verification
schedule. So it clears an internal check now, with the provisional label doing
the honesty work.

> **A question that often comes up here:** *"The notebook ran and printed a
> number. Why can't I call the result final?"* Because a notebook that ran once
> is not yet a notebook that runs. Cells executed out of order can leave stale
> values in memory that silently feed later results. Until the pipeline survives
> a restart from a clean state, the number is a strong draft, and the
> provisional label is what keeps your claim honest in the meantime.

## Components

### 1. The pipeline notebook

Build the seeded notebook (`SEED = 464`) that runs top to bottom: data in,
declared analysis, result out. Three rules govern it.

- **It implements the declared analysis, and nothing else.** Write the analysis
  your Contract and route declaration commit you to, before you look at
  anything else. Exploration that touches the reported result is not
  exploration; it is an undeclared analysis.
- **It loads data from the source your M5 governance record documents**, so a
  reader can follow the pipeline all the way back to provenance.
- **Every number it reports traces to a data cell and a line of code.** No
  number appears in your prose that the notebook does not compute.

### 2. The first result, with its uncertainty

Report the one result your declared analysis produces, in the form your
Contract specified, with its **uncertainty statement** attached: the interval,
spread, or standard error your route provides. A result reported without
uncertainty is not yet a result. Label it in writing, next to the number:
*provisional pending the clean-restart verification (M7)*. Then read it in one
sentence: what the number says, for which units, and what it does not cover.

### 3. The AI-code verification record

Delegate the writing of code as freely as you like; verify every returned
number yourself. For anything AI wrote in your pipeline, record two checks:

- **The known-answer test** — run the code on a tiny input where you already
  know the right output, and confirm it returns exactly that. For example, feed
  your group-difference function two three-row groups you can average by hand.
- **The line review** — read every AI-written line and say in your own words
  what it does. Any line you cannot explain gets rewritten or removed; you
  cannot defend a pipeline you cannot narrate.

Both checks live in the notebook, next to the code they verify, with a ledger
row each.

### 4. The URC abstract draft (the internal gate)

Write the abstract you would submit to the **Undergraduate Research
Conference**, roughly 150–250 words, describing your project as it now stands:
the question, what you measure, the analysis your pipeline executes, the first
result labeled provisional, and the boundary around the claim. This is an
**internal gate**: the abstract must clear the instructor's check at the studio
before it goes out externally. The gate has one non-negotiable rule — the
abstract must stay inside the claim your evidence can support. An abstract that
promises a causal finding your route does not license, that reaches a
population your data never touched, or that reports the provisional number as
settled, does not clear the gate.

> **A question that often comes up here:** *"Why write the abstract now, while
> the result is still provisional?"* Because the abstract's clock is external
> and this Friday is its fixed anchor. The skill being graded is writing a
> public description that is both true today and safe tomorrow: bounded to your
> route, labeled provisional where it must be, and worded so no verification
> outcome can make it retroactively false.

### 5. AI Research Ledger rows

Every use of AI in building this milestone gets a row in your **AI Research
Ledger** (the eight-field table: task delegated · tool used · prompt · output
summary · decision · verification method · remaining concern · responsible
researcher). Drafting pipeline code, debugging an error message, and
red-teaming your abstract are all delegable tasks, and each one you delegated
needs a row naming how you verified the result. "No AI used" is a legitimate
entry if it is true.

**A missing ledger is not a minor lapse.** Per the course rule, a missing AI
Research Ledger entry scores the Craft criterion **0** and the submission is
**returned** for completion before it is graded.

### 6. The dossier update line and the version line

Open the artifact with its version line: **Book Milestone 7, version 1
(executable first run)**, dated, with the reason a reader could use to
reconstruct your thinking. Then end with one line recording what this milestone
adds to your **Research Project Dossier**: the reproducible-analysis component
now exists in executable form, carrying a provisional first result and a gated
URC abstract. Name the file or section where each now lives.

---

## Definition of Done

You are done when your submission carries all of the following. Use this as a
pre-submission checklist.

| Item | Specification |
|---|---|
| **Pipeline notebook** | Seeded (`SEED = 464`); runs top to bottom from data to result; implements the declared analysis and nothing else |
| **First result** | Reported in the form your Contract specified, with its uncertainty statement, labeled provisional pending the M7 clean restart |
| **AI-code verification** | Known-answer test run and reported; every AI-written line reviewed and explained in your own words |
| **URC abstract** | Roughly 150–250 words; inside the claim your evidence supports; the internal gate cleared at the studio |
| **Version line** | Book Milestone 7, version 1, dated, with its reason |
| **Permission status** | Your M3/M5 permission determination is still authorized; blocked work does not proceed |
| **AI Research Ledger** | One row per AI-assisted step; every verification method named and non-vague |
| **Dossier line** | The executable pipeline and the gated abstract located by file or section |
| **Studio work** | Worked at the Friday studio (Oct 9) with your AI assistant; abstract gate cleared; submitted the same day |
| **Filename** | A shared Colab link or `lastname_m06_first_analysis.ipynb`; optional `lastname_m06_first_analysis.pdf` companion |
| **Location** | Brightspace → Assignments → M06 |

---

## Grading Rubric (100 points)

Four bands on the course's five shared virtues
(`planning/ASSESSMENT_ARCHITECTURE.md`), grounded in the studio's authored
criteria for this checkpoint (`planning/BOOK_ASSESSMENTS.yml`,
`first-analysis-v1`).

| Criterion | Exemplary | Proficient | Developing | Beginning |
|---|---|---|---|---|
| **Compass & pathway alignment** (20) | The pipeline implements exactly the declared analysis; the result answers the declared question in the declared form; the abstract stays inside the route's licence (18–20) | Declared analysis implemented; one link between the result and the declaration loose (14–17) | Undeclared extras feed the reported result, or the result drifts from the declared form (8–13) | The pipeline answers a different question than the project declared (0–7) |
| **Evidence integrity & provenance** (20) | Data loaded from the documented M5 source; every reported number traces to a data cell and a line of code (18–20) | Traceable; one provenance link thin (14–17) | A dataset or number asserted without a locatable origin (8–13) | A source that does not exist, or a number with no path back to data (0–7) |
| **Verification of AI-assisted parts** (25) | The known-answer test and the line review are both real and recorded; every AI-assisted step is ledgered with a named, non-vague verification; every judgment is defended in your words, not the tool's (22–25) | Both checks present; one verification vague or one step unlogged (18–21) | AI code used with the known-answer test or the line review missing (11–17) | AI output reproduced without any verification, or code in the pipeline you cannot explain (0–10) |
| **Uncertainty & provisional boundary** (20) | The uncertainty statement is attached and read correctly; the provisional label is present; the abstract makes no promise the evidence cannot keep (18–20) | Uncertainty and label present; one stated loosely (14–17) | A point estimate with no uncertainty, or the provisional label missing (8–13) | The first run reported as a settled finding, or an abstract that overclaims past the route (0–7) |
| **Craft, ledger & abstract gate** (15) | Versioned with its reason, on-format, on-time, gate cleared, complete AI Research Ledger, dossier line present (13–15) | Minor format lapses; abstract and ledger complete (10–12) | Missing pieces, a rushed clinic walkthrough, or an ungated abstract (5–9) | Missing AI Research Ledger (Craft scored 0, submission returned) (0–4) |

**Hard caps (a single failure caps the row regardless of the rest):**

- A **fabricated or unretrievable source** caps *Evidence integrity &
  provenance* at Beginning.
- An **untraceable number** — a reported figure with no path back to your data —
  caps *Verification of AI-assisted parts* at Beginning.
- A **non-reproducing result** — a reported number that does not rerun from your
  seeded notebook — caps *Verification of AI-assisted parts* at Beginning.
- A **missing AI Research Ledger entry** scores *Craft, ledger & abstract gate*
  **0** and the submission is **returned** unread until it is supplied.

**Revision:** eligible under the standing policy — a revised submission within 7
days of feedback recovers up to half the lost points.

## Penalties

- Late: −10 points per day, up to 3 days; not accepted after (documented
  emergencies: talk to me first, per the syllabus).
- Any dataset or source you cite that turns out not to exist or not to be what
  you claim: *Evidence integrity & provenance* scores Beginning regardless of
  the rest — the course's evidence-integrity rule with teeth.
- A reported number that does not rerun from your seeded notebook:
  *Verification of AI-assisted parts* scores Beginning — a number you cannot
  regenerate is not evidence.
- Missing AI Research Ledger entry: *Craft* scores 0 and the submission is
  returned for completion before grading.

## Common Pitfalls

1. **The pipeline that does more than you declared.** Running several
   specifications "to see what happens," then reporting the one that looks
   best. The whole value of declaring first is that the method cannot be chosen
   to flatter the answer. Implement the declared analysis and nothing else; any
   exploration that feeds the reported result undoes your pre-commitment.
2. **The number pasted from a chat.** An estimate that lives in an AI reply,
   with no cell that produces it. If the notebook does not compute it on a
   rerun, it is not your result, and it caps your Verification score. Put every
   reported figure behind a line of code, and run the known-answer test on the
   code that produced it.
3. **The abstract that outruns the pipeline.** A URC abstract that promises a
   causal finding, or a population claim, while your pipeline licenses a
   provisional result for the units you analyzed. The abstract must sit inside
   the claim your evidence supports; an abstract that overclaims does not clear
   the internal gate.

---

*Previous: [M05 — Data and Measurement Governance](milestone_05_causal_identification.md) ·
Next: [M07 — Clean-Restart Verified Analysis](milestone_07_declared_analysis_protocol.md) —
your provisional first result faces a fresh runtime, and either every number
reproduces or the discrepancy becomes the finding.*
