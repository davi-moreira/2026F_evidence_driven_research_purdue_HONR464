# Milestone 19 — Poster-to-Dossier Module

## About the Research Project

Your semester project is **individual**: one researcher, one question, carried
from curiosity to a defended, reproducible claim. It runs through milestones
M00–M23, peaks publicly at the **Purdue Fall Undergraduate Research Expo
poster session (Tuesday, November 17 — required)**, and closes with an oral
**Evidence Defense** and a final research dossier in December. Every milestone
follows the same cadence: **develop in class → present → submit → revise**.
Milestone weights and the revision policy are in the syllabus; instructions
and rubrics live one page per milestone, like this one.

This milestone is the **analytical core of the post-conference research
dossier** and is worth **5% of the course grade** (the dossier component splits
into M19 5%, M20 5%, M21 4%, and the M23 final dossier 6%). It is
**revision-eligible** under the standing policy.

---

## What to Submit on Brightspace

This is the **async module** (async meeting **Mon Nov 23**; notebook **nb17** is
fully self-contained). The deadline falls **after Thanksgiving** so the break is
yours.

Due: **Monday, November 30, 11:59 PM.**

| # | File | Description |
|---|---|---|
| 1 | **`lastname_m19_dossier_core.pdf`** | Your two sensitivity checks, the claim ledger, and the methods+findings skeleton, plus your AI-use disclosure block. |
| 2 | **Updated notebook** (`.ipynb`) | nb17 with your approach-branch sensitivity cells executed on your own pilot. |

*(You also make one async-board post and one reply — see Component 4.)*

---

## Purpose

Your poster compressed the truth to fit a board. The dossier must carry **all**
of it — and to a **higher standard than the poster**. The poster could show a
number; the dossier must show that the number survives being pushed on. This
module does two things at once. First, it runs **sensitivity checks** — the same
finding, recomputed under a defensible alternative choice, to see whether it
holds or wobbles. Second, it builds the **claim ledger**: the spine of every
December artifact, where **every claim you made on the poster gets a row** and
no claim ports forward without being re-verified. The rule that governs this
whole phase: **nothing moves from poster to dossier on trust.** A claim that was
fine on a poster and dissolves under one sensitivity check was never as solid as
the poster made it look — and better you learn that now than at the Evidence
Defense.

## Components

### 1. Two approach-appropriate sensitivity checks (run on your own pilot)

Run **two** sensitivity checks that match your declared approach's branch. Do
them on **your own pilot data**, and record what moved and what didn't:

- **Description** — recompute a headline summary under an **alternative summary
  or binning** (mean vs median; a different bin cut; including vs excluding an
  ambiguous category). Does the pattern survive the choice?
- **Inference** — probe an **alternative specification** and a **non-response /
  missingness** scenario. Does the estimate — and its uncertainty — hold?
- **Prediction** — perturb the **train/test split** (a different seed or fold)
  and swap the **metric**. Does the out-of-sample story survive?
- **Causal** — run an **assumption probe** (a placebo/negative-control check, a
  sensitivity-to-confounding argument, or a bounding exercise). Does the
  identification story hold, or does it depend on an assumption you can't
  defend?

Record, for each check: what you changed, what the result did, and what that
tells you about how firm the claim is.

### 2. The claim ledger

Every claim your poster made gets **one row**. Five columns, each filled
honestly:

| Column | What goes here |
|---|---|
| **Claim** | The statement, worded to its real boundary (units, scope, approach) |
| **Evidence** | Where it comes from — the specific cell/table/output |
| **Verification** | How you checked it (recomputed, cross-checked, triangulated) |
| **Boundary** | What the claim does **not** say (no generalization/causation it can't support) |
| **Survived sensitivity?** | Yes / partly / no — with what the check did |

**Strong row (concrete example):** *Claim — "In my 320 pilot responses, 61% of
first-generation respondents reported skipping office hours at least once, vs
43% of continuing-generation respondents." Evidence — pilot tabulation, nb17
cell 14 (195/320 and 137/320). Verification — recomputed the two proportions by
hand from the raw counts; confirmed the group Ns sum to 320. Boundary —
descriptive; these 320 respondents only; not "first-generation undergraduates avoid
office hours." Survived sensitivity? — Yes; the 18-point gap held at 15 points
when I re-binned "ever skipped" to "skipped weekly or more."*

**Weak row (non-example):** *Claim — "First-gen undergraduates avoid office hours."
Evidence — "my data." Verification — (blank). Boundary — (blank). Survived
sensitivity? — "yes."* No units, no source cell, no boundary, a generalization
the pilot can't support, and a sensitivity verdict asserted rather than shown.
This row would not survive the Evidence Defense — fix it here.

### 3. The methods + findings skeleton (drafted from the ledger)

Draft the **skeleton** of the dossier's methods and findings sections, built
directly from the ledger rows. Methods says what you did and why (approach,
data, key decisions); findings reports each surviving claim at its real
boundary. A methods section is not a methods *memory* — it records decisions so
a stranger could follow them, not just what you happened to remember.

### 4. The async-board exchange

On the module board: **post your ledger's most fragile row** (the claim you're
least sure survives), and **write one shoring reply** to a classmate — a
sensitivity check or verification that could firm up *their* fragile row.
Posting your weakest claim in public is the habit; hiding it is the failure.

### 5. AI-use disclosure block (required on every deliverable)

A short table: which AI tool(s) you used, for what task (locate / draft /
critique / none), and how you verified the output. "No AI used" is a fine
entry; an undisclosed AI contribution is an academic-integrity violation.

---

## Submission Expectations

| Item | Specification |
|---|---|
| **Length** | PDF: two sensitivity checks (what moved) + the claim-ledger table + the methods/findings skeleton, plus the disclosure block |
| **Notebook** | nb17 with your approach-branch cells executed; outputs visible |
| **Board** | One fragile-row post + one shoring reply (checked for completion) |
| **Style** | The ledger is a real table; every "survived sensitivity?" verdict is backed by a check you actually ran |
| **Filenames** | `lastname_m19_dossier_core.pdf` + updated `.ipynb` |
| **Location** | Brightspace → Assignments → M19 |

---

## Grading Rubric (100 points)

| Criterion | Exemplary | Proficient | Developing | Beginning |
|---|---|---|---|---|
| **Approach alignment** (20) | Both checks are the right ones for the declared approach's branch and stay inside its claim boundary (18–20) | Checks fit the approach; one boundary loosely held (14–17) | One check mismatched to the approach (8–13) | Checks unrelated to the approach, or approach ignored (0–7) |
| **Sensitivity execution & evidence integrity** (25) | Both checks run on the real pilot; what moved is recorded; claims re-verified, not ported (22–25) | Checks run; recording of movement thin in places (18–21) | One check run, or results asserted without output (11–17) | Checks not actually run, or poster numbers copied unverified (0–10) |
| **Claim ledger completeness & honesty** (25) | Every poster claim has a row; all five columns filled; boundaries and fragility honest (22–25) | Most claims laddered; a column occasionally thin (18–21) | Ledger partial or boundaries missing on key rows (11–17) | No ledger, or a table of claims with no verification/boundary (0–10) |
| **Methods/findings skeleton & uncertainty** (15) | Skeleton built from the ledger; findings carry their uncertainty and boundary (13–15) | Skeleton present; uncertainty lightly carried (10–12) | Skeleton is a claims restatement without decisions (6–9) | Missing, or contradicts the ledger (0–5) |
| **Async-board citizenship** (5) | Genuinely fragile row posted + a substantive shoring reply (5) | Post + reply present, one thin (3–4) | Only one of the two (1–2) | Neither (0) |
| **Craft & disclosure** (10) | On-format, on-time, notebook runs, complete AI-disclosure block (9–10) | Minor lapses (7–8) | Sloppy table/notebook or missing pieces (4–6) | Missing disclosure block (0–3) |

**Revision:** eligible under the standing policy — a revised PDF within 7 days
of feedback recovers up to half the lost points.

## Penalties

- Late: −10 points per day, up to 3 days; not accepted after (documented
  emergencies: talk to me first, per the syllabus).
- A "survived sensitivity? — yes" verdict with no check behind it is an
  evidence-integrity violation: the Sensitivity criterion scores Beginning
  (0–10) regardless of the rest.
- Any claim ported from the poster without re-verification, once found, drops the
  Claim-ledger criterion to Developing or below.
- Missing AI-disclosure block: Craft scores 0 and the submission is returned
  for completion before grading.

## Common Pitfalls

1. **Porting on trust.** The whole module exists because poster claims must be
   re-verified. Copying a number forward because it "was already checked" is the
   error to avoid.
2. **The cosmetic sensitivity check.** Re-running the identical analysis and
   calling it robustness proves nothing. The check has to *change something*
   defensible.
3. **Hiding the fragile row.** The board post is supposed to be your weakest
   claim. A safe post wastes the one place classmates can shore you up.
4. **Rows without boundaries.** A ledger row with an empty Boundary column is a
   claim with no edge — exactly what the Evidence Defense will push on.
5. **Methods as memory.** "I filtered the data" is a memory; "I dropped the 11
   responses with no consent timestamp, logged in cell 6" is a method.

---

*Previous: [M18 — Feedback-to-Redesign Plan](milestone_18_feedback_redesign_plan.md) ·
Next: [M20 — Reproducibility Audit](milestone_20_reproducibility_audit.md) — a
classmate tries to rebuild your headline number from your package alone, and
signs off if they can.*
