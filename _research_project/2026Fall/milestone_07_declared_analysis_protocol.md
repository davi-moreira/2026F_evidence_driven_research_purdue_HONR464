# Milestone 07 — Declared Analysis Protocol

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

Due: **Friday, October 16, 11:59 PM** (you present a 3-minute protocol walkthrough
at that day's Friday studio, and a partner plus an assigned AI reviewer cross-review
it — part of the grade).

| # | File | Description |
|---|---|---|
| 1 | **`lastname_m07_analysis_protocol.pdf`** *or* a shared Colab notebook link | The declared analysis protocol below: your prediction verdict (the four-part contract, or a defended reason prediction is the wrong question), your leakage trace, your honesty-check plan with retract triggers, your one-sentence claim boundary, your Prediction & Leakage Auditor critique with your written fixes, and your AI Research Ledger rows. This is the graded artifact. |

If you submit a notebook link, set sharing so the instructor can open it, and make
sure any cell you reference actually runs.

---

## Purpose

A **declared analysis protocol** is a written statement of exactly how you will
analyze your data, fixed **before you touch it**. Writing it early is not
bureaucracy. It is the one move that stops a result from being reverse-engineered
into a flattering method. Once you have seen which model or which metric happens to
win on your data, you can no longer honestly claim you would have chosen it anyway.
Declaring the plan first is how you keep that honesty.

This milestone is where the prediction week (Topic 07) becomes your own project's
spine. Prediction is one of the four compass positions, and it is the one most
likely to fool you: a score can look impressive because the model quietly read the
answer, not because it learned anything. So the protocol you declare has to say, in
order, what you are predicting, the dumbest honest rule you must beat, how you will
hold out an honest test, how you will keep score, and how you will catch a fake win
before you report it.

Not every project predicts, and that is fine. If your real question is description,
generalization, or a cause, your protocol says so, names the design that actually
answers it, and confirms it makes **no unlicensed prediction claim**. Deciding that
prediction is the wrong tool is a real, gradable finding — you are judged on the
reasoning behind the verdict, not on whether the verdict is "yes."

> **A question that often comes up here:** *"My project is descriptive (or causal).
> Why am I writing a prediction protocol?"* Because the same discipline protects
> every design. The habit you are practicing is declaring your analysis before the
> data can tempt you, and naming the boundary your evidence stops at. A causal
> project still has to rule out a measure that quietly contains its own outcome; a
> descriptive project still has to keep its language inside the reach its sample
> bought. The prediction spine is the sharpest place to learn the move, and the
> **Prediction & Leakage Auditor** confirms your protocol claims nothing your design
> cannot buy, whichever position you declared.

## Components

### 1. The prediction verdict

State whether your project has a real prediction question. A **prediction** is a
best guess about a case whose outcome you cannot see yet, an **unseen case**. It is
descriptive, not causal: it forecasts *who* or *what*, never *why*.

**If yes**, write the four-part **contract**, in order, because the order is not
negotiable:

- **Target** — the one thing you are predicting, a single column named before
  anything else.
- **Baseline** — the dumbest honest rule you must beat, usually "always guess the
  most common answer." If 60% of cases are "yes," always guessing "yes" scores 60%
  for free, so 60% (the **base rate**) is the bar. A score with no baseline beside
  it is not yet an achievement.
- **Split** — how you divide your rows into a **training set** the model learns from
  and a **held-out set** it never touches during training. The held-out set is your
  only honest exam.
- **Metric** — how you keep score, chosen to match the target. Accuracy works when
  the classes are roughly balanced and lies when one outcome is rare. When one error
  costs more than the other, name the metric from the **confusion matrix** that fits
  the decision (for example, **recall** on the class you are trying to catch, or
  **precision** on the class you flag).

**If no**, write one sentence on why prediction is the wrong question for your
project, name the question it really asks (description, generalization, or a cause)
and the design that answers it, then name the too-good-to-be-true trap nearest your
approach — a measure that quietly contains its own outcome — and your check for it.

### 2. The leakage trace

**Data leakage** is a feature that carries information you would not actually have
at the moment you need the forecast; its value is only settled at or after the
outcome it is supposed to predict. In the book's declare-diagnose-redesign grammar,
leakage is a **data-strategy violation**: the plan for how evidence comes to exist
quietly let the answer sneak into the inputs.

Name the one feature (or measure) in your data whose value could be settled at or
after your outcome, and the two checks that rule it out:

- **The timing check** — is the feature's value known *before* the prediction
  moment, or only settled *at or after* the outcome? Timing, not accuracy, decides.
- **The correlation check** — does the suspect feature track the outcome so tightly
  it is almost a copy of the answer?

A feature that fails the timing check is dropped or re-timed, no matter how much it
helps the score. A leak inflates the score on *this* data and collapses on *new*
data, because the leaky value will not exist when you actually need a forecast.

### 3. The honesty checks and their retract triggers

A single held-out number is a start, not a verdict. Name which of the five checks
apply to your design, and for each one you will run, the result that would make you
**retract** the claim:

- **Overfitting** — a large gap between a high training score and a low held-out
  score, meaning the model memorized rows instead of learning a pattern that
  carries.
- **Cross-validation** — several held-out scores instead of one lucky split; the
  win has to survive the average, not ride on one draw.
- **Calibration** — whether the model's stated probabilities mean what they say
  (among the cases it calls 70% likely, about 70% actually happen).
- **Subgroup performance** — the metric checked separately within groups that
  matter, so a good overall score cannot hide a group the model fails.
- **Distribution shift** — whether the cases you deploy on differ from the cases you
  trained on, which is where a fair-looking model degrades in the real world.

Then state your **model-selection rule**: the written standard for keeping or
rejecting a model, fixed *before* you see which one you happen to like (for example,
"keep a model only if it beats the baseline under cross-validation and survives the
leakage check"). Finish by naming the criteria under which you would declare the
analysis **not useful** — it does not beat the baseline out-of-sample, the win
vanishes under cross-validation, the win depends on a leaked feature, it is badly
calibrated, or it fails on the subgroup or shifted population you care about. A
"not useful" verdict, honestly reached, earns full credit.

### 4. The claim boundary

Write **one sentence**: the exact forecast or finding your protocol would license,
worded to stop where your evidence stops, carrying its **uncertainty** — the
cross-validation spread, a subgroup gap, or the distribution-shift boundary. Then
name the crossing your protocol does **not** license.

The forbidden crossing for a prediction is reading a cause off the model. **Interpretability**
is noticing which features a model leaned on. **Explanation** is knowing what
actually causes the outcome. They are not the same, and a leak can fake the first
while telling you nothing about the second. State, in writing, that you make **no
causal reading of any weight**: prediction answers *who*, never *why*.

> **A question that often comes up here:** *"How is a claim boundary different from
> just reporting my result?"* A result that respects its boundary names the baseline
> it beat, the margin, and the uncertainty, and stops there. An overclaim keeps the
> confident tone but swaps in a bigger subject: "my model scores 0.65 held-out"
> becomes "my model predicts turnout," or "the top feature is X" becomes "X drives
> the outcome." Nothing in the wording flags that the reach just grew. Catching that
> upgrade in your own draft, and forbidding it in writing, is the skill this
> milestone grades.

### 5. Prediction & Leakage Auditor critique, with your fixes

Submit your protocol to the **Prediction & Leakage Auditor** (the required GenAI
Studio reviewer role for M7; full briefing in
`genai_studio/roles/prediction_leakage_auditor.md`). Paste its **leakage trace** and
its **held-out and baseline check**, and for every flag it raises, write your fix:
the leak you traced and dropped, the baseline you added, or the reason a flag does
not apply in your pipeline. A purely descriptive or causal project still runs the
auditor to confirm it makes **no unlicensed prediction claim**, and that
confirmation is itself the ledgered result.

Then name **one recompute**: the single number you would recompute yourself to check
any AI or collaborator, and how you would do it (recompute by hand, alternative
code, or a primary-source read). The auditor can miss a real leak or invent a false
one, so the trace it returns is a set of hypotheses to test in your own pipeline,
not a verdict.

### 6. AI Research Ledger rows

Every use of AI in building this protocol gets a row in your **AI Research Ledger**
(the eight-field table: task delegated · tool used · prompt · output summary ·
decision · verification method · remaining concern · responsible researcher).
Widening a leakage-suspect list, drafting the contract's wording, and running the
Prediction & Leakage Auditor are all delegable tasks, and each one you delegated
needs a row that names how you verified the result. "No AI used" is a legitimate
entry if it is true.

**A missing ledger is not a minor lapse.** Per the course rule, a missing AI
Research Ledger entry scores the Craft criterion **0** and the submission is
**returned** for completion before it is graded.

### 7. Dossier update line

End with one line recording what this milestone finalizes in your **Research Project
Dossier**: your declared-analysis-protocol component now carries a prediction verdict
(the four-part contract or a defended non-prediction verdict), a leakage trace, an
honesty-check plan with retract triggers, and a one-sentence claim boundary. Name the
file or section in your dossier where each now lives.

---

## Submission Expectations

| Item | Specification |
|---|---|
| **Length** | The seven-part protocol + ledger rows (typically 2–4 pages PDF, or the equivalent notebook sections) |
| **Order** | The contract stated in order (target → baseline → split → metric), or the defended non-prediction verdict; the boundary as one explicit sentence with its uncertainty |
| **Presentation** | 3-minute protocol walkthrough at the Friday studio (Oct 16); a partner and the Prediction & Leakage Auditor cross-review your leakage trace and claim boundary — part of the grade |
| **Style** | Plain language; every technical term used as defined above; no causal reading of any model weight |
| **Filename** | `lastname_m07_analysis_protocol.pdf` (or a shared Colab link) |
| **Location** | Brightspace → Assignments → M07 |

---

## Grading Rubric (100 points)

Four bands on the course's five shared virtues (`planning/ASSESSMENT_ARCHITECTURE.md`).

| Criterion | Exemplary | Proficient | Developing | Beginning |
|---|---|---|---|---|
| **Protocol correctness & compass/pathway alignment** (30) | The four-part contract stated in order (or a defended non-prediction verdict + the design that answers the question); the leakage timing check present; the five honesty checks named with retract triggers; a model-selection rule fixed before the scores; protocol stays inside its claim boundary (26–30) | Contract and checks correct; one step or one retract trigger thin or under-argued (21–25) | Contract present but out of order, a honesty check missing, or the model-selection rule chosen after peeking (13–20) | No baseline, no held-out split, or a protocol whose method was reverse-engineered from the result (0–12) |
| **Evidence integrity & provenance** (15) | Every dataset, feature, and source is real and retrievable; each feature's measurement-timing traces to its origin (13–15) | Real and traceable; one provenance or timing link thin (10–12) | A claimed feature or source asserted without a locatable origin (5–9) | A cited source, dataset, or feature that does not exist or is not what you claim (0–4) |
| **Verification of AI-assisted parts** (20) | Every AI-assisted step is ledgered with a named, non-vague verification; the Prediction & Leakage Auditor's trace is pasted with your written fix for each flag; the one recompute is named and real (18–20) | Ledger present; one verification vague or one auditor flag unaddressed (14–17) | Ledger thin; AI outputs used but verification not named, or a flagged leak waved past (8–13) | AI output reproduced without any verification, or a leak flagged and left in the protocol (0–7) |
| **Uncertainty & claim boundary** (20) | The one-sentence boundary carries its uncertainty (cross-validation spread, subgroup gap, or shift boundary); the forbidden crossing named; no causal reading of any weight (18–20) | Boundary present; uncertainty or the forbidden crossing stated loosely (14–17) | A boundary with no uncertainty, or a score reported without the baseline it beat (8–13) | No boundary, an overclaimed certainty, or a cause read off a model weight (0–7) |
| **Craft, ledger & communication** (15) | On-format, on-time, clear 3-minute walkthrough, complete AI Research Ledger, dossier line present, active cross-review (13–15) | Minor format lapses; ledger complete (10–12) | Missing pieces or a rushed walkthrough (5–9) | Missing AI Research Ledger (Craft scored 0, submission returned) (0–4) |

**Hard caps (a single failure caps the row regardless of the rest):**

- A **fabricated or unretrievable source** caps *Evidence integrity & provenance*
  at Beginning.
- An **untraceable number** — a reported figure with no path back to your data —
  caps *Verification of AI-assisted parts* at Beginning.
- A **non-reproducing result** — a headline metric that does not rerun from your
  protocol or notebook — caps *Verification of AI-assisted parts* at Beginning.
- A **missing AI Research Ledger entry** scores *Craft, ledger & communication*
  **0** and the submission is **returned** unread until it is supplied.

**Revision:** eligible under the standing policy — a revised submission within 7
days of feedback recovers up to half the lost points.

## Penalties

- Late: −10 points per day, up to 3 days; not accepted after (documented
  emergencies: talk to me first, per the syllabus).
- Any dataset, feature, or source you cite that turns out not to exist or not to be
  what you claim: *Evidence integrity & provenance* scores Beginning regardless of
  the rest — the course's evidence-integrity rule with teeth.
- Missing AI Research Ledger entry: *Craft* scores 0 and the submission is returned
  for completion before grading.

## Common Pitfalls

1. **The protocol reverse-engineered from the result.** Fitting several models,
   seeing which one wins, and then writing the "declared" plan to match it. The
   whole value of declaring first is that the method cannot be chosen to flatter the
   answer. Fix the target, baseline, split, and metric before you touch the data,
   and write the model-selection rule before you see a single score.
2. **The leaky feature waved past.** Listing a feature settled at or after your
   outcome and calling its timing "probably fine" without the check. Leakage inflates
   the score on your data and collapses on new cases. Run the timing check and the
   correlation check, and drop or re-time any feature that fails.
3. **The score reported without its baseline or its boundary.** A metric with no
   dumb rule beside it and no claim boundary is an overclaim wearing a lab coat. Name
   the baseline your model must beat, end with the one sentence your evidence
   licenses and its uncertainty, and make no causal reading of any weight.

---

*Previous: [M06 — Experimental Measurement or Data-Acquisition Protocol + URC Abstract internal gate](milestone_06_experimental_measurement_protocol.md) ·
Next: [M08 — Minimum Viable Analysis](milestone_08_minimum_viable_analysis.md) —
your declared protocol meets the data for the first time, and you run it end to end
to produce first evidence before the poster phase begins.*
