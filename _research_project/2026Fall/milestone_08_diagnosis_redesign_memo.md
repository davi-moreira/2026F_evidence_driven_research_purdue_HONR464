# Milestone 08 — Design Diagnosis & Redesign Memo

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

Due: **Friday, October 23, 11:59 PM**. You present a 60-second version in class
on **Wednesday, October 21** (M24) — your weakness, your fix, your before/after
numbers.

| # | File | Description |
|---|---|---|
| 1 | **`lastname_m08_diagnosis.pdf`** | 1–2 pages: the declared simplified design, its diagnosand table, one committed redesign with before/after numbers and cost, and the honest statement of what the simplification omits — plus your AI-use disclosure block. |

---

## Purpose

Pilots train in flight simulators because crashing there is cheap. This
milestone is your simulator. You take the design you declared at M07, express a
**simplified version of it in code** using the course's declare/diagnose engine
(nb11), and run it **1,000 seeded times** to measure how it behaves before any
real data arrive. The engine reports **diagnosands** — bias (does the estimator
hit the truth on average?), power (would it detect a real effect?), and coverage
(do the intervals contain the truth as often as they claim?). Then you fix the
worst weakness with **one committed redesign**, showing the before/after
numbers and what the fix costs. "My design is fine" is a feeling; a diagnosand
table is a measurement. This milestone replaces the first with the second.

## Components

### 1. The declared simplified design (code or prose)

State the design you put into the engine: units, the estimand, the estimator,
the assumed effect size and noise, and the sample size. It will be a
**simplification** of your real project — that is expected and fine. Use the
provided declaration skeleton; you fill in parameters, you do not write the
machinery.

### 2. The diagnosand table (from nb11, 1,000 seeded runs)

Report the engine's output for your design: **bias, power, and coverage**, each
from **1,000 seeded replications** (the seed makes the numbers reproducible —
anyone re-running your notebook gets the same table). Read each number in one
sentence: what it says about your design's health.

- **Example (grounded in course work).** The **mentoring-program simulated
  world** declared at n=100 with a small effect might diagnose to bias near
  zero, power around 0.30, coverage near 0.95 — an unbiased design that is
  simply too small to reliably detect its effect.
- **Non-example.** "My design should work fine because it's a standard
  comparison." No diagnosand table, no seeded runs — an untested design has
  undiagnosed diseases.

### 3. One committed redesign (before/after diagnosands + cost)

Choose the single cheapest change that most fixes the worst diagnosand — a
larger n, a lower-noise measure, a different assignment or estimator — re-run
the engine, and report the **before/after** diagnosand table. State the
**cost** of the fix in real terms (more recruitment, more time, a narrower
question). Compare designs on numbers, not vibes.

- **Example.** "Doubling n from 100 to 200 raises power from 0.30 to 0.55; cost:
  I must recruit 100 more units, feasible only if I switch to the secondary-data
  frame."
- **Non-example (a forbidden move).** Quietly changing the *question* to
  whatever the weak design can already answer, and presenting it as a redesign.
  That is a new declaration, not a redesign, and it must be flagged as such.

### 4. What the simplification leaves out (honest statement)

One paragraph: name what your simplified, in-engine design omits relative to
your real project (a covariate you will actually adjust for, a messier sampling
process, measurement error you did not model) and how those omissions might move
the real diagnosands relative to the simulated ones. This is the honesty tax on
simulation, and it is graded.

### 5. AI-use disclosure block (required on every deliverable)

A short table: which AI tool(s) you used, for what task (locate sources /
operationalize / draft / critique / none), and how you verified the output.
"No AI used" is a fine entry; an undisclosed AI contribution is an
academic-integrity violation.

---

## Submission Expectations

| Item | Specification |
|---|---|
| **Length** | 1–2 pages (PDF), tables included |
| **Reproducibility** | Every diagnosand comes from a seeded run; the numbers in the PDF must match what the notebook produces |
| **Presentation** | 60-second redesign pitch in class Wednesday Oct 21 — weakness, fix, before/after numbers; part of the grade |
| **Filename** | `lastname_m08_diagnosis.pdf` |
| **Location** | Brightspace → Assignments → M08 |

---

## Grading Rubric (100 points)

| Criterion | Exemplary | Proficient | Developing | Beginning |
|---|---|---|---|---|
| **Design declaration fidelity** (15) | Simplified design faithfully represents the real one; parameters justified (13–15) | Faithful; one parameter unexplained (10–12) | Simplification distorts the project without saying so (5–9) | No declared design, or it mismatches M07 (0–4) |
| **Diagnosis correctness** (25) | Bias, power, coverage all reported from 1,000 seeded runs and read correctly (22–25) | All three reported; one reading loose (18–21) | A diagnosand missing or misread (11–17) | No diagnosand table, or numbers do not reproduce (0–10) |
| **Redesign quality** (25) | One committed redesign with before/after diagnosands and a stated, honest cost (22–25) | Redesign with before/after; cost vague (18–21) | Redesign proposed without before/after numbers (11–17) | No redesign, or a silent question-swap presented as one (0–10) |
| **Honest simplification statement** (15) | Omissions named and their likely effect on real diagnosands reasoned (13–15) | Omissions named; effect not reasoned (10–12) | Vague acknowledgment (6–9) | Claims the simulation is the real design (0–5) |
| **Redesign pitch** (10) | 60 seconds, weakness/fix/numbers, on time (9–10) | Delivered with minor overrun (7–8) | Over time or numbers missing (4–6) | Not delivered without arrangement (0–3) |
| **Craft & disclosure** (10) | On-format, on-time, complete AI-disclosure block (9–10) | Minor format lapses (7–8) | Missing components or sloppy tables (4–6) | Missing disclosure block (0–3) |

**Revision:** eligible under the standing policy — a revised PDF within 7 days
of feedback recovers up to half the lost points.

## Penalties

- Late: −10 points per day, up to 3 days; not accepted after (documented
  emergencies: talk to me first, per the syllabus).
- **A reported diagnosand that does not reproduce from your seeded notebook: the
  Diagnosis criterion scores Beginning (0–10)** regardless of the rest — a number
  you cannot regenerate is not evidence.
- A silent question-swap presented as a redesign: the Redesign criterion scores
  Beginning (0–10); relabel it honestly as a new declaration.
- Missing AI-disclosure block: Craft scores 0 and the submission is returned for
  completion before grading.

## Common Pitfalls

1. **Diagnosis as decoration.** Running the engine, pasting the table, and never
   saying what the numbers mean for *this* design. Read each diagnosand aloud in
   a sentence.
2. **The heroic redesign.** Proposing five improvements at once. Commit to the
   single cheapest fix and show its before/after — that is the skill.
3. **The unpriced fix.** "Just collect more data." Every redesign has a cost;
   name it, or the comparison is dishonest.
4. **The silent question-shrink.** Redesigning by quietly answering an easier
   question. If you narrow the question, say so out loud — it may be the right
   move, but only when the reader can see it.
5. **Simulation mistaken for reality.** Reporting simulated diagnosands as if
   they were your project's true properties. Name what the simplification leaves
   out.

---

*Previous: [M07 — Design Declaration + URC Abstract](milestone_07_design_declaration_urc_abstract.md) ·
Next: [M09 — Pilot Analysis](milestone_09_pilot_analysis.md) — you stop
simulating and run the real analysis, on real data, bounded to exactly what it
can support.*
