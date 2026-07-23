# Milestone 03 — Research Charter & MIDA Declaration

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

Due: **Friday, September 18, 11:59 PM** (you deliver a 3-minute charter
declaration at the Friday studio that day).

| # | File | Description |
|---|---|---|
| 1 | **`lastname_m03_charter.pdf`** *or* a shared Colab notebook link | Your research charter: the four **MIDA** parts of your design (Model, Inquiry, Data strategy, Answer strategy), a 3-node **DAG** image, your **diagnosis** naming the biggest threat as bias, variance, or power plus the one **redesign** it demands, your **compass position and claim boundary**, and your AI Research Ledger rows. This is the graded artifact. |

If you submit a notebook link, make sure sharing is set so the instructor can
open it, and that the DAG figure renders when the notebook is run.

---

## Purpose

This is the milestone where your question stops floating and gets a **design** to
live in. In nb03 you learned that every study, from a two-person survey to a
national experiment, has the same four parts — **MIDA**: a **Model** (the world
your question assumes), an **Inquiry** (the exact quantity you want), a **Data
strategy** (how the data come to exist), and an **Answer strategy** (how you turn
data into an estimate). You also learned the discipline that separates a real
design from a hope: the four parts must **align** — all point at the same
quantity — and the design must be **diagnosed** before you spend a semester
running it, so you know in numbers what its answer can and cannot support.

A **research charter** is that design, declared out loud and on paper, before any
data arrive. Declaring the inquiry first is what protects you from *inquiry
shopping* — quietly sliding toward whichever number looks best once you have seen
results. Declaring and diagnosing the whole design first is what lets you show up
in December standing behind a claim instead of defending a guess.

This charter is not a detour for a project that will end up predictive or
generalizing. MIDA is the shared machinery every later compass position reuses.
The model, inquiry, data strategy, and answer strategy you declare here become
the spine your descriptive audit (M4), your causal boundary (M5), and every
protocol after it hang from. Get the four parts aligned and honestly diagnosed
now, and the rest of the semester builds on solid ground.

> **A question that often comes up here:** *"If Gemini can draft a whole design
> in seconds, why build it part by part myself?"* Because a design is a chain of
> commitments, and the tool cannot make them for you. It does not know which
> world your question assumes or which single number would actually answer it. If
> you let it guess, you inherit its guess and defend a design you never reasoned
> through. Building each part yourself is what lets you stand behind the whole at
> the studio and at the defense.

## Components

### 1. The Model (M) — your world, in prose and one DAG

State, in a short paragraph, **what the world would have to be like for your
question to have an answer.** Name the **units** (who or what your question is
about), the thing that can **vary** across them, the **outcome** you care about,
and the other forces that could plausibly move that outcome. This is a
commitment to how the world *could* be, not yet a claim about which picture is
true.

Then draw that world as a **DAG** — a directed acyclic graph, a diagram where a
**node** is a variable and an **arrow** claims that one variable could directly
influence another. Your DAG must have **three nodes**: your treatment (or the
thing that varies), your outcome, and **at least one third variable** — a
**confounder**, a common cause with an arrow into *both* the treatment and the
outcome. For each arrow, be ready to name the real-world mechanism it asserts.

Submit the DAG as an **image** (a clear hand drawing photographed, or the
figure from the studio notebook edited to your project).

> **A question that often comes up here:** *"My question is descriptive — there
> is nothing to intervene on. Do I still draw a DAG?"* Yes, and the third node
> still earns its place. For a descriptive question your DAG shows what drives a
> unit into your data and what moves the thing you measure; the confounder
> becomes the trait that bends both. A model with only your treatment and your
> outcome silently assumes nothing else moves the outcome — which is exactly the
> assumption most descriptions get wrong.

### 2. The Inquiry (I) — one estimand that passes the genie test

State the exact quantity you want, two ways: **in one plain sentence a
non-researcher could repeat back**, and **as an estimand** — the target number a
genie who could see your whole model would hand you with no missing data. Apply
the **genie test**: if even an all-knowing genie would ask *"which number do you
mean?"*, your inquiry is still vague. "Does mentoring help?" fails. "The average
of Y1 minus Y0 across all first-years" passes.

Then classify it and name its **units**:

- **Descriptive inquiry** — a summary of the world as it is (a share, an average,
  a difference over a population you could in principle observe).
- **Causal inquiry** — a comparison of two potential-outcome worlds for the same
  units (any estimand with both Y1 and Y0 in it, because it reaches for the
  counterfactual you never see).

Declare the estimand **now, before any data.** The number you name today is the
answer key you are held to in December.

### 3. The Data strategy (D) — how your data come to exist

One paragraph: **who is sampled, and who gets which condition.** Name the units
you can actually reach and the mechanism that decides their condition — a coin
flip, a lottery, self-selection, or plain observation of the world as it is. This
is where a causal inquiry either earns a clean comparison (assignment you
control) or inherits a confound (units select into treatment on their own).

### 4. The Answer strategy (A) — data turned into an estimate

One or two sentences: **how you turn the collected data into an estimate of your
inquiry.** A difference in means, a share, a comparison across groups. The test
your charter must pass is **alignment**: your answer strategy has to target the
inquiry your model made askable, over the same units, not an easier quantity
that happens to be nearby.

### 5. The diagnosis and one redesign

A design earns a claim only when it is **diagnosed**, not merely argued for. In
nb03 you declared a design and ran it many times to read three numbers:

- **Bias** — the average distance between your estimate and the truth. A tilt
  that **more data cannot fix**; only a design change moves it.
- **Variance** — how much the estimate wobbles run to run. **More data shrinks
  it.**
- **Power** — how often the design would actually detect a real effect.

Write, for **your** design: which of the three is your **biggest threat**, what
your best diagnosis (even a rough one, or a reasoned argument if you cannot yet
simulate) says it does to your answer, and the **single redesign** that most
improves it. The redesign must *read the diagnosis* — more units for a variance
or power problem, a changed comparison or assignment for a bias problem. "Collect
more data" for a confounded design is the classic wrong fix.

### 6. Compass position and claim boundary

Name your project's **compass position** — Description, Generalization,
Prediction, or **Causal reasoning** — and write **two sentences** that draw its
boundary:

- **What your design can establish**: the strongest claim your declared,
  diagnosed design actually supports, stated with its uncertainty.
- **What it cannot**: the tempting sentence your design does **not** license.
  Name whether your design **identifies** an effect (a cause you can defend) or
  only shows an **association** (a pattern), and forbid the **silent scope
  change** from *associated with* to *causes* (the wording that quietly claims
  cause your design never earned).

Rigor is a diagnosed property, not a vibe. A design whose four parts quietly
point at different quantities, or one you never diagnosed, makes no promises no
matter how rigorous it sounds. This is that promise, written down and bounded.

### 7. AI Research Ledger rows

Every use of AI in building this charter gets a row in your **AI Research
Ledger** (the eight-field table: task delegated · tool used · prompt · output
summary · decision · verification method · remaining concern · responsible
researcher). Brainstorming a lurking variable, phrasing an estimand, listing
threats to a design, and critiquing your boundary sentence are all delegable
tasks, and each one you delegated needs a row that names how you verified the
result. "No AI used" is a legitimate entry if it is true.

**A missing ledger is not a minor lapse.** Per the course rule, a missing AI
Research Ledger entry scores the Craft criterion **0** and the submission is
**returned** for completion before it is graded.

### 8. Dossier update line

End with one line recording what this milestone finalizes in your **Research
Project Dossier**: your MIDA declaration now carries a model with a DAG, a
declared estimand, a data and answer strategy, a diagnosis with one named
redesign, and a stated compass position and claim boundary. Name the file or
section in your dossier where each now lives.

---

## Submission Expectations

| Item | Specification |
|---|---|
| **Length** | The charter's six declared parts + ledger rows (typically 2–4 pages PDF, or the equivalent notebook sections) |
| **Figure** | The 3-node DAG as a legible image; treatment, outcome, and at least one confounder with an arrow into both |
| **Presentation** | 3-minute charter declaration at the Friday studio (Sep 18); a partner and the assigned MIDA Design Reviewer red-team your alignment, your DAG's arrows, and your claim boundary — part of the grade |
| **Style** | Plain language; every technical term used as defined in nb03; the inquiry stated both in words and as an estimand; the claim boundary stated as two explicit sentences |
| **Filename** | `lastname_m03_charter.pdf` (or a shared Colab link) |
| **Location** | Brightspace → Assignments → M03 |

---

## Grading Rubric (100 points)

Four bands on the course's five shared virtues (`planning/ASSESSMENT_ARCHITECTURE.md`).

| Criterion | Exemplary | Proficient | Developing | Beginning |
|---|---|---|---|---|
| **MIDA alignment & compass fit** (30) | All four MIDA parts present and **aligned** — data and answer strategies reach the declared inquiry; the DAG shows a real confounder into both treatment and outcome, not a one-arrow model; the compass position fits the inquiry's own words (26–30) | Four parts and DAG present and mostly aligned; one part or one arrow thin or under-argued (21–25) | A MIDA part collapsed or the confounder missing, or the answer strategy targets an easier quantity than the inquiry (13–20) | One-arrow "model," or the four parts point at different quantities, or the compass position contradicts the question (0–12) |
| **Evidence integrity & provenance** (15) | Every source, number, or prior finding cited to justify the design is real and retrievable; the reader can trace each to its origin (13–15) | Real and traceable; one provenance link thin (11–12) | A claimed source or figure asserted without a locatable origin (6–10) | A cited source or number that does not exist or does not say what you claim (0–5) |
| **Verification of the diagnosis & AI-assisted parts** (20) | The diagnosis reruns and its numbers trace to the declared design; every AI-assisted step (variable brainstorm, estimand phrasing, threat list, boundary critique) has a ledger row with a named, non-vague verification method (18–20) | Diagnosis traceable and ledger present; one verification method vague or one step unlogged (14–17) | Diagnosis asserted but not traceable to the design, or AI outputs used with verification unnamed (8–13) | A diagnosis number with no path back to the design, or AI output reproduced with no verification (0–7) |
| **Uncertainty, limitations & claim boundary** (20) | The diagnosis names the biggest threat (bias, variance, or power) honestly and says what it does to the answer; both boundary sentences present; the identified-vs-associated line is drawn and the silent scope change from association to cause forbidden (18–20) | Threat named and both boundary sentences present; uncertainty or the forbidden crossing stated loosely (14–17) | Only one boundary sentence, or the threat named without saying what it does, or no redesign that reads the diagnosis (8–13) | No diagnosis, no boundary, or a design whose language slides from association to cause (0–7) |
| **Craft, ledger & communication** (15) | On-format, on-time, clear 3-minute declaration, complete AI Research Ledger, dossier line present (13–15) | Minor format lapses; ledger complete (10–12) | Missing pieces or a rushed declaration (5–9) | Missing AI Research Ledger (Craft scored 0, submission returned) (0–4) |

**Hard caps (a single failure caps the row regardless of the rest):**

- A **fabricated or unretrievable source** caps *Evidence integrity &
  provenance* at Beginning.
- An **untraceable number** — a diagnosis figure with no path back to your
  declared design or simulation — caps *Verification* at Beginning.
- A **non-reproducing result** — a diagnosis whose numbers do not rerun from the
  design you declared — caps *Verification* at Beginning.
- A **missing AI Research Ledger entry** scores *Craft, ledger & communication*
  **0** and the submission is **returned** unread until it is supplied.

**Revision:** eligible under the standing policy — a revised submission within 7
days of feedback recovers up to half the lost points.

## Penalties

- Late: −10 points per day, up to 3 days; not accepted after (documented
  emergencies: talk to me first, per the syllabus).
- Any source or number you cite to justify the design that turns out not to exist
  or not to say what you claim: *Evidence integrity & provenance* scores
  Beginning regardless of the rest — the course's evidence-integrity rule with
  teeth.
- Missing AI Research Ledger entry: *Craft* scores 0 and the submission is
  returned for completion before grading.

## Common Pitfalls

1. **The one-arrow DAG, and MIDA parts that point different directions.** Drawing
   *treatment → outcome* with nothing else is your conclusion wearing a model's
   clothes; it silently assumes nothing else moves your outcome. The node you are
   tempted to omit — the confounder — is usually the one that matters most. The
   same failure at the design level is four MIDA parts that quietly serve
   different quantities: a population inquiry chased by a convenience sample, a
   causal inquiry with a data strategy that never varies the cause. Align them or
   the design promises nothing.
2. **The undiagnosed design.** A charter that declares all four parts and then
   asserts the design "is rigorous" has skipped the only thing that earns the
   word. Rigor is a diagnosed property. Name the biggest threat as bias,
   variance, or power, say what it does to your answer, and bring the one
   redesign it demands — or your declaration makes no promises.
3. **Fixing the wrong number, or upgrading the claim.** Reaching for "more data"
   to rescue a design whose real problem is a confound spends your budget on
   variance while the bias sits untouched, giving you a very precise estimate of
   the wrong quantity. Its twin is a **silent scope change**: writing "mentoring
   *raises* belonging" when your design only shows the two are associated. Match
   the fix to the diagnosis, and keep your language on the side of the line your
   design actually reaches.

---

*Previous: [M02 — Verified Evidence & Contribution Map](milestone_02_verified_evidence_map.md) ·
Next: [M04 — Observational Descriptive Design Audit](milestone_04_observational_descriptive_audit.md) —
your declared, diagnosed design gets its descriptive layer audited: who is
actually in your data, what you measured, and how far a plain description of them
can honestly travel.*
