# Milestone 09 — Pilot Analysis

## About the Research Project

Your semester project is **individual**: one researcher, one question, carried
from curiosity to a defended, reproducible claim. It runs through milestones
M00–M23, peaks publicly at the **Purdue Fall Undergraduate Research Expo
poster session (Tuesday, November 17 — required)**, and closes with an oral
**Evidence Defense** and a final research dossier in December. Every milestone
follows the same cadence: **develop in class → present → submit → revise**.
Milestone weights and the revision policy are in the syllabus; instructions
and rubrics live one page per milestone, like this one.

---

## What to Submit on Brightspace

Due: **Friday, October 30, 11:59 PM**. You present a 4-minute walkthrough in
class that same day (M28); each listener logs one verification question for you,
and you owe answers **before the poster**.

| # | File | Description |
|---|---|---|
| 1 | **`lastname_m09_pilot.pdf`** | 2–3 pages: your branch's analysis, results with uncertainty and claim boundary, the verification log, and your AI-use disclosure block. |
| 2 | **`lastname_m09_pilot.ipynb`** | The runnable pilot notebook. **Every number in the PDF must trace to a cell in this notebook.** |

---

## Purpose

This is the milestone where you stop declaring and diagnosing and actually
**run the analysis** — on real data (or your simulated world), producing your
project's first genuine evidence. It is deliberately **branched by approach**:
the pilot you run is the one your declared approach demands, and the standard you
are held to is that branch's standard. Whatever branch you are in, two things are
non-negotiable and shared across all of them: **every number in your write-up
traces to a cell in your notebook**, and you keep a **verification log** of how
you cross-checked your own outputs. A result you cannot regenerate, or cannot say
how you checked, is not yet a result.

## Components

### Shared components (all branches)

- **The pilot notebook** (`lastname_m09_pilot.ipynb`) — runnable top to bottom,
  seeded where anything is random, so anyone re-running it reproduces your
  numbers.
- **Number-to-cell traceability** — every figure and number in the PDF points to
  the cell that produced it. No orphan numbers.
- **The verification log** (graded) — a short list: for each key result, how you
  cross-checked it (recomputed a second way, spot-checked rows by hand,
  triangulated against a known quantity, compared to the M08 diagnosis).
- **The 4-minute walkthrough** (M28) — what you ran, what came out, what
  surprised you; you collect one verification question per listener and answer
  them before the poster.
- **AI-use disclosure block** — which AI tool(s), for what task (locate sources /
  operationalize / draft / critique / none), and how you verified the output.
  "No AI used" is fine; an undisclosed AI contribution is an academic-integrity
  violation.

### Your branch's analysis

Run **the branch your declared approach requires.** Each branch has its own
deliverable and its own standard.

**Description branch.** Honest summary tables and distributions of the **actual
data**, with every claim bounded to the data at hand.
- *Example:* a table of `lapop_brazil` trust items — shares and distributions —
  reported as "in these interviews, X% report…", never "Brazilians believe…".
- *Non-example:* "Brazilians trust the courts more than the police" — a
  generalization the description cannot buy.

**Inference branch.** An **estimate + an uncertainty interval + a generalization
argument** bounded by your sampling frame.
- *Example:* a mean or adjusted association from a `la_voter_file` sample,
  reported with a 95% interval and a sentence on which population the frame
  actually reaches.
- *Non-example:* a bare point estimate ("turnout is 61%") with no interval and no
  statement of whom it generalizes to.

**Prediction branch.** A **baseline + a model + a held-out comparison + a leakage
check.**
- *Example:* predict `la_voter_file` turnout — a dummy baseline, a simple model,
  both scored on held-out rows, with the feature list checked for leakage.
- *Non-example:* any accuracy number computed on data the model already saw, or a
  "top feature X drives turnout" explanation claim.

**Causal branch.** An **identification argument + an effect estimate + one
assumption probe.** For an **observational** project where identification is not
available, run the **honest association-only analysis** and **sketch the causal
design that WOULD identify** the effect.
- *Example:* analyze the `foos_etal` randomized GOTV experiment — balance check,
  difference-in-means with an interval, a 3-sentence identification argument,
  and one probe of that argument.
- *Non-example:* DiD/RDD/IV vocabulary decorating a comparison whose assumptions
  were never stated — design-mimicry.

**Mixed projects.** Run your **primary branch fully** and add the **core check**
of your secondary branch (for example, a full inference pilot plus one honest
descriptive table). Say in one line why the combination is warranted.

---

## Submission Expectations

| Item | Specification |
|---|---|
| **Length** | 2–3 pages (PDF) + the notebook |
| **Reproducibility** | Notebook runs top to bottom; randomness seeded; every PDF number traces to a cell |
| **Verification** | A written log of how each key result was cross-checked — a graded component, not a formality |
| **Presentation** | 4-minute pilot walkthrough Friday Oct 30; you collect and later answer one verification question per listener |
| **Filenames** | `lastname_m09_pilot.pdf` and `lastname_m09_pilot.ipynb` |
| **Location** | Brightspace → Assignments → M09 |

---

## Grading Rubric (100 points)

### Shared criteria (70 points — apply to every branch)

| Criterion | Exemplary | Proficient | Developing | Beginning |
|---|---|---|---|---|
| **Traceability & reproducibility** (20) | Notebook runs top to bottom, seeded; every PDF number traces to a named cell (18–20) | Runs with a trivial fix; traceability nearly complete (14–17) | Some numbers untraceable, or a cell errors (8–13) | Notebook does not run, or numbers cannot be located (0–7) |
| **Verification log** (20) | Each key result cross-checked a second way, method stated per result (18–20) | Most results checked; one unlogged (14–17) | A single generic "I checked it" line (8–13) | No verification log (0–7) |
| **Uncertainty & claim boundary** (15) | Results carry uncertainty and stay strictly inside the branch's boundary (13–15) | Inside the boundary; uncertainty thin (10–12) | One boundary slip or missing interval (6–9) | Overclaim (generalization, causation, or leakage-inflated score) (0–5) |
| **Walkthrough & verification questions** (10) | 4 minutes, clear arc; listener questions collected and answered before the poster (9–10) | Delivered; light follow-up on questions (7–8) | Over time or questions unanswered (4–6) | Not delivered without arrangement (0–3) |
| **Craft & disclosure** (5) | On-format, on-time, complete AI-disclosure block (5) | Minor format lapses (4) | Missing components (2–3) | Missing disclosure block (0–1) |

### Branch execution (30 points — grade on the table for your declared branch)

| Branch | Exemplary (27–30) | Proficient (21–26) | Developing (12–20) | Beginning (0–11) |
|---|---|---|---|---|
| **Description** | Honest tables + distributions of the real data; every claim bounded to the data at hand | Tables present; one claim reaches past the data | Summary present but distributions or bounding missing | Generalizes beyond the sample as if descriptive = population |
| **Inference** | Estimate + interval + a generalization argument bounded by the frame | Estimate + interval; generalization loosely bounded | Estimate present; interval or frame argument missing | Bare estimate narrated as truth for everyone |
| **Prediction** | Baseline + model + held-out comparison + a real leakage check | All present; leakage check cursory | Model beats baseline but scoring or leakage check is off | In-sample score, or leakage uncaught, or importance read as cause |
| **Causal** | Identification argument + effect estimate + one assumption probe (or honest association-only + the identifying design sketched) | Argument + estimate; probe or sketch thin | Estimate present; identification asserted, not argued | Design-mimicry: causal vocabulary, no argued assumptions |

**Mixed projects** are graded on their primary branch's column, with the secondary
branch's core check folded into the Verification-log and Uncertainty rows.

**Revision:** eligible under the standing policy — a revised PDF + notebook
within 7 days of feedback recovers up to half the lost points.

## Penalties

- Late: −10 points per day, up to 3 days; not accepted after (documented
  emergencies: talk to me first, per the syllabus).
- **A reported number that does not reproduce from the submitted notebook: the
  Verification criterion scores Beginning (0–7)** regardless of the rest — this
  is the course's evidence-integrity rule with teeth.
- A result claimed outside the branch's boundary (a descriptive pilot narrated as
  a population fact, a predictive score read as explanation, an association read
  as an effect): the Uncertainty & claim-boundary criterion scores Beginning.
- Missing AI-disclosure block: Craft scores 0 and the submission is returned for
  completion before grading.

## Common Pitfalls

1. **Orphan numbers.** A figure in the PDF with no cell behind it. If you cannot
   point to the cell, you cannot defend the number — and M22 will ask.
2. **The verification formality.** "I double-checked everything." The log must
   say *how*, per result: recomputed, spot-checked, triangulated.
3. **The excited-mouth upgrade.** The pilot behaves, and the write-up quietly
   promotes "associated" to "causes" or "in the sample" to "in general." Stay in
   your branch.
4. **Leakage you were warned about.** A spectacular held-out score usually means
   a leak, not a breakthrough. Check the features before you celebrate.
5. **Hiding a failed pilot.** A pilot that collapsed is legitimate evidence —
   present the failure and its diagnosis. Fabricating or forcing a clean result
   is the one unrecoverable move.

---

*Previous: [M08 — Design Diagnosis & Redesign Memo](milestone_08_diagnosis_redesign_memo.md) ·
Next: [M10 — Poster Storyboard](milestone_10_poster_storyboard.md) — your
pilot's honest evidence becomes one defensible headline and a 90-second read
path.*
