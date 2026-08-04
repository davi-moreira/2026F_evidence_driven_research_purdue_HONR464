# Course milestone M8 — Robustness Audit

<!-- book-milestone-bridge:begin -->
> **Book Milestone bridge (D41)** — course milestone **M8**.
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

Due: **Friday, October 23, 11:59 PM** (you work on it at that Friday's studio).
That studio is a **robustness-audit walkthrough**: you walk your pre-listed
checks, what survived them, and your loudest wrong flag past the required
**Robustness & Sensitivity Reviewer**, and you polish from what the walkthrough
surfaces.

| # | File | Description |
|---|---|---|
| 1 | **`lastname_m08_audit.pdf`** *or* the same as notebook sections | **The robustness audit**: the four-part written record below of how hard you tried to break your own verified result and what survived. This is the graded core. |
| 2 | **`lastname_m08_audit.ipynb`** *or* a shared Colab link | The runnable audit notebook — seeded, reruns end to end. Every number in your audit traces to a cell here. |
| 3 | **EDR\|AI "It is your turn" — ch. 23, ch. 24, ch. 25, ch. 26** | The completed "It is your turn" sections of this milestone's book chapters, worked in their companion Colab notebooks (share the links) or included in your artifact. See "The Book Anchor" below. |

If you submit a notebook link, set sharing so the instructor can open it, and
confirm every check reruns when the notebook is run top to bottom.

---

## The Book Anchor — "It Is Your Turn"

This milestone is anchored in the course book, **EDR\|AI**. Read the chapters
below as you develop the milestone, and complete each chapter's closing **"It
is your turn"** section in its companion Colab notebook (or carry the same
work inside your project notebook):

- Ch. 23 — [Robustness and Sensitivity](https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464/book/part4-credible-evidence/21-robustness-and-sensitivity.html) · [companion notebook](https://colab.research.google.com/github/davi-moreira/2026F_evidence_driven_research_purdue_HONR464/blob/main/notebooks/book/ch21_robustness_and_sensitivity.ipynb)
- Ch. 24 — [Diagnostics and Negative Tests](https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464/book/part4-credible-evidence/22-diagnostics-and-negative-tests.html) · [companion notebook](https://colab.research.google.com/github/davi-moreira/2026F_evidence_driven_research_purdue_HONR464/blob/main/notebooks/book/ch22_diagnostics_and_negative_tests.ipynb)
- Ch. 25 — [AI as Adversarial Reviewer](https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464/book/part4-credible-evidence/23-ai-as-adversarial-reviewer.html) · [companion notebook](https://colab.research.google.com/github/davi-moreira/2026F_evidence_driven_research_purdue_HONR464/blob/main/notebooks/book/ch23_ai_as_adversarial_reviewer.ipynb)
- Ch. 26 — [Recognizing False Confidence](https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464/book/part4-credible-evidence/24-recognizing-false-confidence.html) · [companion notebook](https://colab.research.google.com/github/davi-moreira/2026F_evidence_driven_research_purdue_HONR464/blob/main/notebooks/book/ch24_recognizing_false_confidence.ipynb)

These sections are the point of the reading, not extra work: across the
semester, the book's "It is your turn" sections — one per lesson, collected by the twelve Book Milestones — chain into your final
research chapter, so what you complete here is a draft piece of your final
artifact. Include the completed sections in this milestone's submission (see
the submission table above) and carry them forward in your Research Project
Dossier.

---

## Purpose

This is the milestone where you stop producing evidence and start **attacking
it**. You take the clean-restart verified result from M7 and try to break it on
purpose, before a reviewer or a stranger does it for you. The skill you are
practicing is the one every later defense rests on: a result you have not tried
to break is a result you do not yet know.

A **robustness audit** is the graded record of that attempt. It lays out the
checks you committed to *before* you looked at their results, what your
headline claim looks like after they ran, which flags from a human and an AI
panel survived a data check, and the one limitation no check could fix. It is
the difference between a result you went looking for and a result that survived
a test you set in advance.

Two disciplines govern the whole audit. You report the checks that hurt your
finding as fully as the ones that helped it. And an AI reviewer is another
critique, never independent verification: a flag becomes real when a check in
your own data confirms it, not when the reviewer sounds certain.

> **A question that often comes up here:** *"What happens if a check breaks my
> result?"* You are graded on the audit, not on survival. A finding that fails
> its own pre-listed checks sends you back to your route or your pipeline;
> that is the honest path, not softer wording. It happens while there is
> still time to fix things before the poster locks. A broken result found now
> costs a revision. A broken result found by a reader later costs the claim.

## Components

### 1. The pre-listed checks

The heart of the audit. Commit in writing to **three** robustness or placebo
checks *before* you look at any of their results, each tied to the reviewer
attack it answers. Name each check by what it varies (the **sample**, the
**measurement**, the **specification**, or the **metric**), or name it as a
**negative test** or a **leave-one-out influence** check.

A **negative test** is a check run where your design predicts nothing should
appear, and its prediction is written *before* the run. Judge it against the
**null reference spread** — the range of values the test produces when nothing
is really there — never against exact zero. A placebo estimate of 0.03 passes
if the null spread covers it; a fail is a value the spread cannot explain.

Commit to reporting all three, whatever they show. Pre-listing is the whole
discipline that separates honest robustness from a **specification search**:
quietly running many versions of the analysis and reporting the winner.

### 2. What survived

Your headline claim after the checks ran, reworded to carry its **range** and
its **compass boundary**. If a check moved the estimate, say which one and by
how much. Two guard-rails apply by name:

- A same-sign **specification spread** — the range of estimates across your
  defensible analysis choices — is a direction plus a range, never an
  uncertainty interval. It measures your choices, not sampling noise. Report it
  as "positive across all N specifications, from A to B," and compare only
  checks measured in the same units; a span pooled across incomparable panels
  means nothing.
- If units dropped out of your data, a **complete-case contrast** — a
  comparison run only on the units with complete records — is never "the
  effect among stayers." Who stays can depend on the outcome, so the complete
  cases answer a different question; name the question your contrast actually
  answers.

### 3. The verified AI-review trail

Submit your audited result to the **Robustness & Sensitivity Reviewer** (the
required GenAI Studio reviewer role for M8; full briefing in
`genai_studio/roles/robustness_sensitivity_reviewer.md`), plus your multi-model
panel if you run one. Then adjudicate: every flag marked **confirmed or refuted
by a data check**, never by how confident the reviewer sounded. Include the
single most confident **wrong** flag you caught, and name it for what it is: an
AI reviewer asserting a flaw the data refute is **confident fabrication**, and
two reviewers wrong the same way are **correlated errors**, not a
confirmation. A flag with no check behind it does not enter the audit.

### 4. The remaining limitation and the adjudication

Name the one weakness no check could fix, stated as expertise, not hidden. A
limitation you name yourself is a strength; one a reviewer finds for you is a
wound. Then close the audit with the adjudication in three lines: what
survived, what did not, and what you still cannot rule out. Findings are never
communicated as certainties, and this is where your result's honest edges get
written down.

### 5. The audit notebook

A seeded notebook (`SEED = 464`) that reruns top to bottom and reproduces every
number the audit reports. Your three pre-listed checks live here as runnable
cells, with the negative test's prediction written in markdown above its cell,
so the order of commitment is on the record. A result that will not rerun from
this notebook is not yet a result.

### 6. AI Research Ledger rows

Every use of AI in building this audit gets a row in your **AI Research
Ledger** (the eight-field table: task delegated · tool used · prompt · output
summary · decision · verification method · remaining concern · responsible
researcher). Proposing an extra specification, red-teaming your surviving
headline, running the Robustness & Sensitivity Reviewer, and adjudicating a
panel are all delegable tasks, and each one you delegated needs a row naming
how you verified it against your own data. "No AI used" is a legitimate entry
if it is true.

**A missing ledger is not a minor lapse.** Per the course rule, a missing AI
Research Ledger entry scores the Craft criterion **0** and the submission is
**returned** for completion before it is graded.

### 7. The dossier update line and the version line

Open the artifact with its version line: **Book Milestone 8, version 1**,
dated, with the reason a reader could use to reconstruct your thinking. Then
end with one line recording what this milestone finalizes in your **Research
Project Dossier**: the **robustness and diagnostic record** now exists — the
pre-listed checks, their full results, the adjudication, and the limitation.
Name the file or section where each now lives.

---

## Definition of Done

You are done when your submission carries all of the following. Use this as a
pre-submission checklist.

| Item | Specification |
|---|---|
| **Pre-listed checks** | Three checks, named by what each varies and tied to the reviewer attack it answers, committed before looking |
| **Negative test** | Prediction written before the run; judged against the null reference spread, never exact zero |
| **What survived** | Headline reworded with its range and compass boundary; any check that moved it reported by how much; the specification spread reported as direction plus range, never as an interval |
| **Attrition guard-rail** | Any complete-case contrast named for the question it actually answers — never "the effect among stayers" |
| **Verified AI-review trail** | Robustness & Sensitivity Reviewer run; each flag confirmed or refuted by a data check; the loudest wrong flag named |
| **Remaining limitation** | The one weakness no check fixed, stated plainly, with the three-line adjudication |
| **Notebook** | Seeded (`SEED = 464`); reruns top to bottom; every reported number traces to a cell |
| **Version line** | Book Milestone 8, version 1, dated, with its reason |
| **Permission status** | Your permission determination is still authorized; blocked work does not proceed |
| **AI Research Ledger** | One row per AI-assisted step; every verification method named and non-vague |
| **Dossier line** | The robustness and diagnostic record located by file or section |
| **Studio work** | Worked at the Friday studio (Oct 23) with your AI assistant; required Robustness & Sensitivity review logged; submitted the same day |
| **Filenames** | `lastname_m08_audit.pdf` (or notebook sections), `lastname_m08_audit.ipynb` (or a shared Colab link) |
| **Location** | Brightspace → Assignments → M08 |

---

## Grading Rubric (100 points)

Four bands on the course's five shared virtues
(`planning/ASSESSMENT_ARCHITECTURE.md`), grounded in the studio's authored
criteria for this checkpoint (`planning/BOOK_ASSESSMENTS.yml`,
`robustness-audit-v1`).

| Criterion | Exemplary | Proficient | Developing | Beginning |
|---|---|---|---|---|
| **Compass & pathway alignment** (15) | The surviving headline stays inside its declared compass kind and reach, and carries its range, never a single flattering number (13–15) | Inside the boundary; the range stated loosely (10–12) | The headline drifts toward a claim the design does not license (5–9) | Overclaim: an observational correlation narrated as a cause, or a sample described as a population (0–4) |
| **Evidence integrity & provenance** (15) | Every number in the audit traces to a real cell, dataset, or retrievable source (13–15) | Traceable; one path thin (10–12) | A claimed figure or source without a locatable origin (5–9) | A fabricated or unretrievable source, or a number with no path back to data (0–4) |
| **Verification & robustness** (30) | Three pre-listed checks run and reported in full, the harmful ones included; every flag confirmed or refuted by a named data check; the loudest wrong flag caught; the notebook reruns and every number reproduces (27–30) | Checks run and mostly reported; one verification vague, or one flag acted on without a named check (21–26) | A generic "I checked it," or checks run after the result was chosen and relabeled as pre-listed (14–20) | Specification searching reported as robustness, an AI flag pasted in unverified, or a headline number that does not rerun (0–13) |
| **Uncertainty & limitations** (25) | The surviving headline carries its range or interval; the specification spread is never presented as an interval; the negative test is judged on its null spread; any complete-case contrast is named for what it answers; the limitation is stated as expertise, calibrated (22–25) | All present; one stated loosely (18–21) | Only a point estimate, or a limitation gestured at without saying what it costs the claim (11–17) | No uncertainty, an exact-zero verdict on the negative test, or a "stayers" effect claimed from complete cases (0–10) |
| **Craft, ledger & communication** (15) | Versioned with its reason, on-format, on-time, walkthrough feedback incorporated, complete AI Research Ledger, dossier line present (13–15) | Minor format lapses; ledger complete (10–12) | Missing pieces or a rushed walkthrough (5–9) | Missing AI Research Ledger (Craft scored 0, submission returned) (0–4) |

**Hard caps (a single failure caps the row regardless of the rest):**

- A **fabricated or unretrievable source** caps *Evidence integrity &
  provenance* at Beginning.
- An **untraceable number** — a figure with no path back to your data — caps
  *Verification & robustness* at Beginning.
- A **non-reproducing result** — a headline number that does not rerun from
  your submitted notebook — caps *Verification & robustness* at Beginning.
- A **missing AI Research Ledger entry** scores *Craft, ledger & communication*
  **0** and the submission is **returned** unread until it is supplied.

**Revision:** eligible under the standing policy — a revised submission within 7
days of feedback recovers up to half the lost points.

## Penalties

- Late: −10 points per day, up to 3 days; not accepted after (documented
  emergencies: talk to me first, per the syllabus).
- Any source you cite that turns out not to exist or not to say what you claim:
  *Evidence integrity & provenance* scores Beginning regardless of the rest —
  the course's evidence-integrity rule with teeth.
- A headline number that does not reproduce from your submitted notebook:
  *Verification & robustness* scores Beginning regardless of the rest.
- A specification search reported as robustness — many versions run, only the
  flattering one disclosed: *Verification & robustness* scores Beginning.
- Missing AI Research Ledger entry: *Craft* scores 0 and the submission is
  returned for completion before grading.

## Common Pitfalls

1. **The specification search dressed as robustness.** Quietly running many
   versions of your analysis and reporting only the one that reached
   significance, with the search never disclosed. Same table, opposite
   integrity. The only defense is the order on the record: pre-list your
   checks, run all of them, and report the whole picture — including the ones
   that showed nothing.
2. **The unverified AI flag.** Pasting a reviewer's confident critique into
   your audit as a real finding, or its caveat into your limitations, without
   running the data check that settles it. A flaw is real when your own output
   confirms it, not when a model sounds sure. Two models agreeing can be
   correlated error, not confirmation.
3. **The guard-rail slips.** Judging your negative test against exact zero, or
   narrating a complete-case contrast as "the effect among stayers." Both
   quietly swap in a different question. A null check has its own noise, so
   name the spread; dropped units have their own reasons, so name the question
   the complete cases actually answer.

---

*Previous: [M07 — Clean-Restart Verified Analysis](milestone_07_declared_analysis_protocol.md) ·
Next: [M09 — Bounded Research-Note v0](milestone_09_poster_draft_research_audit.md) —
the claims your audit licensed, at the strength it licensed them, become a
research note a stranger can weigh.*
