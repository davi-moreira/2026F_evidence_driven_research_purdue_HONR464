# Milestone 05 — Causal Identification Strategy or Causal-Language Boundary

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

Due: **Friday, October 2, 11:59 PM**. That Friday is the course's **async
module**: there is no class meeting, and you complete this milestone on your own
time. In place of a live studio pitch, you record a **90-second causal-strategy
statement** and post it to the Brightspace discussion board by the same
deadline. On the board, a partner and the assigned **Causal Identification
Skeptic** GenAI Studio reviewer red-team your identification argument (the
async board red-team); you reply with your resolutions. The written document is
what is graded.

| # | File | Description |
|---|---|---|
| 1 | **`lastname_m05_causal_identification.pdf`** *or* a shared Colab notebook link | The six-part deliverable below: your causal question and estimand, your confounding causal diagram (image), your identification argument **or** your honest causal-language boundary, the Causal Identification Skeptic critique with your written resolutions, your one recompute, and your AI Research Ledger rows. This is the graded artifact. |

If you submit a notebook link, make sure sharing is set so the instructor can
open it, and that the causal-diagram figure renders when the notebook is run.

---

## Purpose

Last week you audited what your data can plainly **describe**, and you drew the
boundary that description cannot cross. This week you meet the hardest word in
research: **because**. A **causal question** asks what would change if you
intervened, not just what goes with what. This milestone decides, honestly and
in writing, whether your project earns that word.

You do one of two things, and you do exactly one of them for real:

- If your setting gives you leverage — an argument that your comparison isolates
  the effect and not something else — you write an **identification argument**
  and hand it to a skeptic to attack.
- If it does not, you write the **causal-language boundary**: the sentence that
  keeps your claim on the honest *associated with* side of the line, and names
  the confounder you cannot rule out.

Both outcomes are passing outcomes. What is *not* passing is **design mimicry**:
borrowing the vocabulary of a causal method to decorate a comparison whose one
untestable assumption was never stated or probed. Writing "difference-in-
differences" does not make parallel trends true; calling something a "natural
experiment" does not make the assignment as-if random. The word *because* is
earned by an argued and probed assumption, never by the name of a method.

> **A question that often comes up here:** *"What if my project turns out to be
> descriptive or predictive, not causal at all?"* Then your deliverable is the
> causal-language boundary, and writing it well is a full-credit answer. Most
> honors projects this semester will land here, and that is correct, not a
> shortfall. The failure this milestone catches is not "my design is only
> descriptive." It is "my design is only descriptive, but my sentences quietly
> say *because* anyway." Catch that in your own draft before a skeptic does.

## Components

Draft every piece yourself first. AI may critique what you wrote afterward, and
the Causal Identification Skeptic is a required reviewer, but the strategy you
submit has to be reasoned by you. Whether your design earns a causal claim is a
never-delegate decision.

### 1. The causal question and estimand

State three things, one line each.

- **Treatment** — the thing being tested, the intervention whose effect you want
  (for example, *making the Hajj pilgrimage*, *joining a mentoring program*).
- **Outcome** — what you measure afterward (for example, *views toward
  outsiders*, *first-year retention*).
- **Estimand** — the exact quantity you are after, written down before you
  compute anything: the **average causal effect** of the treatment on the
  outcome, the average of Y(1) minus Y(0) across your group. Y(1) is the outcome
  with the treatment, Y(0) the outcome without it. Naming the estimand keeps you
  honest about what number would actually answer your question.

Then, in one sentence, name the **counterfactual** at the heart of the claim:
the outcome that would have happened under the choice a treated unit did *not*
make, which you never observe. This is the **fundamental problem of causal
inference**, and naming it is what forces the rest of the deliverable.

### 2. The confounding causal diagram

Draw the arrows among your **treatment**, your **outcome**, and the one
**confounder** you most fear. A **confounder** is a third factor that pushes on
*both* who gets the treatment and the outcome (for example, a health-conscious
lifestyle drives both a coffee habit and a longer life). When it points into
both, it opens a **back door**: a path connecting treatment and outcome that
runs through the confounder instead of through a real effect, manufacturing
correlation that is not cause.

Your diagram must show, at minimum: the arrow from treatment to outcome you want
to estimate, and at least one confounder with arrows into *both* treatment and
outcome. That double arrow is the whole reason the tool exists. It names the
**selection into treatment** — the process that decided who got treated — that
your identification argument must close or your boundary must confess.

Submit the diagram as an **image** (a clear hand drawing photographed, or the
notebook-generated figure from the studio notebook, edited to your project). A
diagram that draws only the treatment-to-outcome arrow and hides the confounder
has skipped the reason you drew it.

### 3. The identification argument — OR — the honest causal-language boundary

Do exactly one of these, for your real project.

**If you have leverage, write the identification argument (three sentences).**
An **identification argument** is your written reason that a comparison recovers
a causal effect, not a formula you apply. Name your leverage from what the week
taught, and it must be one you can defend:

- **Selection on observables** — you adjust for the confounders you can *see* and
  argue no unobserved confounder remains. Its assumption is exactly that: no
  hidden confounder. "We controlled for everything" is a claim to distrust,
  because controlling for the confounders you happen to observe is not the same
  as identifying the effect.
- **A natural experiment** — a chance-like force outside your control assigned the
  treatment, so assignment is **as-if random** and treated and untreated are
  comparable (a lottery, a birthday cutoff).
- **Difference-in-differences (DiD)** — compare the change over time in a treated
  group to the change in an untreated group. **Untestable assumption: parallel
  trends** — absent the treatment, the two groups would have moved in parallel.
- **Regression discontinuity (RDD)** — treatment switches on at a sharp **cutoff**,
  so units just below and just above are nearly identical. **Untestable
  assumption: as-if random at the cutoff** — nothing else jumps at the line and
  units cannot precisely nudge their own score across it.
- **Instrumental variables (IV)** — a **nudge** (an instrument) pushes some units
  toward treatment but reaches the outcome only through treatment. **Untestable
  assumption: exclusion** — the nudge touches the outcome through treatment
  alone, with no back door of its own.

Your three sentences: (1) the estimand you want; (2) why your comparison is a
valid counterfactual, naming the design and its **one untestable assumption**;
(3) what therefore follows, stated with uncertainty. An **untestable
assumption** is a claim the design depends on that the data can never confirm,
only make plausible. Name how a skeptic would attack it.

**If you have no leverage, write the causal-language boundary (one sentence).**
The **causal-language boundary** is the point past which your evidence stops
earning *because* and must switch to *associated with*. Write: "My design does
not identify an effect because [the confounder I cannot rule out], so my claim
stops at *associated with*." This is a finding, not a failure. It tells you which
assumption you would still have to defend, or that your claim belongs on the
*associated with* side of the line.

### 4. The Causal Identification Skeptic critique and your resolutions

The **Causal Identification Skeptic** (a GenAI Studio role) is a **required**
reviewer for this milestone. Paste your identification argument or your boundary
to it and ask it to attack. It returns a ranked **Threats to identification**
list and any **Language-boundary flags**. Do not accept the attack as
automatically right, and do not let it decide your design; it supplies the
attack, you supply the defense.

Then **answer every ranked threat in writing.** For each threat, either show why
your design rules it out (a lottery or a cutoff you already have) or acknowledge
it as a limitation you carry. An unanswered top threat is an open hole in your
claim. These threats and your resolutions are the required M5 content of your AI
Research Ledger (a critique-task row), and they are what the async board
red-team continues.

### 5. One recompute

Name the single number in your deliverable that you would **recompute yourself**
to check any AI's or collaborator's estimate, and say exactly how. A **recompute**
is an independent redo by a second route: the same difference computed by
hand-filtering each group and subtracting, an interval recomputed from the raw
numbers, an adjusted estimate rebuilt one step at a time. Every reported number
needs a path back to the data that produced it. **Code running without errors is
not the same as code being correct** — a cell can execute cleanly and still
compute the wrong quantity.

### 6. AI Research Ledger rows and dossier update line

Every use of AI in building this deliverable gets a row in your **AI Research
Ledger** (the eight-field table: task delegated · tool used · prompt · output
summary · decision · verification method · remaining concern · responsible
researcher). Red-teaming your causal sentence, having the Skeptic rank threats,
and asking Gemini to name a confounder you might have missed are all delegable
tasks, and each one you delegated needs a row naming how you verified the result.
"No AI used" is a legitimate entry if it is true.

**A missing ledger is not a minor lapse.** Per the course rule, a missing AI
Research Ledger entry scores the Craft criterion **0** and the submission is
**returned** for completion before it is graded.

End with one line recording what this milestone finalizes in your **Research
Project Dossier**: your MIDA declaration's **identification / assignment**
component now carries a causal question, a confounding diagram, and either a
defended identification argument or a written causal-language boundary. Name the
file or section in your dossier where each now lives.

---

## Submission Expectations

| Item | Specification |
|---|---|
| **Length** | The six-part deliverable + ledger rows (typically 2–4 pages PDF, or the equivalent notebook sections) |
| **Figure** | The confounding causal diagram as a legible image: the treatment-to-outcome arrow plus at least one confounder with arrows into both |
| **Presentation** | 90-second recorded causal-strategy statement, posted to the Brightspace board by Friday Oct 2; a partner and the Causal Identification Skeptic red-team your identification argument on the board thread (the async board red-team) — part of the grade |
| **Style** | Plain language; every technical term used as defined above; your language matched to the license your design actually holds |
| **Filename** | `lastname_m05_causal_identification.pdf` (or a shared Colab link) |
| **Location** | Brightspace → Assignments → M05 |

---

## Grading Rubric (100 points)

Four bands on the course's five shared virtues (`planning/ASSESSMENT_ARCHITECTURE.md`).

| Criterion | Exemplary | Proficient | Developing | Beginning |
|---|---|---|---|---|
| **Causal-identification correctness** (compass/pathway alignment) (30) | Question, estimand, and confounding diagram correct; the identification argument names one real untestable assumption and how a skeptic attacks it, **or** the causal-language boundary is stated with the confounder it confesses; language matches the license held (26–30) | Argument or boundary correct; one assumption or one diagram arrow thin or under-argued (21–25) | Argument or boundary present but the untestable assumption unnamed, or the confounder missing from the diagram (13–20) | Design mimicry: a causal label or the word *because* with no stated, probed assumption; or a confounder-free diagram (0–12) |
| **Evidence integrity & provenance** (20) | Every dataset, study, and number named is real and retrievable; the reader can trace each to its origin (18–20) | Real and traceable; one provenance link thin (14–17) | A claimed dataset, estimate, or study asserted without a locatable source (8–13) | A cited source, dataset, or figure that does not exist or does not say what you claim (0–7) |
| **Verification of AI-assisted parts** (20) | Every AI-assisted step (Skeptic critique, confounder brainstorm, sentence red-team) has a ledger row with a named, non-vague verification method; the one recompute is stated with its route (18–20) | Ledger present; one verification method vague, or the recompute named but its route thin (14–17) | Ledger thin; AI outputs used but verification not named, or no recompute (8–13) | An AI output or number reproduced with no verification, or an identification argument written by AI and left unchecked (0–7) |
| **Uncertainty & causal-language boundary** (20) | Uncertainty stated around the estimate; every ranked Skeptic threat answered in writing; the boundary between *because* and *associated with* drawn precisely and the language stays inside it (18–20) | Uncertainty and threats present; one threat answered loosely or one caveat stated loosely (14–17) | Some threats unanswered, or uncertainty asserted without the boundary it implies (8–13) | No uncertainty, an unanswered top threat, or causal language the design does not license (0–7) |
| **Craft, ledger & communication** (10) | On-format, on-time, clear 90-second statement, complete AI Research Ledger, dossier line present (9–10) | Minor format lapses; ledger complete (7–8) | Missing pieces or a rushed statement (4–6) | Missing AI Research Ledger (Craft scored 0, submission returned) (0–3) |

**Hard caps (a single failure caps the row regardless of the rest):**

- **Design mimicry** — a causal claim carrying language its design does not
  license, or a causal-method label with its untestable assumption never stated
  or probed — caps *Causal-identification correctness* at Beginning.
- A **fabricated or unretrievable source** caps *Evidence integrity &
  provenance* at Beginning.
- An **untraceable number** — a figure with no path back to your data — caps
  *Verification of AI-assisted parts* at Beginning.
- A **non-reproducing result** — a headline number that does not rerun from the
  work behind it — caps *Verification of AI-assisted parts* at Beginning.
- A **missing AI Research Ledger entry** scores *Craft, ledger & communication*
  **0** and the submission is **returned** unread until it is supplied.

**Revision:** eligible under the standing policy — a revised submission within 7
days of feedback recovers up to half the lost points.

## Penalties

- Late: −10 points per day, up to 3 days; not accepted after (documented
  emergencies: talk to me first, per the syllabus).
- Any dataset, study, or number you cite that turns out not to exist, not to say
  what you claim, or not to rerun: the relevant integrity or verification
  criterion scores Beginning regardless of the rest — the course's evidence-
  integrity rule with teeth.
- A causal claim whose one untestable assumption is never stated or probed
  (design mimicry): *Causal-identification correctness* scores Beginning.
- Missing AI Research Ledger entry: *Craft* scores 0 and the submission is
  returned for completion before grading.

## Common Pitfalls

1. **Design mimicry — the label without the argument.** Writing "natural
   experiment," "difference-in-differences," or "regression discontinuity" over a
   comparison whose one untestable assumption you never stated. The vocabulary is
   not the argument. A skeptic reads past the label straight to the assumption,
   and so should you: name parallel trends, the clean cutoff, or exclusion, and
   say how it could fail.
2. **"We controlled for everything."** Treating adjustment for the confounders you
   happen to *observe* as if it identified the effect, when an unobserved
   confounder still opens the back door. Adjustment works only for the confounder
   you can see. Name the one variable whose absence would break your
   identification, and say how you would know you were missing it.
3. **The AI-written identification argument.** Asking Gemini to judge whether your
   design earns *because*, or pasting a fluent caveat you did not reason to.
   Judging identification is the whole skill this milestone teaches, and it is
   exactly what an AI fakes best. Draft the argument or the boundary yourself,
   then use the Skeptic to attack it, and log both.

---

*Previous: [M04 — Observational Descriptive Design Audit](milestone_04_observational_descriptive_audit.md) ·
Next: [M06 — Experimental Measurement or Data-Acquisition Protocol + URC Abstract internal gate](milestone_06_experimental_measurement_protocol.md) —
your defended causal line meets the design that would let you assign the
treatment yourself, or the protocol that would bring your observational data
into being.*
