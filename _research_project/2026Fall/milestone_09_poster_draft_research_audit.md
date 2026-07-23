# Milestone 09 — Poster Draft 1 and Research Audit

## About the Research Project

Your semester project is **individual**: one researcher, one question, carried
from curiosity to a defended, reproducible claim. It runs through milestones
**M0–M15**, peaks publicly at the **Purdue Fall Undergraduate Research Expo
poster session (Tuesday, November 17 — required)**, and closes with an oral
**Evidence Defense** and a final research chapter in December. Every milestone
follows the same cadence: **Friday-studio kickoff → develop across the week →
present → submit → revise (where eligible)**. Every milestone also updates your
cumulative **Research Project Dossier** and appends at least one row to your
**AI Research Ledger** — the running record of what you handed to AI and how you
checked it. Milestone weights and the revision policy live in the syllabus;
instructions and rubrics live one page per milestone, like this one.

---

## What to Submit on Brightspace

Due: **Friday, October 30, 11:59 PM**. At the Friday studio that day you present
a short walkthrough and your draft is red-teamed on the **four audits** by two
peers and by two required GenAI Studio reviewer roles (the **Poster Critic** and
the **Robustness & Sensitivity Reviewer**).

| # | File | Description |
|---|---|---|
| 1 | **`lastname_m09_poster_draft.pdf`** | **Poster draft 1**: your project laid out as a first poster — question, evidence, and one bounded headline claim. A rough draft, not the locked poster. |
| 2 | **`lastname_m09_audit.pdf`** *or* the same as notebook sections | **The research audit**: the four-part written record of how hard you tried to break your own claim and what survived. This is the graded core. |
| 3 | **`lastname_m09_audit.ipynb`** *or* a shared Colab link | The runnable audit notebook — seeded, reruns end to end. **Every number on your poster draft and in your audit traces to a cell here.** |

If you submit a notebook link, set sharing so the instructor can open it, and
confirm every figure renders when the notebook is run top to bottom.

---

## Purpose

This is the milestone where you stop producing evidence and start **attacking
it** — first yourself, then in front of a room. You take the first real estimate
you computed at M8 and you try to break it on purpose, before a stranger at the
Expo does it for you. The skill you are practicing is the one every later defense
rests on: **a number you have not tried to break is a number you cannot yet
defend.**

A **research audit** is the graded record of that attempt. It lays out the
robustness and placebo checks you committed to *before* you looked, what your
headline claim looks like after those checks, which flaws a human and an AI panel
found that survived a data check, and the one limitation no check could fix. It is
the difference between a result you went looking for and a result that survived a
test you set in advance.

Alongside the audit you assemble **poster draft 1**: the same evidence, shaped for
the first time into a poster that reads from question to bounded claim. This is
draft 1 on purpose. The full poster-craft treatment — read path, data-ink, figure
honesty — arrives next week at M10. Here the draft exists early so your evidence
and its boundary can be attacked while there is still time to change them.

> **A question that often comes up here:** *"If the poster gets its real polish at
> M10, why draft it now at all?"* Because the fastest way to find an overclaim is
> to try to fit it on a poster. A headline that will not sit inside its compass
> boundary in one line, or a number you cannot trace to a cell when a reviewer
> points at it, is a problem you want surfaced this week — not at the Expo. The
> draft is bait for the red-team; the audit is what you learned from letting them
> bite.

## Components

### 1. Poster draft 1

A first full draft of your poster: your research **question**, your **evidence**,
and **one bounded headline claim**. Three things are graded here, and all three
are skills you have already practiced:

- **One headline claim, inside its boundary.** State your finding in one sentence
  that carries its **compass kind** (descriptive or causal) and its **range**, not
  a single flattering number. "In the units my data reach, the gap runs about 0.6
  to 0.9 SD" is a bounded headline. "Trust drives support" on an observational
  design is an **overclaim** the draft must not make: it reports an observational
  association with the grammar of a cause.
- **Every number traces to a cell.** Each figure and number on the draft points to
  the cell in your audit notebook that produced it. A number with no cell behind it
  is an **untraceable number**, and the Poster Critic role is tuned to hunt for
  exactly these.
- **Uncertainty is visible, not buried.** The headline's range or interval appears
  on the draft, in the same eye-span as the claim.

Poster *craft* (the read path, the data-ink, the axis honesty) is previewed by the
four-audit red-team this week and graded fully at M10. Draft 1 is judged on whether
the claim, its traceability, and its uncertainty are honest — not on polish.

### 2. The research audit (the four-part spine)

The heart of this milestone. Write the four pieces you drafted in the week's
notebook, now finalized for *your* project. A reader who has never seen your work
should be able to tell exactly how far you pushed on your own number.

- **Pre-listed checks.** The **three** robustness or placebo checks you committed
  to *before* you looked at any of their results, each tied to the reviewer attack
  it answers. Name each check by what it varies — the **sample**, the
  **measurement**, the **specification**, or the **metric** — or name it as a
  **placebo test** or a **leave-one-out influence** check. Pre-listing is the whole
  discipline that separates honest robustness from a **specification search**.
- **What survived.** Your headline claim after the checks ran, worded to carry its
  **range** and its **compass boundary**. If a check moved the estimate, say which
  one and by how much. A **specification curve** that stays positive across every
  defensible choice is a direction plus a range, never a single number.
- **The verified AI-review trail.** The real flaws your human reviewer and your
  multi-model AI panel found, each marked **confirmed or refuted by a data check** —
  not by how confident the reviewer sounded. Include the single most confident
  **wrong** flag you caught, and name it: an AI reviewer that asserts a flaw the
  data refute is **confident fabrication**, and two reviewers wrong the same way are
  **correlated errors**, not a confirmation.
- **The remaining limitation.** The one weakness no check could fix, stated as
  expertise, not hidden. A limitation you name yourself is a strength; one a
  reviewer finds for you at the Expo is a wound.

### 3. The audit notebook (traceability)

A seeded notebook (`SEED = 464`) that reruns top to bottom and reproduces every
number you report. Your pre-listed checks live here as runnable cells. This is what
makes the audit checkable rather than merely asserted: a result that will not rerun
from this notebook is not yet a result.

### 4. AI Research Ledger rows

Every use of AI in building this audit and draft gets a row in your **AI Research
Ledger** (the eight fixed fields: task delegated · tool used · prompt · output
summary · decision · verification method · remaining concern · responsible
researcher). Proposing an extra specification, red-teaming your headline sentence,
running the Poster Critic on your draft, and adjudicating a multi-model panel are
all delegable tasks, and each one you delegated needs a row naming how you verified
it against your own data. "No AI used" is a legitimate entry if it is true.

**A missing ledger is not a minor lapse.** Per the course rule, a missing AI
Research Ledger entry scores the Craft criterion **0** and the submission is
**returned** for completion before it is graded.

### 5. Dossier update line

End with one line recording what this milestone finalizes in your **Research
Project Dossier**: your **robustness and diagnostic record** now exists (the
pre-listed checks and their results), and your **claim–evidence table** now carries
its audited row — claim, evidence, verification, boundary, and what survived
sensitivity. Name the file or section where each now lives.

---

## Definition of Done

You are done when your submission carries all of the following. Use this as a
pre-submission checklist.

| Item | Specification |
|---|---|
| **Poster draft 1** | Question → evidence → one bounded headline claim; uncertainty visible; every number traceable to a cell |
| **Pre-listed checks** | Three checks, named and tied to the reviewer attack each answers, committed before looking |
| **What survived** | Headline reworded to carry its range and compass boundary; any check that moved it reported by how much |
| **Verified AI-review trail** | Each flag marked confirmed or refuted by a data check; the loudest wrong flag named |
| **Remaining limitation** | The one weakness no check fixed, stated plainly |
| **Notebook** | Seeded (`SEED = 464`); reruns top to bottom; every reported number traces to a cell |
| **AI Research Ledger** | One row per AI-assisted step; every verification method named and non-vague |
| **Dossier line** | Robustness/diagnostic record and claim–evidence row located by file or section |
| **Presentation** | Short walkthrough at the Friday studio; four-audit red-team by two peers + the two required GenAI Studio roles; feedback incorporated |
| **Filenames** | `lastname_m09_poster_draft.pdf`, `lastname_m09_audit.pdf` (or notebook sections), `lastname_m09_audit.ipynb` |
| **Location** | Brightspace → Assignments → M09 |

---

## Grading Rubric (100 points)

Four bands on the course's five shared virtues
(`planning/ASSESSMENT_ARCHITECTURE.md`).

| Criterion | Exemplary | Proficient | Developing | Beginning |
|---|---|---|---|---|
| **Compass & pathway alignment** (20) | Headline claim stays inside its declared compass kind and reach; the poster draft and the audit both carry the range, never a single flattering number; no overclaim past the declared boundary (18–20) | Inside the boundary; range stated but loosely, or one sentence reaches slightly past the design (14–17) | Boundary present but the headline drifts toward a claim the design does not license (8–13) | Overclaim: an observational correlation narrated as a cause, or a sample described as a population (0–7) |
| **Evidence integrity & provenance** (20) | Every number on the draft and in the audit traces to a real cell, dataset, or retrievable source; a reader can follow each to its origin (18–20) | Traceable; one number's path thin or one source under-linked (14–17) | A claimed figure or source asserted without a locatable origin (8–13) | A fabricated or unretrievable source, or a headline number with no path back to the data (0–7) |
| **Verification & robustness** (25) | Three pre-listed checks run and reported in full; each AI-flagged issue confirmed or refuted by a named data check; the loudest wrong flag caught; the notebook reruns and every number reproduces (23–25) | Checks run and mostly reported; one verification vague, or one flag acted on without a named check (18–22) | A single generic "I checked it" line, or checks run after the result was chosen and relabeled as pre-listed (11–17) | Specification searching reported as robustness, an AI flag pasted in unverified, or a headline number that does not rerun from the notebook (0–10) |
| **Uncertainty & limitations** (20) | The surviving headline carries its range or interval; the one limitation no check fixed is stated as expertise, calibrated, neither hidden nor spiraling (18–20) | Uncertainty and limitation both present but one stated loosely (14–17) | Only a point estimate, or a limitation gestured at without saying what it costs the claim (8–13) | No uncertainty stated, or the result reported as settled certainty (0–7) |
| **Craft, ledger & communication** (15) | Poster draft 1 assembled and legible, on-format, on-time; clear studio walkthrough with the four-audit feedback incorporated; complete AI Research Ledger; dossier line present (14–15) | Minor format lapses; ledger complete (11–13) | Missing pieces or a rushed walkthrough; feedback not incorporated (6–10) | Missing AI Research Ledger (Craft scored 0, submission returned) (0–5) |

**Hard caps (a single failure caps the row regardless of the rest):**

- A **fabricated or unretrievable source** caps *Evidence integrity & provenance*
  at Beginning.
- An **untraceable number** — a figure with no path back to your data — caps
  *Verification & robustness* at Beginning.
- A **non-reproducing result** — a headline number that does not rerun from your
  submitted notebook — caps *Verification & robustness* at Beginning.
- A **missing AI Research Ledger entry** scores *Craft, ledger & communication*
  **0** and the submission is **returned** unread until it is supplied.

**Revision:** eligible under the standing policy — a revised submission within 7
days of feedback recovers up to half the lost points.

## Penalties

- Late: −10 points per day, up to 3 days; not accepted after (documented
  emergencies: talk to me first, per the syllabus).
- Any source you cite that turns out not to exist or not to say what you claim:
  *Evidence integrity & provenance* scores Beginning regardless of the rest — the
  course's evidence-integrity rule with teeth.
- A headline number that does not reproduce from your submitted notebook:
  *Verification & robustness* scores Beginning regardless of the rest.
- Missing AI Research Ledger entry: *Craft* scores 0 and the submission is returned
  for completion before grading.

## Common Pitfalls

1. **The specification search dressed as robustness.** Quietly running many
   versions of your analysis and putting only the one that reached significance on
   the poster, with the search never disclosed. Same table, opposite integrity. The
   only defense is the order on the record: pre-list your checks, run all of them,
   and report the whole picture — including the ones that showed nothing.
2. **The unverified AI flag.** Pasting a reviewer's confident critique into your
   audit as a real finding, or its caveat into your limitations, without running the
   data check that settles it. A flaw is real when your own output confirms it, not
   when a model sounds sure. Two models agreeing can be correlated error, not
   confirmation. Draft your claim yourself, then let AI attack it, then verify the
   attack.
3. **The orphan number on the poster.** A headline figure with no cell behind it,
   or an "in the sample" result quietly upgraded to "in general" or "causes" once it
   is shrunk to poster size. If you cannot point to the cell that produced a number,
   you cannot defend it — and the Expo will ask.

---

*Previous: [M08 — Minimum Viable Analysis](milestone_08_minimum_viable_analysis.md) ·
Next: [M10 — Final Poster Lock](milestone_10_final_poster_lock.md) — the audited
claim that survived this week becomes the single defensible headline your locked
poster carries to the Expo, with no revision window behind it.*
