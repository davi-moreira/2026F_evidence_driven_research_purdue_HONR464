# Course milestone M7 — Robustness Audit

<!-- book-milestone-bridge:begin -->
> **Book Milestone bridge** — course milestone **M7**.
> This submission presents **Book Milestone 8 — Your robustness audit** (version 1): work from its [milestone page](https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464/book/studios/milestone08-stress-test.html#milestone).
<!-- book-milestone-bridge:end -->

## About the Research Project

Your semester project is **individual**: one researcher, one question, carried
from curiosity to a defended, reproducible claim. It runs through milestones
**M0–M15**, peaks publicly at the **Purdue Fall Undergraduate Research Expo
poster session (Tuesday, November 17 — required)**, and closes with an oral
**Evidence Defense** and a final research chapter in December. Every milestone
follows the same cadence: **Friday-studio kickoff → develop across the week →
submit → revise (where eligible)**. Every milestone also updates your
cumulative **Research Project Dossier** and appends at least one row to your
**AI Research Ledger** — the running record of what you handed to AI and how you
checked it. Milestone weights live in the syllabus;
instructions and rubrics live one page per milestone, like this one.

---

## What to Submit on Brightspace

Due: **Friday, October 16, 11:59 PM** (you work on it at that Friday's studio).
October break shortens this week to one lecture and the studio, so the audit is
planned before it is run. That studio is Studio 8's milestone session, an
**audit walkthrough and adjudication round**: you present your pre-list, show
what survived, and defend every reviewer flag you confirmed or refuted.

| # | File | Description |
|---|---|---|
| 1 | **A shared Colab notebook link** *or* **`lastname_m07_audit.ipynb`** | The eight-part audit record below, carried in the notebook itself or in an optional companion **`lastname_m07_audit.pdf`**: your dated pre-list of three checks with the attack each one answers, the run and what survived, your licensed null check, your reworded claim with its range and compass boundary, the verified AI-review trail, the one limitation no check could fix, your AI Research Ledger rows, and your dossier line. This is the graded artifact. |
| 2 | **EDR\|AI "It is your turn" — ch. 24, ch. 25, ch. 26, ch. 27** | The completed "It is your turn" sections of this milestone's book chapters, worked in their companion Colab notebooks (share the links) or included in your artifact. See "The Book Anchor" below. |

Set sharing so the instructor can open **and rerun** the notebook. Every check
you report has to run from it, so confirm the audit reproduces before you
submit.

---

## The Book Anchor — "It Is Your Turn"

This milestone is anchored in the course book, **EDR\|AI**. Read the chapters
below as you develop the milestone, and complete each chapter's closing **"It
is your turn"** section in its companion Colab notebook (or carry the same
work inside your project notebook):

- Ch. 24 — [Robustness and Sensitivity](https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464/book/part4-credible-evidence/21-robustness-and-sensitivity.html) · [companion notebook](https://colab.research.google.com/github/davi-moreira/2026F_evidence_driven_research_purdue_HONR464/blob/main/notebooks/book/ch21_robustness_and_sensitivity.ipynb)
- Ch. 25 — [Diagnostics and Negative Tests](https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464/book/part4-credible-evidence/22-diagnostics-and-negative-tests.html) · [companion notebook](https://colab.research.google.com/github/davi-moreira/2026F_evidence_driven_research_purdue_HONR464/blob/main/notebooks/book/ch22_diagnostics_and_negative_tests.ipynb)
- Ch. 26 — [AI as Adversarial Reviewer](https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464/book/part4-credible-evidence/23-ai-as-adversarial-reviewer.html) · [companion notebook](https://colab.research.google.com/github/davi-moreira/2026F_evidence_driven_research_purdue_HONR464/blob/main/notebooks/book/ch23_ai_as_adversarial_reviewer.ipynb)
- Ch. 27 — [Recognizing False Confidence](https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464/book/part4-credible-evidence/24-recognizing-false-confidence.html) · [companion notebook](https://colab.research.google.com/github/davi-moreira/2026F_evidence_driven_research_purdue_HONR464/blob/main/notebooks/book/ch24_recognizing_false_confidence.ipynb)

These sections are the point of the reading, not extra work: across the
semester, the book's "It is your turn" sections — one per lesson, collected by the twelve Book Milestones — chain into your final
research chapter, so what you complete here is a draft piece of your final
artifact. Include the completed sections in this milestone's submission (see
the submission table above) and carry them forward in your Research Project
Dossier.

---

## Purpose

At M6 your declared analysis became a pipeline, produced a number, and survived
a clean restart. That makes the number reproducible. It does not yet make it
true. A result you have not tried to break is a result you do not yet know, and
this week you attack your own finding the way a hostile reviewer would.

The artifact is your **robustness audit**: the record of what you tried to break,
what held, and what you still cannot rule out. Its spine has four parts, and
their order is the point.

1. **The pre-list.** Three checks written down before you look at any of their
   results, each one named with the reviewer attack it answers.
2. **What survived.** The checks run and all of them reported, with your claim
   reworded to carry its range and its compass boundary.
3. **The verified AI-review trail.** Every flag an adversarial reviewer raised,
   confirmed or refuted by a check in your own data, including the loudest wrong
   flag it gave you.
4. **The remaining limitation.** The one weakness no check could fix, written by
   you before a reader finds it.

The pre-list comes first because a check invented after a disappointing result
is not a check. It is a search. **Pre-listing** means committing to your checks
and to reporting all of them, whichever way they come out, and dating that
commitment. A grid that shows only the runs that agreed with you tells a reader
nothing except that you were selective.

October break shortens this week, so the planning matters more than usual. You
write the pre-list before the studio, and the studio is where the checks meet
the reviewer and your claim gets rewritten to fit what actually survived.

> **A question that often comes up here:** *"All three of my checks agreed with
> the original result. Isn't that the answer?"* It is a good sign and a narrow
> one. Checks can only find the errors they were built to find, and three
> versions of one flawed comparison will lean the same way together. Agreement
> across your grid tells you the result is stable under the choices you listed.
> It cannot see a mistake all of them share, which is why the remaining
> limitation is a required part of the artifact rather than a confession.

## Components

### 1. The pre-list: three checks, written before you look

Write down three checks before you run any of them, and date the list. For each
one, record two things in the same row: the check itself, and the **reviewer
attack** it answers, meaning the specific objection a skeptical reader would
raise about your result. A check with no attack behind it is decoration.

Pick checks that turn a real handle on your analysis. The **sample** is which
data you keep, for example dropping the largest category and rerunning. The
**measurement** is how a concept becomes a number, for example swapping one
defensible index for another. The **specification** is the bundle of modeling
choices behind the estimate, for example changing a cutoff or a control.

Two rules bind the list. You commit to reporting all three results, including
the ones that hurt. And no check may define its comparison group by something
your treatment or exposure could itself have changed; that comparison may be
worth reporting, in its own place, clearly labeled for what it is.

### 2. The run, and what survived

Run all three and report every one, as **direction and size** together. Direction
is which way the number moved; size is how far. "The gap stayed positive and
ranged from 4.1 to 6.8 points" is a report. "Robust" is not.

Three guard-rails govern how you read the grid.

- **A same-sign spread is a direction plus a range, never an uncertainty
  interval.** The **specification spread** is the span your answer covered
  across the versions you ran, and it measures your choices, not chance. Each
  version still carries its own sampling uncertainty from M6, and the spread is
  not a substitute for it. Report both, and never write the spread with the
  words that belong to an interval.
- **Compare only what is comparable.** Results belong in the same panel when
  they are measured in the same units, about the same group, for the same kind
  of quantity. A check that changes who is counted or what the outcome means
  gets its own labeled panel, and you report a span within a panel, never across
  panels.
- **A complete-case contrast is never "the effect among stayers."** A
  **complete-case contrast** is what you get when you compare only the units
  with complete data, after some dropped out or went missing. Whoever remains is
  a group selected by whatever caused the missingness, so the contrast is not
  the effect for the people who stayed and not the effect for everyone you
  started with. Report it as what it is: a comparison among complete cases, with
  the missingness described.

### 3. The null check your design licenses

Run one **negative test**, a check that runs your exact analysis where the true
answer has to be zero. For example, run the same comparison in a period before
your cause could have acted, or with the group labels replaced by a coin flip.
Write the prediction before the run: what you expect to see if your pipeline is
clean.

Read the result against the **null reference spread**, the range of readings
your own procedure produces when nothing is happening. The true answer is zero;
your sample will almost never return exactly zero, because samples wobble. A
clean pass is a reading that sits comfortably inside that spread. What should
worry you is a reading far outside it, big enough that ordinary wobble is a
strained explanation. Demand exact zeros and you will fail healthy machinery, or
worse, tinker until the readout prints 0.00 and call the tinkering a fix.

Name the test correctly, too. A placebo test replaces the real cause with one
that cannot act. A falsification test checks a consequence that must be false if
your explanation is right. A negative control points your machinery at an
outcome your cause could not touch. State which one you ran, and state the
assumption it rests on.

### 4. The reworded claim, with its range and its boundary

Rewrite your headline claim so it carries what the audit found. Two things must
appear in the sentence.

- **The range.** Not the single best number, but the span it held across your
  pre-listed checks, with its uncertainty reported alongside and labeled as the
  separate thing it is.
- **The compass boundary.** Name your claim's **kind**, meaning descriptive or
  causal, and its **reach**, meaning the data at hand, a population, or unseen
  cases. Then say what the audit does not license. For example: "Among the units
  in this sample, the difference ranged from 4.1 to 6.8 points across the three
  checks; this is a descriptive comparison for the data at hand, and it does not
  license a causal reading or a claim about units outside the sample."

A claim that gets narrower after an audit is a claim that got better. Narrowing
it now is cheaper than defending it later.

### 5. The verified AI-review trail (required reviewer role)

Commission an adversarial review from the **Robustness & Sensitivity Reviewer**,
the required GenAI Studio reviewer role for this milestone (full briefing in
`genai_studio/roles/robustness_sensitivity_reviewer.md`). Give it your result,
your checks, and your claim, and ask what would break them. Add a peer reviewer
at the studio when one is available; a second human attack finds different
things than a model does.

Neither review is independent verification. An AI reviewer is another critique,
and a confident critique is still just a critique. So every flag gets settled
**by a data check in your own pipeline**, and your trail records four fields per
flag: the flag as raised, the check you ran, the output that check produced, and
your verdict of confirmed or refuted.

Name the **loudest wrong flag**: the objection the reviewer stated most
confidently that your data refuted. Keep it in the record. It is the cheapest
lesson available about the tool you will use again next week, and it is the
reason confidence never counts as evidence here.

### 6. The confidence audit and the one remaining limitation

Close the audit with an honest account of where your belief actually comes from.
Write two short lists and one sentence.

- **The not-yet-recomputed list.** Every number in your artifact that you have
  not recomputed yourself, by hand or by an independent route. Naming them is
  the point; you are not required to have finished them all.
- **The source of your confidence in the headline number.** Your own
  recomputation, a tool's fluent summary, or the fact that it matched what you
  hoped for. Only the first one counts as a reason, and saying so plainly is
  part of the grade.
- **The one limitation no check could fix.** One weakness your audit could not
  reach, stated in one sentence, with what it would take to address it. A
  limitation you volunteer is a boundary. The same limitation found by a reader
  is a hole.

### 7. AI Research Ledger rows

Every use of AI in this audit gets a row in your **AI Research Ledger** (the
eight-field table: task delegated · tool used · prompt · output summary ·
decision · verification method · remaining concern · responsible researcher).
Proposing candidate checks, writing the code for a robustness run, running the
Robustness & Sensitivity Reviewer, and drafting the reworded claim are all
delegable tasks, and each one you delegated needs a row naming how you verified
the result. "No AI used" is a legitimate entry if it is true.

**A missing ledger is not a minor lapse.** Per the course rule, a missing AI
Research Ledger entry scores the Craft criterion **0** and the submission is
**returned** for completion before it is graded.

### 8. The dossier update line and the version line

Open the artifact with its version line: **Book Milestone 8, version 1
(robustness audit)**, dated, with the reason: what the audit changed about your
claim, and why. Then end with one line recording what this milestone finalizes
in your **Research Project Dossier**: the robustness and diagnostic record now
exists, together with the reworded claim it licenses and the limitation it could
not remove. Name the file or section where each now lives.

---

## Definition of Done

You are done when your submission carries all of the following. Use this as a
pre-submission checklist.

| Item | Specification |
|---|---|
| **Pre-list** | Three checks written and dated before any of them ran, each paired with the reviewer attack it answers |
| **Full reporting** | All three results reported, including the ones that hurt; anything added later labeled exploratory |
| **Direction and size** | Every check reported as which way the number moved and by how much, within commensurable panels |
| **Spread discipline** | The specification spread reported as a direction plus a range, never as an uncertainty interval |
| **Complete-case honesty** | Any comparison restricted to complete cases labeled as such, with the missingness described, never as the effect among those who stayed |
| **Null check** | One negative test, named correctly, with the prediction written before the run and the result read against the null reference spread |
| **Reworded claim** | The headline claim carrying its range, its uncertainty, its kind and reach, and what the audit does not license |
| **AI-review trail** | Robustness & Sensitivity Reviewer run; every flag settled by a data check with its output; the loudest wrong flag named |
| **Confidence audit** | The not-yet-recomputed list, the source of your belief in the headline number, and the one limitation no check could fix |
| **Version line** | Book Milestone 8, version 1, dated, with a reason a reader could reconstruct |
| **Permission status** | Your permission determination is still authorized; blocked work does not proceed |
| **AI Research Ledger** | One row per AI-assisted step; every verification method named and non-vague |
| **Dossier line** | The audit record and the reworded claim located by file or section |
| **Studio work** | Worked at the Friday studio (Oct 16) with your AI assistant; required reviewer role logged; submitted the same day |
| **Filename** | A shared Colab link or `lastname_m07_audit.ipynb`; optional `lastname_m07_audit.pdf` companion |
| **Location** | Brightspace → Assignments → M07 |

---

## Grading Rubric (100 points)

Four bands on the course's five shared virtues
(`planning/ASSESSMENT_ARCHITECTURE.md`), grounded in the studio's authored
criteria for this checkpoint (`planning/BOOK_ASSESSMENTS.yml`,
`robustness-audit-v1`).

| Criterion | Exemplary | Proficient | Developing | Beginning |
|---|---|---|---|---|
| **Compass & pathway alignment** (15) | Every check tests the same substantive claim; panels are commensurable; the reworded claim names its kind and reach and stops there (13–15) | Aligned; one panel or boundary sentence loose (10–12) | A check that answers a different question is folded in, or the reworded claim drifts past the route (5–9) | The audit tests something other than the declared claim, or the claim keeps a reach the design never had (0–4) |
| **Evidence integrity & full reporting** (20) | The pre-list is dated before the runs; all three results reported, including the unfavorable ones; every reported figure traces to its output (18–20) | Complete; one trace row or one date thin (14–17) | A result omitted, or a check added later and presented as pre-listed without a label (8–13) | Selective reporting, a fabricated source, or a post-hoc check reported as pre-listed (0–7) |
| **Verification & adjudication** (30) | Every reviewer flag settled by a data check with its output shown; confirmed and refuted flags both present; the loudest wrong flag named; the null check run with its prediction written first; every AI-assisted step ledgered with a non-vague verification (27–30) | All flags settled; one check or one prediction recorded loosely (21–26) | A flag answered by argument rather than by a check, or a null check run without a prior prediction (14–20) | Reviewer flags pasted in or dismissed unverified, or no null check at all (0–13) |
| **Uncertainty & claim boundary** (20) | The spread is reported as a direction plus a range and never as an interval; the negative test is read against the null reference spread; any complete-case contrast is labeled honestly; the remaining limitation is named (18–20) | Present; one of the three guard-rails stated loosely (14–17) | The spread and the uncertainty blurred together, or the negative test judged against exact zero (8–13) | The spread sold as an uncertainty interval, a complete-case contrast reported as the effect among stayers, or no limitation at all (0–7) |
| **Craft, ledger & communication** (15) | Versioned with its reason, on-format, on-time, complete AI Research Ledger, dossier line present (13–15) | Minor format lapses; ledger complete (10–12) | Missing pieces or a rushed record (5–9) | Missing AI Research Ledger (Craft scored 0, submission returned) (0–4) |

**Hard caps (a single failure caps the row regardless of the rest):**

- A **fabricated or unretrievable source** caps *Evidence integrity & full
  reporting* at Beginning.
- A **post-hoc check reported as pre-listed**, or a check you ran and did not
  report, caps *Evidence integrity & full reporting* at Beginning.
- A **specification spread presented as an uncertainty interval** caps
  *Uncertainty & claim boundary* at Beginning.
- A **missing AI Research Ledger entry** scores *Craft, ledger & communication*
  **0** and the submission is **returned** unread until it is supplied.

**Revision:** eligible under the standing policy — a revised submission within 7
days of feedback recovers up to half the lost points.

## Penalties

- Late: −10 points per day, up to 3 days; not accepted after (documented
  emergencies: talk to me first, per the syllabus).
- Any dataset, result, or source you cite that turns out not to exist or not to
  be what you claim: *Evidence integrity & full reporting* scores Beginning
  regardless of the rest — the course's evidence-integrity rule with teeth.
- A check you ran and did not report, or one added after a disappointing result
  and presented as pre-listed: *Evidence integrity & full reporting* scores
  Beginning — selective reporting is the failure this milestone exists to
  prevent.
- Missing AI Research Ledger entry: *Craft* scores 0 and the submission is
  returned for completion before grading.

## Common Pitfalls

1. **The check invented after the result.** Running versions until one looks
   reassuring, then presenting that set as the plan. Dates are what separate an
   audit from a search. Write and date the three checks first, report all three,
   and label anything you add afterwards as exploratory.
2. **The spread sold as an interval.** Writing "the effect is between 4.1 and
   6.8 points" when that span came from your analysis choices. The spread says
   how much your decisions moved the number; the uncertainty says how much
   chance could. Report them as two different quantities, because they answer
   two different questions.
3. **The negative test judged against exact zero.** Declaring a clean pipeline
   because a placebo returned 0.03, or condemning it because one returned 0.4,
   with no idea what your own procedure produces when nothing is happening.
   Build the null reference spread first, then read the reading against it.
4. **The dropped rows renamed as a finding.** Reporting a complete-case contrast
   as "the effect among the people who stayed." Whoever stayed was selected by
   whatever caused the missingness, so that sentence names a group you did not
   choose and cannot describe. Label the contrast for what it is and describe
   the missingness.
5. **The flag settled by tone.** Accepting a reviewer's objection because it
   sounded certain, or dropping one because it sounded odd. Confidence is not
   evidence, and the loudest flag is often the wrong one. Turn every flag into a
   check, show the output, and let only the output decide.

---

*Previous: [M06 — First Reproducible Analysis (+ URC Abstract Internal Gate)](milestone_06_experimental_measurement_protocol.md) ·
Next: [M08 — Bounded Research Note and Claim-Evidence Table](milestone_08_minimum_viable_analysis.md) —
what survived this audit becomes a written claim, every sentence traced to the
evidence that licenses it.*
