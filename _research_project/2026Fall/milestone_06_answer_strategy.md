# Milestone 06 — Answer Strategy Declaration

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

Due: **Wednesday, October 14, 11:59 PM**. That same day (M21) is the in-class
**clinic** where you run the claim-anatomy checklist on your own declaration
with rotating consults and a pair proof-read — bring a near-final draft.

| # | File | Description |
|---|---|---|
| 1 | **`lastname_m06_answer_strategy.pdf`** | 1–2 pages: the triad, the concrete procedure, the uncertainty plan, and the pre-written result sentence, plus your AI-use disclosure block. |

---

## Purpose

This milestone completes MIDA. M03 gave you the **inquiry** — the number or
pattern the genie would hand you. M06 supplies the **answer strategy**: the
exact, named procedure that turns your data into an estimate of that inquiry,
and the honest account of how far off that estimate could be. The discipline
here is the **estimand → estimator → estimate** triad: the quantity you want,
the recipe you will run, and the dish that recipe produces. A number with no
named procedure behind it ("the analysis shows…") is not an answer strategy. By
the end you will have written the sentence that reports your future result —
*before you have it* — worded so that it cannot say more than your approach
permits.

## Components

### 1. The estimand / estimator / estimate triad (≈1 short paragraph)

State all three for your project, in order:

- **Estimand** — the quantity you declared at M03 (an average treatment effect,
  a population share, an adjusted association, a held-out accuracy). The genie's
  number.
- **Estimator** — the procedure that targets it (difference-in-means, an
  adjusted regression, a baseline-vs-model comparison). The recipe.
- **Estimate** — what that estimator will hand you when run on your data. The
  dish. (You will fill in the actual value at the pilot, M09; here you name what
  *kind* of number it will be and its units.)

### 2. The concrete procedure (≈1 paragraph)

Name the procedure precisely enough that someone else could run it. Pick the
form your **declared approach** requires — for example:

- **Inference / causal:** difference-in-means between two groups, or an
  **adjusted regression with HC2 robust standard errors**, naming the outcome,
  the key regressor, and the two honest covariates you will adjust for.
- **Prediction:** a **baseline-vs-model comparison** on held-out data, naming
  the target, the baseline rule, the model, and the metric.
- **Description:** the summary and grouping that produces your honest table,
  naming the variables and the cut.

- **Example (grounded in course work).** For the **mentoring-program simulated
  world**, the estimand is the average treatment effect of mentoring on the
  outcome; the estimator is difference-in-means between the mentored and
  un-mentored groups; the estimate will be a difference in outcome units.
- **Non-example.** "I'll run the numbers and see what the data say." No named
  procedure, no stated estimand — this is inquiry shopping waiting to happen.

### 3. The uncertainty plan (≈1 paragraph)

State, in advance, how you will express how wrong you could be: a confidence
interval from robust standard errors, a bootstrap or simulation-based interval,
the spread of held-out performance across resamples. Name the source of the
uncertainty (sampling variability, measurement error, a small n) and how your
plan will surface it. A result strategy with no uncertainty plan is a defect —
uncertainty deleted is certainty invented.

### 4. The pre-written result sentence, inside the boundary (1–2 sentences)

Write the sentence you will use to report your finding, with a blank where the
number goes, worded so it stays **inside your approach's claim boundary**:

- Description: "In these data, ___% of ___ show ___."
- Inference: "In the population my frame reaches, ___ and ___ are associated by
  ___ (95% interval ___), adjusting for ___."
- Prediction: "On held-out cases, my model beats the baseline by ___ on ___."
- Causal: "Under [stated, checked identification], the effect of ___ on ___ is
  ___ (interval ___)."

- **Non-example (crossed out for a reason).** "Adjusting for the covariates I
  named, X **causes** a ___ increase in Y." Reading a regression coefficient as
  a causal effect because covariates were "controlled for" is exactly the
  overreach M19 had you cross out. Keep the verb inside what the design bought.

### 5. AI-use disclosure block (required on every deliverable)

A short table: which AI tool(s) you used, for what task (locate sources /
operationalize / draft / critique / none), and how you verified the output.
"No AI used" is a fine entry; an undisclosed AI contribution is an
academic-integrity violation.

---

## Submission Expectations

| Item | Specification |
|---|---|
| **Length** | 1–2 pages (PDF), plus the disclosure block |
| **Clinic** | In-class claim-anatomy clinic Wednesday Oct 14 — bring a near-final draft; consult notes and your pair proof-read feed the grade |
| **Style** | Clear prose; a heading per component; the result sentence quoted exactly as you will use it |
| **Filename** | `lastname_m06_answer_strategy.pdf` |
| **Location** | Brightspace → Assignments → M06 |

---

## Grading Rubric (100 points)

| Criterion | Exemplary | Proficient | Developing | Beginning |
|---|---|---|---|---|
| **Triad correctness** (25) | Estimand, estimator, estimate each named and mutually consistent; the estimator genuinely targets the declared estimand (22–25) | All three present; the link between estimand and estimator slightly loose (18–21) | One element missing or mislabeled (11–17) | Estimator does not target the inquiry, or the triad is absent (0–10) |
| **Procedure concreteness** (20) | Procedure named precisely enough to reproduce, and it fits the declared approach (18–20) | Procedure named but under-specified in one respect (14–17) | Vague ("run a regression") with no outcome/regressor/metric named (8–13) | No named procedure (0–7) |
| **Uncertainty plan** (15) | Source of uncertainty named and a concrete method to express it (13–15) | Plan present but generic (10–12) | Uncertainty mentioned, no method (5–9) | No uncertainty plan (0–4) |
| **Boundary-safe result sentence** (20) | Pre-written sentence sits exactly inside the approach's boundary; verb matches the design (18–20) | Inside the boundary with one soft word to tighten (14–17) | One claim-boundary violation (the silent upgrade) (8–13) | Causal or population claim the design cannot buy (0–7) |
| **Clinic engagement & revision** (10) | Ran the claim-anatomy checklist on own work; consult and proof-read feedback visibly incorporated (9–10) | Participated; light incorporation (7–8) | Present but disengaged (4–6) | Absent without arrangement (0–3) |
| **Craft & disclosure** (10) | On-format, on-time, complete AI-disclosure block (9–10) | Minor format lapses (7–8) | Missing components or sloppy citations (4–6) | Missing disclosure block (0–3) |

**Revision:** eligible under the standing policy — a revised PDF within 7 days
of feedback recovers up to half the lost points.

## Penalties

- Late: −10 points per day, up to 3 days; not accepted after (documented
  emergencies: talk to me first, per the syllabus).
- A result sentence that claims outside its approach's boundary (association
  reported as effect, sample reported as population): the Boundary criterion
  scores Beginning (0–7) regardless of the rest.
- Any cited source or dataset that turns out not to exist or not to say what you
  claim: the relevant criterion scores Beginning — the course's
  evidence-integrity rule with teeth.
- Missing AI-disclosure block: Craft scores 0 and the submission is returned for
  completion before grading.

## Common Pitfalls

1. **The oracle regression.** Naming "regression" as if it answers the question
   by itself. Regression is an estimator, not an oracle — say what it estimates
   and under what reading.
2. **The number with no recipe.** "The analysis shows 4.2." Which analysis?
   Every estimate must trace to a named estimator.
3. **The silent upgrade.** Writing "associated with" in one sentence and
   "impact" or "effect" in the next. Each stronger word is a claim your design
   must actually buy.
4. **Uncertainty deferred to later.** "I'll add the interval at the pilot." The
   *plan* for uncertainty belongs here, before any number exists, so the number
   never arrives naked.
5. **Estimator–inquiry mismatch.** Declaring a causal estimand at M03 and then
   proposing an estimator that can only recover an association. The triad must
   line up end to end.

---

*Previous: [M05 — Data Strategy + Feasibility & Ethics Checkpoint](milestone_05_data_strategy_ethics.md) ·
Next: [M07 — Design Declaration + URC Abstract](milestone_07_design_declaration_urc_abstract.md) —
the whole MIDA blueprint distilled onto one page, and your first public
commitment: the conference abstract.*
