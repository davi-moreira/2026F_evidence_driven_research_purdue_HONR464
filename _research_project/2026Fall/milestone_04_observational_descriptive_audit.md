# Milestone 04 — Observational Descriptive Design Audit

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

Due: **Friday, September 25, 11:59 PM** (you present a 3-minute walkthrough at
the Friday studio that day).

| # | File | Description |
|---|---|---|
| 1 | **`lastname_m04_descriptive_audit.pdf`** *or* a shared Colab notebook link | The five-part audit below: your population/frame/sample stack, your selection DAG (image), your concept→construct→indicator measurement plan with its coverage risk, your one-sentence generalization boundary with the crossing it forbids, and your AI Research Ledger rows. This is the graded artifact. |

If you submit a notebook link, make sure sharing is set so the instructor can
open it, and that the selection-DAG figure renders when the notebook is run.

---

## Purpose

Every project in this course has a **descriptive layer**, no matter where it
ends up on the compass. Before you can claim your data predict, generalize, or
identify a cause, you have to be honest about the simpler question underneath:
**who is actually in your data, what did you measure about them, and how far can
a plain description of them travel?** This milestone audits exactly that layer.

You treat your own project, right now, as an **observational descriptive
design** — a study that *observes* units as they are (no intervention) and
*describes* what it finds. A **design audit** is a structured self-inspection:
you lay the design's parts on the table and mark where each one is sound and
where it leaks. The skill you are practicing is the course's signature move,
applied to yourself: draw the boundary of what your description can support, and
refuse to step over it.

This is not a detour from a predictive or causal project. It is the floor every
later claim stands on. If you cannot say who your data speak for, no amount of
modeling later will rescue the claim. At the Friday studio you walk the class
through the audit in three minutes; a partner and an assigned AI reviewer attack
your generalization sentence and your DAG's arrows, and you revise from what
survives.

> **A question that often comes up here:** *"My project is going to be causal
> (or predictive). Why am I doing a descriptive audit?"* Because the descriptive
> layer is where your units, your measure, and your reach are decided, and those
> decisions constrain every later claim. A causal estimate on a biased sample is
> a biased causal estimate. A prediction from a frame that misses half your
> target population predicts for the half you kept. Auditing description first is
> how you find the leak before it contaminates the fancy claim on top of it.

## Components

### 1. Population / frame / sample stack

Name the four layers, in order, and say exactly how each one narrows the one
above it.

- **Target population** — the full set of units your question is ultimately
  about (for example, *all first-year Purdue undergraduates in Fall 2026*).
- **Accessible population** — the part of the target you could realistically
  reach given time, access, and permissions (for example, *first-years in the
  three residence halls you can survey*).
- **Sampling frame** — the concrete list or mechanism your units actually come
  from (for example, *the hall listserv you were given access to*). The frame is
  a real object, not an aspiration.
- **Sample** — the units that ended up in your data after the frame, plus who
  responded.

Then name the **silent exclusion**: the units your frame drops without
announcing it. A listserv misses everyone who opted out of email. A subreddit
scrape misses lurkers who never post. Write one sentence naming who your frame
silently drops and why it matters for your question.

> **A question that often comes up here:** *"Aren't the population and the frame
> basically the same?"* Almost never, and the gap between them is the whole
> point. The **population** is who you *mean*; the **frame** is who you can
> actually *list and reach*. Every gap between the two is a group your answer
> quietly stops covering. Naming the gap out loud is what separates an honest
> description from an accidental overclaim.

### 2. A selection DAG

Draw the process by which a unit ends up in your data. A **DAG** (directed
acyclic graph) is a diagram of arrows, where each arrow means *this influences
that*. A **selection DAG** shows what drives a unit into your sample, so you can
see which forces bend your description away from the population.

Your DAG must show, at minimum: the path from target population to accessible
population to frame to responded-and-recorded, and at least one **selection
influence** — a trait that affects *both* whether a unit shows up in your data
*and* the thing you are measuring. That double arrow is where description gets
dangerous, because it means the units you kept differ systematically from the
ones you lost on the very variable you care about.

Submit the DAG as an **image** (a clear hand drawing photographed, or the
notebook-generated figure from the studio notebook, edited to your project). A
DAG that only draws the tidy funnel and hides the selection influence has
skipped the reason the tool exists.

### 3. Measurement plan for your key construct

Climb the **concept → construct → indicator** ladder for the one construct at
the center of your description.

- **Concept** — the abstract idea (for example, *sense of belonging*).
- **Construct** — the specific, targetable version of it (for example,
  *belonging to one's residence-hall floor community*).
- **Indicator** — the concrete thing you can actually record (for example, *a
  1–5 self-report item on the hall survey*).

Each rung must visibly narrow the one above it. Then name the dominant **data
risk** to that indicator, using the right word for it:

- **Coverage** — units the frame never reaches at all.
- **Nonresponse** — units in the frame who were asked but did not answer.
- **Missingness** — values that are blank for units you did keep.

State which of the three most threatens your measure, and whether it is likely
to be random or to run in a direction (systematic). One paragraph.

### 4. The generalization boundary

This is the heart of the audit. Write **two sentences**.

- **The population sentence your frame licenses**: the strongest description
  your design actually supports, naming the population the frame reaches and the
  uncertainty around it. Begin it with *"In the units my frame reaches, …"* or
  *"For [the specific population], with the uncertainty that …"*.
- **The crossing your design does NOT license**: the tempting sentence a careless
  reader might walk away with, which your design cannot support. Name the
  **silent upgrade** you are forbidding. A silent upgrade is when a sentence
  about your frame is quietly rewritten as a sentence about the whole target
  population, or about cause, without any new license being bought.

> **A question that often comes up here:** *"How is a silent upgrade different
> from just stating my finding?"* A finding stays inside the license your design
> bought. A silent upgrade swaps the subject of the sentence while keeping the
> same confident tone. "Students in my three halls report high belonging"
> becomes "Purdue first-years feel they belong" with no new sampling license,
> and now the sentence covers people your frame never touched. The upgrade is
> silent because nothing in the wording flags that the reach just grew. Your job
> is to catch it in your own draft and forbid it in writing.

### 5. AI Research Ledger rows

Every use of AI in building this audit gets a row in your **AI Research Ledger**
(the eight-field table: task delegated · tool used · prompt · output summary ·
decision · verification method · remaining concern · responsible researcher).
Locating a frame, drafting an exclusion list, generating the DAG scaffold, and
critiquing your boundary sentence are all delegable tasks, and each one that you
delegated needs a row that names how you verified the result. "No AI used" is a
legitimate entry if it is true.

**A missing ledger is not a minor lapse.** Per the course rule, a missing AI
Research Ledger entry scores the Craft criterion **0** and the submission is
**returned** for completion before it is graded.

### 6. Dossier update line

End with one line recording what this milestone finalizes in your **Research
Project Dossier**: your data + measurement documentation now carries a declared
frame, a selection DAG, a measurement ladder, and a stated generalization
boundary. Name the file or section in your dossier where each now lives.

---

## Submission Expectations

| Item | Specification |
|---|---|
| **Length** | The five-part audit + ledger rows (typically 2–4 pages PDF, or the equivalent notebook sections) |
| **Figure** | The selection DAG as a legible image; funnel plus at least one selection-influence arrow |
| **Presentation** | 3-minute walkthrough at the Friday studio (Sep 25); a partner and an assigned AI reviewer red-team your boundary and DAG — part of the grade |
| **Style** | Plain language; every technical term used as defined above; the generalization boundary stated as two explicit sentences |
| **Filename** | `lastname_m04_descriptive_audit.pdf` (or a shared Colab link) |
| **Location** | Brightspace → Assignments → M04 |

---

## Grading Rubric (100 points)

Four bands on the course's five shared virtues (`planning/ASSESSMENT_ARCHITECTURE.md`).

| Criterion | Exemplary | Proficient | Developing | Beginning |
|---|---|---|---|---|
| **Design-audit correctness** (30) | Population/frame/sample stack correct and its silent exclusion named; DAG shows a real selection influence, not just the funnel; measurement ladder narrows at every rung (26–30) | Stack and DAG correct; one rung or one arrow thin or under-argued (21–25) | Stack or DAG present but a layer collapsed, or the selection influence missing (13–20) | Frame described as if it were the population; DAG decorative or absent (0–12) |
| **Evidence integrity & provenance** (20) | Every named frame, indicator, and source is real and retrievable; the reader can trace each to its origin (18–20) | Real and traceable; one provenance link thin (14–17) | A claimed frame or indicator asserted without a locatable source (8–13) | A cited source or survey item that does not exist or does not say what you claim (0–7) |
| **Verification of AI-assisted parts** (20) | Every AI-assisted step (frame list, DAG scaffold, boundary critique) has a ledger row with a named, non-vague verification method (18–20) | Ledger present; one verification method vague or one step unlogged (14–17) | Ledger thin; AI outputs used but verification not named (8–13) | AI output reproduced without any verification, or the boundary caveat written by AI and unchecked (0–7) |
| **Uncertainty & generalization boundary** (20) | Both boundary sentences present; the licensed population sentence carries its uncertainty; the forbidden silent upgrade is named precisely (18–20) | Both sentences present; uncertainty or the forbidden crossing stated loosely (14–17) | Only one sentence, or the boundary asserted without the crossing it forbids (8–13) | No boundary, or a description silently upgraded to the whole population or to cause (0–7) |
| **Craft, ledger & communication** (10) | On-format, on-time, clear 3-minute walkthrough, complete AI Research Ledger, dossier line present (9–10) | Minor format lapses; ledger complete (7–8) | Missing pieces or a rushed walkthrough (4–6) | Missing AI Research Ledger (Craft scored 0, submission returned) (0–3) |

**Hard caps (a single failure caps the row regardless of the rest):**

- A **fabricated or unretrievable source** caps *Evidence integrity & provenance*
  at Beginning.
- An **untraceable number** — a figure with no path back to your data — caps
  *Verification of AI-assisted parts* at Beginning.
- A **missing AI Research Ledger entry** scores *Craft, ledger & communication*
  **0** and the submission is **returned** unread until it is supplied.

**Revision:** eligible under the standing policy — a revised submission within 7
days of feedback recovers up to half the lost points.

## Penalties

- Late: −10 points per day, up to 3 days; not accepted after (documented
  emergencies: talk to me first, per the syllabus).
- Any frame, indicator, or source you cite that turns out not to exist or not to
  say what you claim: *Evidence integrity & provenance* scores Beginning
  regardless of the rest — the course's evidence-integrity rule with teeth.
- Missing AI Research Ledger entry: *Craft* scores 0 and the submission is
  returned for completion before grading.

## Common Pitfalls

1. **The frame described as the population.** Writing "my sample represents
   first-year students" when your frame is three residence halls on one campus.
   The frame is who you could reach; say who that leaves out before a reviewer
   says it for you.
2. **The DAG that decorates instead of shows selection.** A neat funnel from
   population to sample with every arrow pointing the same way looks tidy and
   teaches nothing. The DAG earns its place only when it draws the selection
   influence — the trait that bends both who shows up and what you measure.
3. **The caveat written by AI and left unverified.** Asking a tool to "write my
   limitations paragraph" and pasting it in. A boundary you did not reason to is
   a boundary you cannot defend at the studio, and an unverified AI caveat with
   no ledger row caps your verification score. Draft the boundary yourself, then
   use AI to attack it.

---

*Previous: [M03 — Research Charter & MIDA Declaration](milestone_03_research_charter_mida.md) ·
Next: [M05 — Causal Identification Strategy or Causal-Language Boundary](milestone_05_causal_identification.md) —
your defended description becomes the baseline a causal question either earns the
right to cross, or is explicitly forbidden from crossing.*
