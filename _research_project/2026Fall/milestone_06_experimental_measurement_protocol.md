# Milestone 06 — Experimental Measurement or Data-Acquisition Protocol (+ URC Abstract Internal Gate)

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

Due: **Friday, October 9, 11:59 PM**. That Friday is a **protocol clinic and
abstract workshop**: you bring a near-final draft, walk a partner and an AI
reviewer (Gemini, or optionally the **Experimental Design Reviewer** role in
GenAI Studio) through your
measurement protocol, and clear the internal gate on your URC abstract before it
can go out. The red-team notes from that studio feed the grade; you polish from
them and submit by the same-day deadline.

| # | File | Description |
|---|---|---|
| 1 | **`lastname_m06_measurement_protocol.pdf`** *or* a shared Colab notebook link | The six-part deliverable below: your construct and measurement design, the descriptive quantity it reports, your measurement DAG (image), your artifact plan, your two-sentence claim boundary, your URC abstract, and your AI Research Ledger rows. This is the graded artifact. |

If you submit a notebook link, set sharing so the instructor can open it, and
confirm the measurement-DAG figure renders when the notebook is run.

---

## Purpose

Every project needs a way to **get the number it is built to report**. M4 asked
who is in your data; M5 asked whether your design earns the word *because*. M6
asks the question underneath both: **how will you actually measure the thing at
the center of your project, and how far can that measurement travel?**

This week you learned the surprise that anchors the milestone: an experiment can
be a **measurement instrument**, not a causal test. An **experiment as a
measurement system** uses randomly assigned, controlled stimuli to reveal a
**latent characteristic** — a real property you cannot read off directly, like
how much discrimination a job market holds or how sensitive an attitude is to how
it is framed. The audit experiment, the list experiment, the conjoint, the
behavioral game, the calibration protocol, the A/B instrument test: each points a
randomized stimulus at a standing feature of the world and reports a **descriptive
quantity**. Random assignment is a measuring trick there, not a causal claim.

So the deliverable has two honest jobs. First, write the **protocol**: the design
that will produce your project's key number, with the artifacts that could fake
that number named and guarded against. Not every project runs an experiment; if
yours acquires data by another route (a scrape, an archive, a survey, an
instrument reading), you write the **data-acquisition protocol** for that route,
and you still name the threats to **construct validity** the same way. Second,
clear the **URC abstract internal gate**: the short public description of your
project, worded so it does not promise more than your protocol can deliver. A
number with no named procedure behind it, or an abstract that overclaims, is not
a protocol.

> **A question that often comes up here:** *"My project doesn't run an
> experiment. Does this milestone still apply?"* Yes, and the shape is the same.
> Whether you assign a stimulus or pull rows from an archive, you are building an
> instrument that reads a construct, and every instrument can be fooled. The
> experimental-measurement path and the data-acquisition path both end at the
> same two things: the descriptive quantity your design reports, and the boundary
> around it. Pick the path your question needs and write that one.

## Components

### 1. The construct and the measurement design

Name the **latent characteristic** at the center of your project: the one real
property you cannot read off directly and must reveal through a design (a level of
some attitude, a prevalence, a preference weight, a detection threshold).
Then declare how you will measure it, and why that route fits.

- If an experiment serves it best, name which one and why: an **audit
  experiment**, a **list experiment**, a **conjoint experiment**, a **behavioral
  game**, a **calibration protocol**, or an **A/B instrument test**. Say what the
  **controlled stimulus** is (the thing you set on purpose and assign by chance)
  and how assignment happens.
- If a direct measure or another data-acquisition route serves it better, name the
  source, the instrument, and how a unit's value gets recorded.

One short paragraph. The test is that a reader could see, from your words, exactly
how a single unit's measurement comes to exist.

### 2. The descriptive quantity it reports (the estimand)

State the exact number your design is built to report, and the units it is in. In
this course that number is the **estimand**: the quantity the design exists to
measure. Keep it **descriptive** — a level, a prevalence, a weight, or a
threshold **for the units you observe** — not the effect of an intervention you
would deploy.

Name it in one sentence, with its units. For example: *"the share of respondents
who hold [sensitive attitude], on a 0-to-1 scale, for the units in my sample,"*
or *"the average detection threshold, in decibels, for the listeners I test."*
If a random assignment sits in your design, say in one line why it serves this
**descriptive** measurement and does not turn the inquiry causal.

> **A question that often comes up here:** *"I randomize a stimulus — doesn't that
> make my question causal?"* Not by itself. The word that fixes the kind is your
> **question**, not your **procedure**. When the target is a property of the world
> as it stands, the inquiry is descriptive even though you shuffled. Naming the
> descriptive quantity out loud is how you keep the coin flip from smuggling in a
> causal claim you cannot defend.

### 3. The measurement DAG and the artifact plan

Draw the machinery as a **DAG** (a directed acyclic graph: a picture of arrows
where each arrow means *this influences that*). Your measurement DAG must show, at
minimum: the **randomized stimulus** (or your data source) feeding the measured
response, the **latent characteristic** feeding it too (the thing you actually
want), and at least one **artifact arrow**, drawn dashed, feeding the response
without any truth value.

Then write the **artifact plan**. Name the two threats to **construct validity**
your design most fears, using the right words:

- **Demand effect** — respondents shift their answer toward what they think you
  want, so the reading moves for a reason that is not the construct.
- **Instrument effect** — the tool or wording itself pushes the reading, so the
  procedure, not the construct, produces part of the number.

For each, name the one **redesign** move that defuses it (blinding the
administrator, neutral wording, an unobtrusive measure, a counterbalanced order,
a calibration check), and tie each redesign to a dashed arrow in your DAG. For a
data-acquisition project, name the acquisition threats to construct validity in
the same shape (a source that self-selects, a field that means something other
than your construct) and the move that guards each. Submit the DAG as an
**image**.

### 4. The claim boundary (two sentences)

This is the heart of the protocol. Write **two sentences**.

- **The descriptive claim your design licenses**, worded for the units observed
  and carrying its **uncertainty**. Begin it with *"For the units I measure,
  [descriptive quantity] is around ___, with the uncertainty that ___."* The
  uncertainty names your interval, your standard error, or the artifact you could
  not fully rule out.
- **The sentence your design does NOT license**: the tempting **causal** or
  **population** claim a careless reader might walk away with. Name it and forbid
  it. "We randomized, therefore we have a causal effect," or a measurement number
  reported as if it covered a population your design never reached, is exactly the
  overreach this week exists to catch.

### 5. The URC abstract (internal gate)

Write the abstract you would submit to the **Undergraduate Research Conference**,
roughly 150–250 words, describing your project as it now stands: the question, the
construct, the descriptive quantity your protocol will measure, and the boundary
around it. This is an **internal gate**: it must clear the instructor's check at
the studio before it goes out externally. The gate has one non-negotiable rule —
**the abstract must stay inside the boundary you wrote in Component 4.** An
abstract that promises a causal finding, or a population claim your design cannot
buy, does not clear the gate.

### 6. AI Research Ledger rows and dossier update line

Every use of AI in building this protocol gets a row in your **AI Research
Ledger** (the eight-field table: task delegated · tool used · prompt · output
summary · decision · verification method · remaining concern · responsible
researcher). Scouting real measurement studies in your field, extending the DAG
code, and red-teaming your boundary or your abstract are all delegable tasks, and
each one you delegated needs a row naming how you verified the result. "No AI
used" is a legitimate entry if it is true.

**A missing ledger is not a minor lapse.** Per the course rule, a missing AI
Research Ledger entry scores the Craft criterion **0** and the submission is
**returned** for completion before it is graded.

End with one line recording what this milestone finalizes in your **Research
Project Dossier**: your data and measurement documentation now carries a declared
measurement design, a measurement DAG, an artifact plan, a stated claim boundary,
and a gated URC abstract. Name the file or section where each now lives.

---

## Submission Expectations

| Item | Specification |
|---|---|
| **Length** | The six-part protocol + abstract + ledger rows (typically 2–4 pages PDF, or the equivalent notebook sections) |
| **Figure** | The measurement DAG as a legible image: stimulus (or source) and latent characteristic into the response, plus at least one dashed artifact arrow |
| **Clinic** | Protocol clinic and abstract workshop at the Friday studio (Oct 9); a partner and an AI reviewer (Gemini or the Experimental Design Reviewer role) red-team your boundary and artifact plan — part of the grade |
| **Style** | Plain language; every technical term used as defined this week; the claim boundary stated as two explicit sentences; the abstract inside that boundary |
| **Filename** | `lastname_m06_measurement_protocol.pdf` (or a shared Colab link) |
| **Location** | Brightspace → Assignments → M06 |

---

## Grading Rubric (100 points)

Four bands on the course's five shared virtues (`planning/ASSESSMENT_ARCHITECTURE.md`).

| Criterion | Exemplary | Proficient | Developing | Beginning |
|---|---|---|---|---|
| **Compass & pathway alignment** (30) | The design is declared as experimental-descriptive or data-acquisition; the descriptive quantity is named with units; any random assignment is shown to serve measurement, not a causal claim; the boundary matches (26–30) | Design and quantity correct; one link between assignment and descriptive inquiry stated loosely (21–25) | Design or quantity present but the descriptive-vs-causal line blurred, or the quantity vague (13–20) | Random assignment read as a causal effect, or no named descriptive quantity (0–12) |
| **Evidence integrity & provenance** (20) | Every construct, instrument, and cited measurement study is real and retrievable; the descriptive quantity traces to the design that produces it (18–20) | Real and traceable; one provenance link thin (14–17) | A claimed instrument or study asserted without a locatable source (8–13) | A cited source or measurement study that does not exist or does not say what you claim (0–7) |
| **Verification of AI-assisted parts** (20) | Every AI-assisted step (study scout, DAG scaffold, boundary or abstract critique) has a ledger row with a named, non-vague verification method; the AI reviewer's critique is resolved in writing (18–20) | Ledger present; one verification method vague or one step unlogged (14–17) | Ledger thin; AI outputs used but verification not named (8–13) | AI output reproduced without any verification, or the boundary or abstract written by AI and unchecked (0–7) |
| **Uncertainty & artifact boundary** (20) | Both boundary sentences present; the licensed sentence carries its uncertainty; the artifact plan names a real demand effect and instrument effect, each with a redesign tied to a dashed DAG arrow; the forbidden causal or population sentence is named precisely (18–20) | Both sentences present; uncertainty or one artifact stated loosely (14–17) | Only one sentence, or an artifact named with no redesign, or the boundary without the crossing it forbids (8–13) | No boundary, or a measurement upgraded to a causal or population claim the design cannot buy (0–7) |
| **Craft, ledger & abstract gate** (10) | On-format, on-time, clear clinic walkthrough, URC abstract inside the boundary, complete AI Research Ledger, dossier line present (9–10) | Minor format lapses; abstract and ledger complete (7–8) | Missing pieces, a rushed walkthrough, or an abstract that drifts past the boundary (4–6) | Missing AI Research Ledger (Craft scored 0, submission returned) (0–3) |

**Hard caps (a single failure caps the row regardless of the rest):**

- A **fabricated or unretrievable source** — a cited measurement study or
  instrument that does not exist or does not say what you claim — caps *Evidence
  integrity & provenance* at Beginning.
- An **untraceable number** — a descriptive quantity or interval with no path back
  to the design or data that produced it — caps *Verification of AI-assisted
  parts* at Beginning.
- A **non-reproducing result** — a simulated or computed figure in your protocol
  that does not rerun from the notebook it came from — caps *Verification of
  AI-assisted parts* at Beginning.
- A **missing AI Research Ledger entry** scores *Craft, ledger & abstract gate*
  **0** and the submission is **returned** unread until it is supplied.

**Revision:** eligible under the standing policy — a revised submission within 7
days of feedback recovers up to half the lost points.

## Penalties

- Late: −10 points per day, up to 3 days; not accepted after (documented
  emergencies: talk to me first, per the syllabus).
- Any instrument, measurement study, or source you cite that turns out not to
  exist or not to say what you claim: *Evidence integrity & provenance* scores
  Beginning regardless of the rest — the course's evidence-integrity rule with
  teeth.
- A measurement reported as a causal effect, or as a population claim your design
  never reached: the *Uncertainty & artifact boundary* criterion scores Beginning
  regardless of the rest.
- Missing AI Research Ledger entry: *Craft* scores 0 and the submission is
  returned for completion before grading.

## Common Pitfalls

1. **The randomized-therefore-causal slip.** Writing "I randomized the stimulus,
   so this is a causal effect" when your target is a standing property of the
   world. Random assignment here is a measuring trick. Name the descriptive
   quantity your design reports, and keep the verb inside it.
2. **The DAG that hides the artifact.** Drawing a tidy stimulus-to-response arrow
   and stopping. That funnel teaches nothing. The DAG earns its place only when it
   draws the dashed **demand-effect** and **instrument-effect** arrows and your
   redesign confronts them by name.
3. **The abstract that outruns the protocol.** Writing a URC abstract that
   promises a causal finding or a population claim while your protocol licenses
   only a descriptive quantity for the units you measure. The abstract must sit
   inside the Component 4 boundary; an abstract that overclaims does not clear the
   internal gate.

---

*Previous: [M05 — Causal Identification Strategy or Causal-Language Boundary](milestone_05_causal_identification.md) ·
Next: [M07 — Declared Analysis Protocol](milestone_07_declared_analysis_protocol.md) —
your gated measurement design becomes the exact, named procedure that turns the
data it produces into your project's reported number.*
