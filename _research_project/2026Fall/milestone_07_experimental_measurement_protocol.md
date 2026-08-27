# Course milestone M7 — First Reproducible Analysis (+ URC Abstract Internal Gate)

<!-- book-milestone-bridge:begin -->
> **Book Milestone bridge** — course milestone **M7**.
> This submission presents **Book Milestone 7 — Your first reproducible analysis** (version 1): work from its [milestone page](https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464/book/studios/milestone07-first-analysis.html#milestone).
<!-- book-milestone-bridge:end -->

## About the Research Project

Your semester project is **individual by default**: one researcher, one question,
carried from curiosity to a defended, reproducible claim. With instructor
approval, and only if at least three active projects remain and the required
peer-evaluation assignments are feasible, you may instead complete the same
chain as a group. The same five Final Project components apply
in either mode. Unless this brief marks a requirement as individual, an approved
group submits one shared artifact naming every member, and its shared rubric
rows receive a common score. Each member's AI Research Ledger and any other
requirement marked individual are scored per member, so recorded milestone
scores can differ only on those rows. Every member remains responsible for the
complete work and their own defense. Peer Evaluation remains a true peer
rating: group members rate every teammate; an individual-project researcher
is rated by two instructor-assigned project peers; nobody rates themselves. See
[Final Project — Grading and Project Modes](final_project_grading_and_project_modes.md).
It runs through milestones
**M1–M16**, peaks publicly at the **Purdue Fall Undergraduate Research Expo
poster session (Tuesday, November 17 — required)**, and closes with the
reproducible package and cold run in December. Every milestone
follows the same cadence: **Friday-studio kickoff → develop across the week →
work it at the Friday studio → submit by the deadline on the course platform,
11:59 PM → revise (where eligible)**. Every milestone also updates your
cumulative **Research Project Dossier** and appends at least one row to your
**AI Research Ledger** — the running record of what you handed to AI and how you
checked it. Milestone weights live in
[Final Project — Grading and Project Modes](final_project_grading_and_project_modes.md);
instructions and rubrics live one page per milestone, like this one.

---

## What to Submit on Brightspace

Due: **Tuesday, October 13, 11:59 PM**. That week's Friday is Studio 7's milestone
session, run as a **pipeline clinic and abstract workshop**: you bring your
running notebook, restart it from empty in front of your own eyes, walk the
verification record past your AI assistant's review, and clear the internal gate
on your URC abstract before it can go out. You repair what the clinic exposes
and submit by Tuesday night, after the October Break weekend.

| # | File | Description |
|---|---|---|
| 1 | **A shared Colab notebook link** *or* **`lastname_m07_first_analysis.ipynb`** | The nine-part deliverable below, carried in the notebook itself or in an optional companion **`lastname_m07_first_analysis.pdf`**: the seeded pipeline, your route-specific result with its uncertainty statement, the clean-restart record with your environment record, the claim-to-output trace, two independent re-derivations judged against a tolerance you declared first, the leakage audit with every flag settled, your gated URC abstract, your AI Research Ledger rows, and your dossier line. This is the graded artifact. |
| 2 | **`lastname_m07_conference_application.pdf`** | Proof that you applied to present at the Fall Undergraduate Research Expo: the confirmation page or confirmation email, saved as a PDF. Applying is not optional and it is not something the course does for you. Without this confirmation there is no poster session for you to present at, however good the rest of your project is. |
| 3 | **`lastname_m07_meeting_round01.pdf`** | Confirmation that your **Round 01 mentor meeting** happened, inside the **Mon Oct 5 to Sun Oct 11** window you requested at M4: the date and time, who attended, and the two or three decisions that came out of it, each with what you changed or why you kept your course. |
| 4 | **EDR\|AI "It is your turn" — ch. 22, ch. 23** | **Already submitted, not collected again here.** These sections were due on their own reading dates, as IYT Practice submissions; the dated list is on the course page. Confirm each one is complete and carry the work into this milestone and your Research Project Dossier. See "The Book Anchor" below. |

Set sharing so the instructor can open **and rerun** the notebook. The rerun is
part of the milestone: confirm the result in your write-up matches what the
notebook prints from a fresh runtime, top to bottom, before you submit.

---

## Round 01 of your mentor meetings, confirmed

The meeting you requested at M4 has to have happened by now, inside the
**Mon Oct 5 to Sun Oct 11** window. This milestone collects the proof that it
did: the date and time, who attended, and the two or three decisions that came
out of it. For each decision, say what you changed. Where you kept your course,
say so plainly and say why the meeting did not move you. A meeting that changed
nothing and cannot say why was a status report.

Record it the day it happens rather than reconstructing it in November. The
conversation itself is human work, so your AI Research Ledger gets a row only
for what you delegated afterwards. **Round 02 is requested at M8 and confirmed
at M14.**

---

## The Book Anchor — "It Is Your Turn"

This milestone is anchored in the course book, **EDR\|AI**. Read the chapters
below as you develop the milestone, and complete each chapter's closing **"It
is your turn"** section in its companion Colab notebook (or carry the same
work inside your project notebook) **by the date that chapter's reading is
due**:

- Ch. 22 — [AI as Programmer](https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464/book/part4-credible-evidence/19-ai-as-programmer.html) · [companion notebook](https://colab.research.google.com/github/davi-moreira/2026F_evidence_driven_research_purdue_HONR464/blob/main/notebooks/book/ch22_ai_as_programmer.ipynb)
- Ch. 23 — [AI as Analytical Assistant](https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464/book/part4-credible-evidence/20-ai-as-analytical-assistant.html) · [companion notebook](https://colab.research.google.com/github/davi-moreira/2026F_evidence_driven_research_purdue_HONR464/blob/main/notebooks/book/ch23_ai_as_analytical_assistant.ipynb)

These sections are the point of the reading, not extra work: across the
semester, the book's "It is your turn" sections — one per lesson, submitted on the date its reading is due — chain into a complete research artifact, so what you complete here is a
draft piece of your own. You hand each section in on the date its own reading is due, under
**IYT Practice** — the dated list is on the course page. They are not
collected a second time here: carry the completed work forward into this
milestone and your Research Project Dossier.

---

## Purpose

Everything your project has said so far, it has said in words. Your Contract
names the question, your route declaration names the design, and your
measurement plan names how each concept becomes a column. This week the words
become running code, and your project produces its first number.

The artifact is one honest result you can reproduce from a clean start, with its
uncertainty attached. Studio 7 runs both halves of that sentence inside a single
week. Monday you hand the writing of code to AI and keep every judgment for
yourself. Wednesday you execute the analysis, attach its uncertainty, and verify
that what printed is what you can defend. Friday is the milestone.

One discipline is simple to state and hard to keep: your notebook implements the
**declared analysis** and nothing else. The declared analysis is the one your
Contract and route declaration committed you to before any result was visible.
For example, if you declared a difference in group means with a bootstrap
interval, you compute that, not the four alternatives that occurred to you once
the first number looked disappointing. A method chosen after seeing which one
flatters your data proves nothing, and the pipeline is where your pre-commitment
gets kept in code a reader can run.

Then the number has to survive a **clean restart**: a rerun from a fresh runtime,
with memory cleared, using Restart & Run All from the top. It matters because
notebooks accumulate **hidden state**, values left in memory by cells you edited
or ran out of order. You rename a column, the old one still lives in memory,
every cell below keeps working, and every number below may be wrong. A notebook
that ran once is a draft. A notebook that runs from nothing is evidence.

Verification here is five checks, not one. The restart must match. Every number
you plan to report must trace to the cell that produced it. The uncertainty
itself must reproduce, not only the point estimate. Two key numbers must survive
re-derivation by routes that share no code with the original. And a required
auditor must find no leak and no unlicensed generalization in what you plan to
say. If a number moves on the restart, the pipeline is the finding, and you
explain and fix the cause before any claim goes forward.

The same Friday carries a second, fixed anchor: the **URC abstract internal
gate**. The abstract is the short public description of your project, and it
leaves the course on the conference's calendar rather than on your research
schedule. So it clears an internal check here, bounded by exactly what this
week's verified result licenses and nothing beyond it.

> **A question that often comes up here:** *"My numbers matched on the first
> restart. Am I done?"* A match is the entry ticket, not the milestone. A
> pipeline can reproduce a wrong number perfectly, run after run. The
> claim-to-output trace catches the number you misquoted in your prose, the
> re-derivation catches the bug both runs shared, and the leakage audit catches
> the sentence that quietly claims more than the pipeline computed. All five
> checks together are what verified means here.

## Components

### 1. The pipeline: your declared analysis in code

Build the seeded notebook (`SEED = 464`) that runs top to bottom: data in,
declared analysis, result out. Three rules govern it.

- **It implements the declared analysis, and nothing else.** Write the analysis
  your Contract and route declaration commit you to, before you look at anything
  else. Exploration that touches the reported result is not exploration; it is
  an undeclared analysis.
- **It loads data from the source your M6 governance record documents**, so a
  reader can follow the pipeline all the way back to provenance.
- **Every number it reports traces to a data cell and a line of code.** No
  number appears in your prose that the notebook does not compute.

Delegate the writing of code as freely as you like, and verify everything that
comes back. Two checks cover the code AI wrote for you. The **line review** is
reading every returned line and saying in your own words what it does; any line
you cannot explain gets rewritten or removed, because you cannot defend a
pipeline you cannot narrate. The **known-answer test** is running a piece of
code on a tiny input whose right answer you already know. For example, feed your
group-difference function two three-row groups you can average by hand, and
confirm it returns exactly that. Both checks live in the notebook, next to the
code they verify, and each one earns a ledger row.

### 2. The result, with its uncertainty

Report the one result your declared analysis produces, in the form your route
and Contract specified, with its **uncertainty statement** attached: the
interval, spread, standard error, or held-out range your route provides. A
result reported without uncertainty is not yet a result.

The form is route-specific. If your route predicts, report your held-out
performance beside the declared baseline it has to beat. For the other routes,
report the quantity your Contract named, computed by the estimator it named.
Then read the number in one sentence: what it says, for which units, and what it
does not cover.

### 3. The clean restart and the environment record

Restart your runtime so memory is empty, then Restart & Run All. Record three
things. First, the **environment record**: one cell that prints your Python
version, your library versions, and your data files with the date each was
retrieved. Second, the headline numbers before and after the restart. Third, the
verdict. If the numbers match, say so, to the digit you report. If any number
moves, explain the discrepancy, fix its cause, and restart again until the
pipeline is stable. "Close enough" is not a category here. A moved digit has a
cause: hidden state, an out-of-order cell, or an unseeded draw. Finding it is a
real result about your own evidence machine.

### 4. The claim-to-output trace

Build the **claim-to-output trace**: a table pointing every number you plan to
report to the specific cell that produces it. One row per number, carrying the
sentence it appears in, the number itself, and the cell. This is what lets a
reader, and a future you, audit your writing against your code in minutes. A
figure with no cell behind it is an **untraceable number**, and it caps your
Verification score.

### 5. Two independent re-derivations, against a tolerance you declare first

Do this for **two** key numbers, not one. An **independent re-derivation** is
the same number reached twice by unrelated paths: by hand from a small table,
with a different library, or from the raw definition written fresh in a new
cell. For example, recompute your pipeline's difference in means from two group
averages you calculate with plain arithmetic.

Before you run the second route, write down your **tolerance**: how close the
two answers must land for you to call it agreement. State it as a number, not as
a feeling. For example, "agreement means the two routes match to three decimal
places," or "within 0.05 percentage points." Declaring the tolerance first is
the whole point, because a tolerance chosen after you see the gap will always
turn out wide enough. If the routes agree inside it, your belief in the number
no longer rests on one script. If they disagree, you just found the bug this
milestone exists to catch, and the fix goes into your clean-restart record.

### 6. The leakage audit (required reviewer role)

Submit your verified draft to the **Prediction & Leakage Auditor**, the required
GenAI Studio reviewer role for this milestone (full briefing in
`genai_studio/roles/prediction_leakage_auditor.md`). Its focus depends on your
route.

- **If your route predicts**, the auditor hunts **data leakage**: a feature
  whose value is only settled at or after the outcome it is supposed to predict.
  Settle each flag with two checks in your own pipeline. The **timing check**
  asks whether the feature's value is known before the prediction moment. The
  **correlation check** asks whether the feature tracks the outcome so tightly
  that it is nearly a copy of the answer. A feature that fails the timing check
  is dropped or re-timed, no matter how much it helps your score.
- **For every other route**, the auditor's focus is your language. It hunts any
  **out-of-sample or generalization claim**, a sentence that quietly extends
  your result to units, times, or populations your design never reached. Every
  flagged sentence gets bounded or cut, and the confirmation that you make no
  unlicensed prediction claim is itself a ledgered result.

For every flag, write your fix or your refutation, each settled by a check in
your own pipeline. The auditor can miss a real leak and invent a false one, so
its flags are hypotheses to test, never verdicts.

### 7. The URC abstract draft (the internal gate)

Write the abstract you would submit to the **Undergraduate Research
Conference**, roughly 150–250 words, describing your project as it now stands:
the question, what you measure, the analysis your pipeline executes, the
verified result with its uncertainty, and the boundary around the claim. This is
an **internal gate**, which means the abstract must clear the instructor's check
at the studio before it goes out externally.

The gate has one non-negotiable rule. The abstract may use only the claims your
current verified result licenses. An abstract that promises a causal finding
your route does not license, that reaches a population your data never touched,
or that states as settled a number no stress test has yet touched, does not
clear the gate. Your result is verified this week and not yet audited: next
week's robustness work can narrow it, and your wording has to survive that
without becoming false.

> **A question that often comes up here:** *"Why write the abstract now, when
> the audit is still ahead?"* Because the abstract's clock is external and this
> Friday is its fixed anchor. The skill being graded is writing a public
> description that is both true today and safe tomorrow: bounded to your route,
> carrying its uncertainty, and worded so no later check can make it
> retroactively false.

### 8. Applying to the conference

The gated abstract has somewhere to go. Once it clears the studio check, apply
to present a poster at the **Fall Undergraduate Research Expo** through Purdue's
Undergraduate Research site:
<https://www.purdue.edu/undergrad-research/conferences/fall/index.php>.

The form asks for a specific set of things, and it is worth having them written
down before you open it:

- **Title.** Your project title, informative rather than clever.
- **Abstract.** The one you just gated. Do **not** put your name inside the
  abstract box.
- **Publication consent.** Yes, the abstract may appear in the booklet.
- **Five keywords** that would let someone working on your question find you.
- **Author.** You. Projects here are individual by default; an approved group
  lists every member.
- **Format.** In person.
- **Availability** on the day: select every slot you can genuinely make.
- **Presentation type.** Poster. You are not applying for a research talk.
- **Research category** and **judging unit**: the ones that fit your question,
  which for an Honors project is usually the discipline your evidence comes from
  rather than the college you are enrolled in. Ask me if it is not obvious.
- **Mentor.** Davi Cordeiro Moreira, `dcordeir@purdue.edu`. The Expo requires a
  faculty mentor of record, and an application without one does not stand.

When the confirmation arrives, save it as a PDF and submit it with this
milestone. That confirmation is your evidence that the step was actually taken,
not merely planned. **The external application deadline is set by the
conference, not by this course, and it is posted on Brightspace. It does not
move because your analysis is still settling.**

### 9. AI Research Ledger rows

Every use of AI in building this milestone gets a row in your **AI Research
Ledger** (the eight-field table: task delegated · tool used · prompt · output
summary · decision · verification method · remaining concern · responsible
researcher). Drafting pipeline code, debugging an error message, writing the
environment-record cell, proposing a re-derivation route, running the Prediction
& Leakage Auditor, and red-teaming your abstract are all delegable tasks, and
each one you delegated needs a row naming how you verified the result. "No AI
used" is a legitimate entry if it is true.

**A missing ledger is not a minor lapse.** Per the course rule, a missing AI
Research Ledger entry scores the Craft criterion **0** and the submission is
**returned** for completion before it is graded.

### 10. The dossier update line and the version line

Open the artifact with its version line: **Book Milestone 7, version 1 (first
reproducible analysis)**, dated, with the reason a reader could use to
reconstruct your thinking. Then end with one line recording what this milestone
finalizes in your **Research Project Dossier**: the reproducible analysis
notebook now exists, verified rather than merely executed, carrying its
uncertainty statement, its environment record, its claim-to-output trace, and a
gated URC abstract. Name the file or section where each now lives.

---

## Definition of Done

You are done when your submission carries all of the following. Use this as a
pre-submission checklist.

| Item | Specification |
|---|---|
| **Pipeline notebook** | Seeded (`SEED = 464`); runs top to bottom from data to result; implements the declared analysis and nothing else |
| **Delegated-code checks** | Every AI-written line reviewed and explained in your own words; the known-answer test run and reported |
| **Result and uncertainty** | Reported in the form your route and Contract specified, with its uncertainty statement, and read in one sentence |
| **Clean restart** | Fresh runtime; Restart & Run All; numbers match to the digit you report, or every discrepancy explained and fixed |
| **Environment record** | Python version, library versions, and data files with retrieval dates, printed by a cell |
| **Claim-to-output trace** | Every number you plan to report pointed to the cell that produces it |
| **Re-derivations** | Two key numbers recomputed by independent routes and judged against a tolerance declared before the run |
| **Leakage audit** | Prediction & Leakage Auditor run; every flag fixed or refuted by a check in your own pipeline |
| **URC abstract** | Roughly 150–250 words; inside the claims your verified result licenses; the internal gate cleared at the studio |
| **Version line** | Book Milestone 7, version 1, dated, with its reason |
| **Permission status** | Your M4/M6 permission determination is still authorized; blocked work does not proceed |
| **AI Research Ledger** | One row per AI-assisted step; every verification method named and non-vague |
| **Dossier line** | The verified notebook, its trace, and the gated abstract located by file or section |
| **Studio work** | Worked at the Friday studio (Oct 9) with your AI assistant; abstract gate cleared; submitted by Tuesday, Oct 13 |
| **Filename** | A shared Colab link or `lastname_m07_first_analysis.ipynb`; optional `lastname_m07_first_analysis.pdf` companion |
| **Location** | Brightspace → Assignments → M07 |

---

## Grading Rubric (100 points)

Four bands on the course's five shared virtues
(`planning/ASSESSMENT_ARCHITECTURE.md`), grounded in the studio's authored
criteria for this checkpoint (`planning/BOOK_ASSESSMENTS.yml`,
`first-analysis-v1`).

| Criterion | Exemplary | Proficient | Developing | Beginning |
|---|---|---|---|---|
| **Compass & pathway alignment** (15) | The pipeline implements exactly the declared analysis; the result answers the declared question in the declared form; the abstract stays inside the route's licence (13–15) | Declared analysis implemented; one link between the result and the declaration loose (10–12) | Undeclared extras feed the reported result, or the result drifts from the declared form (5–9) | The pipeline answers a different question than the project declared (0–4) |
| **Evidence integrity & provenance** (20) | Data loaded from the documented M6 source; the environment is recorded; every reported number traces to a data cell and a line of code (18–20) | Traceable; one trace row or the environment record thin (14–17) | A dataset or number asserted without a locatable origin, or an incomplete trace (8–13) | A source that does not exist, or a number with no path back to data (0–7) |
| **Verification** (30) | The clean restart is run and recorded; every discrepancy explained and fixed; both re-derivations are genuinely independent and judged against a tolerance declared first; the line review and known-answer test are real; every auditor flag settled by a named check; every AI-assisted step ledgered with a non-vague verification (27–30) | All five checks present; one recorded loosely (21–26) | A restart claimed but not recorded, a re-derivation that reuses the original code, a tolerance written after the gap was visible, or a flag answered without a check (14–20) | No clean restart, a discrepancy left unexplained, an auditor flag pasted in or dismissed unverified, or code in the pipeline you cannot explain (0–13) |
| **Uncertainty & claim boundary** (20) | The uncertainty statement is attached, reproduces, and is read correctly; the result is never worded as settled certainty; the abstract makes no promise the evidence cannot keep (18–20) | Uncertainty present and reproducing; one reading or boundary sentence loose (14–17) | A point estimate with no uncertainty, or uncertainty reported but never read (8–13) | The first verified run narrated as a certain finding, or an abstract that overclaims past the route (0–7) |
| **Craft, ledger & abstract gate** (15) | Versioned with its reason, on-format, on-time, gate cleared, complete AI Research Ledger, dossier line present (13–15) | Minor format lapses; abstract and ledger complete (10–12) | Missing pieces, a rushed clinic walkthrough, or an ungated abstract (5–9) | Missing AI Research Ledger (Craft scored 0, submission returned) (0–4) |

**Hard caps (a single failure caps the row regardless of the rest):**

- A **fabricated or unretrievable source** caps *Evidence integrity &
  provenance* at Beginning.
- An **untraceable number** — a reported figure with no path back to your data —
  caps *Verification* at Beginning.
- A **non-reproducing result** — a headline number or interval that does not
  rerun from a fresh runtime — caps *Verification* at Beginning.
- A **missing AI Research Ledger entry** scores *Craft, ledger & abstract gate*
  **0** and the submission is **returned** unread until it is supplied.

**Revision:** eligible under the standing policy — a revised submission within 7
days of feedback recovers up to half the lost points.

## Penalties

- Late: −10 points per day, up to 3 days; not accepted after (documented
  emergencies: talk to me first, per the syllabus).
- Any dataset or source you cite that turns out not to exist or not to be what
  you claim: *Evidence integrity & provenance* scores Beginning regardless of
  the rest — the course's evidence-integrity rule with teeth.
- A headline number or interval that does not rerun from a fresh runtime:
  *Verification* scores Beginning — a number you cannot regenerate is not
  evidence.
- Missing AI Research Ledger entry: *Craft* scores 0 and the submission is
  returned for completion before grading.

## Common Pitfalls

1. **The pipeline that does more than you declared.** Running several
   specifications "to see what happens," then reporting the one that looks best.
   The whole value of declaring first is that the method cannot be chosen to
   flatter the answer. Implement the declared analysis and nothing else; any
   exploration that feeds the reported result undoes your pre-commitment.
2. **The restart that never happened, and the discrepancy waved past.** Trusting
   the in-session numbers because the notebook "just ran," or watching a digit
   move and calling it close enough. Hidden state can keep a wrong number alive
   for weeks, and until you find the cause you do not know which of the two
   numbers is yours. Restart from empty, run everything, and record what printed.
3. **The re-derivation that is not independent.** Calling your own function a
   second time, or writing the tolerance after you see how far apart the two
   answers landed. A second path that shares code shares its bugs, and a
   tolerance chosen afterwards always fits. Pick an unrelated route, and fix the
   number that counts as agreement before you run it.
4. **The abstract that outruns the pipeline.** A URC abstract that promises a
   causal finding, or a population claim, while your pipeline licenses a result
   for the units you analyzed. The abstract must sit inside the claims your
   verified result supports; an abstract that overclaims does not clear the
   internal gate.

---

*Previous: [M06 — Data and Measurement Governance](milestone_06_causal_identification.md) ·
Next: [M08 — Robustness Audit](milestone_08_declared_analysis_protocol.md) —
your verified result now gets attacked on purpose: three checks pre-listed
before you look, a licensed null check, and an adversarial review decide what
survives.*
