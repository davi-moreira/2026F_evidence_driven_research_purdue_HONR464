# Milestone 08 — Minimum Viable Analysis

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

Due: **Friday, October 23, 11:59 PM** (you present a 60-second first-evidence
walkthrough at the Friday studio that day — your estimate, its interval, and the
one threat you most fear).

| # | File | Description |
|---|---|---|
| 1 | **A shared Colab notebook link** *(the reproducible artifact)* | Your minimum viable analysis: a seeded notebook that reruns end to end and produces the one number you report. It carries the five-part spine below in its markdown, plus your AI Research Ledger rows. This is the graded artifact and it becomes the **reproducible Colab notebook** in your dossier. |
| 2 | **`lastname_m08_minimum_viable_analysis.pdf`** *(optional companion)* | If you prefer to write the five-part spine as a 1–2 page PDF, submit it alongside the link. The notebook link is still required, because the number has to reproduce. |

Set sharing so the instructor can open **and rerun** the notebook. Confirm the
number in your write-up matches what the notebook prints when run top to bottom.

---

## Purpose

At M7 you declared an analysis protocol. This milestone is where you run the
**smallest honest version of it** and produce your **first real estimate** — one
number, with an interval around it, that you can defend. "Minimum viable" is the
whole point: not the full analysis, but the smallest analysis that yields a
single reportable quantity, reruns from a seed, and states plainly what it can
and cannot support. A grand plan you never executed is a hope; a first estimate
you can reproduce is evidence. This milestone turns the first into the second.

The notebook this week (nb08, *Experimental Causal Research*) built exactly this
muscle on a real get-out-the-vote experiment: it named the **potential outcomes**
Y(1) and Y(0) behind a causal claim, estimated an **average treatment effect** as
a difference in means, put a **randomization-inference** interval around it, read
a **power** curve to see the smallest effect the design could catch, and watched
**attrition, noncompliance, and spillover** each change which units and which
quantity the number honestly described. Its Project Transfer cell hands you the
five-piece spine below. Your job at M8 is to run that spine on **your own**
question.

Not everyone is randomizing. If your project is descriptive, predictive, or
observational-causal, you still report one estimate with an interval, still read
whether your design could catch the effect you expect, and still name the nearest
threat — which for a non-randomized design is usually a **confounder**, a third
trait that pushes on both who gets treated and the outcome. The pathway changes
the machinery; the discipline stays the same.

> **A question that often comes up here:** *"I do not have all my data yet. How
> can I report a real estimate?"* Report the estimate your **available** data can
> support, and label its reach honestly. A minimum viable analysis on a pilot
> slice, a first wave, or a public dataset stand-in is real evidence as long as
> the number reproduces and you say exactly what it speaks for. What is forbidden
> is a number with no path back to data, or a claim wider than the slice you ran.

## Components

### 1. The quantity your estimate targets

Name, in plain words, the quantity your number is trying to hit. For a causal
project, write the **potential outcomes** Y(1) and Y(0) for one unit in your
study — the outcome under treatment and the outcome without it — and mark which
one your data actually observe. (You never see both for the same unit; that gap
is why an average is what you estimate.) For a descriptive or predictive project,
name the equivalent target: the quantity your estimate is a stand-in for (a
population mean, a rate, a predicted value for unseen cases).

State this before any number appears, so the reader knows what the estimate is
supposed to be, not just what it turned out to be.

### 2. The minimum viable estimate and its interval

Report the **one number** your analysis produces — a **difference in means**, or
your pathway's equivalent — computed in a **seeded** notebook (`SEED = 464`), so
anyone who reruns it gets the same figure. Attach uncertainty: a
**randomization-inference interval** (re-randomize under the null and read the
spread) if you randomized, or the standard interval your pathway uses. Read the
number in one sentence: what it says, and whether the interval excludes the value
that would mean "no effect / no difference."

- **Example (grounded in the week's work).** "Re-running my notebook, the treated
  wards turned out about +3.4 points higher, and the randomization interval runs
  from +1.9 to +4.8, so it clears zero."
- **Non-example.** A number pasted from a chat window with no code that produces
  it. If the notebook does not compute it, it is not your estimate.

### 3. The power / adequacy read

Say whether your design is **realistically powered** for the effect you expect —
whether it is large enough to catch that effect if it is real, or so small that a
null result would tell you nothing. The week's power curve showed that a study of
50 per arm misses even a sizable effect most of the time. If your design is
underpowered, that is not a failure to hide; it is a finding that changes **how
you word your result**. State the wording change in one sentence (for example, "I
report this as suggestive, not confirmatory, because my interval is too wide to
rule out a null").

### 4. The nearest threat, and how your analysis handles or bounds it

Name the **single threat closest to your design** and say what your analysis does
about it. Choose from the threats the week taught:

- **Attrition** — units drop out in a way tied to the outcome, so the survivors
  are a selected group and the estimate bends.
- **Noncompliance** — assigned-to-treat units do not take the treatment, diluting
  the **intent-to-treat** estimate toward zero.
- **Spillover** — treatment leaks from treated units onto controls, shrinking the
  measured effect.
- **Multiplicity** — testing many outcomes and reporting the one that "worked,"
  which finds a false winner by chance.
- **Confounding** — for a non-randomized design, a third trait driving both the
  treatment and the outcome.

Pick the one nearest your design, say why it is the nearest, and state how your
analysis **handles it** (a fix) or **bounds it** (an honest limit on the claim).
One threat, faced squarely, beats five named and none addressed.

### 5. The quantity sentence and the overclaim you forbid

Write **two sentences**.

- **The quantity sentence**: exactly what your estimate means and **for whom** —
  the units and the population it speaks for (for example, "the intent-to-treat
  effect for everyone assigned," or "the average difference among the wards in my
  frame"). Name the group before you name the effect.
- **The overclaim you forbid**: the tempting sentence that would quietly widen
  your estimate to units or a population it does not cover, or upgrade a
  difference into a proven cause without a new license. Name it so a careless
  reader (or a future you) cannot slip into it.

> **A question that often comes up here:** *"Isn't stating the forbidden
> overclaim just admitting my study is weak?"* The opposite. A reader trusts a
> number more, not less, when the researcher has already drawn its edges. The
> overclaim you forbid is the one a skeptic would have used against you; naming it
> first is how you keep control of what your evidence is allowed to say.

### 6. AI Research Ledger rows

Every use of AI in building this analysis gets a row in your **AI Research
Ledger** (the eight-field table: task delegated · tool used · prompt · output
summary · decision · verification method · remaining concern · responsible
researcher). Writing the interval code, explaining a power result, or critiquing
your quantity sentence are all delegable tasks, and each one needs a row that
names how you verified the result. "No AI used" is a legitimate entry if it is
true.

**A missing ledger is not a minor lapse.** Per the course rule, a missing AI
Research Ledger entry scores the Craft criterion **0** and the submission is
**returned** for completion before it is graded.

### 7. Dossier update line

End with one line recording what this milestone finalizes in your **Research
Project Dossier**: your **reproducible Colab notebook** now exists and produces a
first estimate with an interval, and your **claim–evidence table** carries its
opening row (the claim your number supports, the evidence, the verification, the
boundary). Name the file or section where each now lives.

---

## Submission Expectations

| Item | Specification |
|---|---|
| **Reproducibility** | The reported number reruns from the seeded notebook top to bottom; the figure in your write-up matches what the notebook prints. A number that does not reproduce is not evidence. |
| **Length** | The five-part spine + ledger rows (typically the notebook's markdown, or an equivalent 1–2 page PDF companion) |
| **Presentation** | 60-second first-evidence walkthrough at the Friday studio (Oct 23): your estimate, its interval, the nearest threat; a partner and an assigned GenAI Studio reviewer red-team it — part of the grade |
| **Style** | Plain language; every technical term used as defined above; the quantity sentence and the forbidden overclaim stated as two explicit sentences |
| **Filename** | A shared Colab link (required); optional `lastname_m08_minimum_viable_analysis.pdf` |
| **Location** | Brightspace → Assignments → M08 |

---

## Grading Rubric (100 points)

Four bands on the course's five shared virtues (`planning/ASSESSMENT_ARCHITECTURE.md`).

| Criterion | Exemplary | Proficient | Developing | Beginning |
|---|---|---|---|---|
| **Compass / pathway alignment** (20) | The estimate matches the declared compass position and design pathway; the quantity targeted (potential outcomes or pathway equivalent) is named before the number and stays inside the claim boundary (18–20) | Estimate matches the pathway; the quantity named but one link to the declared position thin (14–17) | Estimate present but drifts from the declared pathway, or the target quantity never named (8–13) | The number answers a different question than the project declared, or no target quantity is stated (0–7) |
| **Evidence integrity** (20) | Every source, dataset, and measure is real and retrievable; every number traces to a line of code the reader can find (18–20) | Real and traceable; one provenance link thin (14–17) | A dataset or measure asserted without a locatable source, or one number hard to trace (8–13) | A cited source or dataset that does not exist, or a number with no path back to data (0–7) |
| **Verification** (25) | The reported number reruns from the seeded notebook and is confirmed by a named cross-check (recompute, alternative code, self-check cell); every AI-assisted step has a ledger row with a non-vague verification method (22–25) | Number reproduces; one cross-check or one ledger verification loose (18–21) | Number reproduces but no independent cross-check named, or AI outputs used with verification unnamed (11–17) | The number does not rerun from the notebook, or an AI-written result is reproduced with no verification (0–10) |
| **Uncertainty & limitations** (25) | The interval is reported and read correctly; the power/adequacy read is honest; the nearest threat is faced with a fix or an explicit bound; the quantity sentence and the forbidden overclaim are both precise (22–25) | Interval, power read, threat, and both sentences present; one stated loosely (18–21) | Interval reported but no power read, or the threat named without handling, or only one of the two boundary sentences (11–17) | No interval, or the estimate reported as certain, or the number silently upgraded to a wider population or to proven cause (0–10) |
| **Craft & AI Research Ledger** (10) | On-format, on-time, clear 60-second walkthrough, complete AI Research Ledger, dossier line present (9–10) | Minor format lapses; ledger complete (7–8) | Missing pieces or a rushed walkthrough (4–6) | Missing AI Research Ledger (Craft scored 0, submission returned) (0–3) |

**Hard caps (a single failure caps the row regardless of the rest):**

- A **fabricated or unretrievable source** caps *Evidence integrity* at Beginning.
- An **untraceable number** — a figure with no path back to your data — caps
  *Verification* at Beginning.
- A **non-reproducing result** — the reported number does not rerun from your
  seeded notebook — caps *Verification* at Beginning.
- A **missing AI Research Ledger entry** scores *Craft & AI Research Ledger* **0**
  and the submission is **returned** unread until it is supplied.

**Revision:** eligible under the standing policy — a revised submission within 7
days of feedback recovers up to half the lost points.

## Penalties

- Late: −10 points per day, up to 3 days; not accepted after (documented
  emergencies: talk to me first, per the syllabus).
- Any source, dataset, or measure you cite that turns out not to exist or not to
  say what you claim: *Evidence integrity* scores Beginning regardless of the
  rest — the course's evidence-integrity rule with teeth.
- A reported number that does not reproduce from your seeded notebook:
  *Verification* scores Beginning — a number you cannot regenerate is not
  evidence.
- Missing AI Research Ledger entry: *Craft & AI Research Ledger* scores 0 and the
  submission is returned for completion before grading.

## Common Pitfalls

1. **The number with no notebook.** Reporting an estimate that lives in a chat
   reply or a mental calculation, with no seeded code that produces it. If the
   notebook does not compute it on a rerun, it is not your estimate, and it caps
   your Verification score. Put every reported figure behind a line of code.
2. **The naked point estimate.** Reporting "+3.4 points" with no interval and no
   power read, as if one number settled the question. A minimum viable analysis
   is the estimate **and** its uncertainty; a point with no interval hides how
   little (or how much) the data actually pin down.
3. **The silent upgrade.** Writing a quantity sentence about the units your data
   reach, then walking away with a claim about a whole population or a proven
   cause you never licensed. Name the forbidden overclaim in writing so you catch
   it in your own draft before a reviewer catches it for you.

---

*Previous: [M07 — Declared Analysis Protocol](milestone_07_declared_analysis_protocol.md) ·
Next: [M09 — Poster Draft 1 & Research Audit](milestone_09_poster_draft_research_audit.md) —
your first estimate becomes the headline a poster draft must defend and a
four-part research audit tries to break.*
