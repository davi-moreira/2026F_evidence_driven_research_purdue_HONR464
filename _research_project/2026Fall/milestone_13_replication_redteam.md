# Milestone 13 — Replication and Red-Team Report

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

This milestone is the whole of the **Replication & red-team** component and is
worth **5% of the course grade**. It runs differently from the rest. There is no
Friday studio: the package is exchanged at the Week-13 studio, and the work is a
**self-paced module over the Thanksgiving break**, submitted the Sunday night you
come back. This once, the artifact you audit is **not your own** — it is a
classmate's finished reproducibility package, anonymized by the instructor so you
cannot tell whose it is. You reproduce its headline number cold, red-team it, and
report what holds. It is revision-eligible under the standing policy.

---

## What to Submit on Brightspace

Due: **Sunday, November 29, 11:59 PM** (async — no class meeting; the exchange
runs on the course discussion board over the break).

| # | File | Description |
|---|---|---|
| 1 | **`lastname_m13_redteam.pdf`** *or* a shared Colab notebook link | The five-part **Replication and Red-Team Report** below on your assigned peer package: your reproduction log, your claim-to-output trace, one alternative specification and one hidden assumption, your verified GenAI Studio pass, and your prioritized recommendations. This is the graded artifact. |
| 2 | **The board post + one reply** | Post your single **most-threatening weakness** (with the check that would settle it) to the async board, and reply substantively to **one** classmate's post. Both are part of the grade. |

If you submit a notebook link, set sharing so the instructor can open it, and make
sure every reproduction cell runs top to bottom when opened. Attach your **AI
Research Ledger** rows inside the report. The package you were assigned is
anonymized: **do not** try to identify the author, and paste only the cleared
contents the instructor handed you into any AI tool.

---

## Purpose

"It works on my machine" is not reproducibility — it is a rumor. This milestone
tests the real thing on someone else's work: could **you**, a cold stranger,
rebuild a peer's headline number from the package they shipped, using nothing
outside it, and then say honestly where that number is fragile? You do two jobs
that a green check cannot do for you. First **reproduction**: regenerating a
study's reported number from the same data and code it shipped, run by a different
person. (This is not **replication**, which is a similar result from a *new* study
or new data. This is the same package, same number, your hands.) Second the
**red-team**: once the number regenerates, you attack it — you line each written
claim against the output behind it, you swap one defensible choice the author never
disclosed, you push on one assumption the analysis quietly leans on, and you rank
what you find by how much each weakness threatens the claim.

The trap this milestone exists to refuse is **"it ran, so it's fine."** A clean
**restart-and-run-all** (clearing the notebook's memory and running every cell from
the top with no manual fixes) proves the code *executes*. It says nothing about
whether the write-up's sentence matches what the code computed, whether a different
reasonable choice moves the number, or whether an assumption buried in the analysis
is false. Those are the questions a red-team asks, and none is answered by a green
check. A weakness you surface now, in private, becomes an honest caveat your peer
can add. The same weakness left buried becomes the question that ends their defense.

> **A question that often comes up here:** *"If the notebook runs top to bottom
> with no errors, hasn't the package already passed?"* No, and that is the entire
> point of M13. A clean run certifies that code executes. It never certifies that
> the sentence on the poster is true. Reproduction earns you a trustworthy number;
> the red-team is where you find out what that number can and cannot hold. Your job
> is not to make a new claim of your own — it is to test whether theirs survives
> the exact trace you will soon run on your own dossier.

## Components

### 1. The reproduction log

Open your assigned package and run **restart-and-run-all** from a clean start.
Then log, plainly:

- **Did it reproduce?** Whether the run completed top to bottom with no manual
  fixes, and every break you hit, with the **exact cell** where it broke.
- **The headline number.** The single figure the study's main claim rests on
  (for example, "canvassing raised turnout by 4 points"), as **your** run
  produced it — not as the write-up states it.
- **Did it match?** Whether your reproduced number matches the write-up's stated
  number, and if not, by how much.

This log is your **attestation**: you are the cold replicator, and you sign off on
whether the peer's headline number regenerates from the package alone. If part of
it does **not** reproduce, that is a finding, not a failure — log the residual
honestly, name what broke and where, and say what a fix would require. Concealing a
break costs more than reporting one.

> **A question that often comes up here:** *"The package reproduced cleanly. Isn't
> the audit basically done?"* No — a clean reproduction is the *start* of the
> audit, not the end. It buys you a trustworthy number to interrogate. Everything
> in the rest of this report is what you do *after* the number regenerates, and it
> is where the real findings live.

### 2. The claim-to-output trace

Lay every claim the write-up makes beside the output that is supposed to back it,
so agreement and disagreement sit on one screen instead of in your memory. This is
**claims-vs-computation agreement**: checking that each sentence the write-up
asserts is backed by a number the code actually produces. Flag **every** gap. Two
gaps recur and both belong here:

- **A rounded or restated number.** The write-up says one figure; the code
  produces another (for example, the poster says 4 points and the code says 3.41).
  Small on its own, it tells you the author reported a number the package does not
  produce.
- **Missing uncertainty.** A single settled number reported with no interval and
  no statement of how firm it is. A reader cannot tell signal from noise, so a
  point estimate with no uncertainty is a reporting gap, not a detail.

### 3. One alternative specification and one hidden assumption

Push on the number two ways, exactly as the module rehearsed.

- **One alternative specification** — a different, equally defensible way to
  compute the same headline, to see whether the answer depends on a choice the
  author never disclosed (for example, weighting the data or leaving it
  unweighted). Report the number both ways and the size of the swing between them.
  Neither endpoint is automatically "the truth"; the finding is that the choice
  moves the number and was not disclosed.
- **One hidden assumption** — a claim the analysis quietly relies on and never
  states, which the result would not survive without (for example, treating every
  observation as independent when the data are **clustered** — grouped so that
  members of a group are more alike than members of different groups, and so carry
  less independent information than their raw count suggests). Show what happens to
  the number, or to the certainty around it, when you honor the assumption instead
  of ignoring it.

For each, say in one phrase whether it **moves** the estimate, **widens** its
uncertainty, or **breaks** the claim outright.

### 4. The required GenAI Studio pass, verified by your own run

M13 requires one pass through Purdue's **GenAI Studio Reproducibility Auditor**,
the course-configured role that reads a package the way a cold replicator would and
returns a **reproduction gap list** and a **claim-to-output trace**
(`genai_studio/roles/reproducibility_auditor.md`). Paste only the cleared package
contents. The role proposes; it cannot run code, so every gap it names is a
**suspect you test yourself**, not a verdict. Report which of its flags **survived
your own run**, and which you added or dropped.

Name the trap the module warned you about. **Correlated errors across tools** means
two AI readers make the *same* mistake, so their agreement feels like confirmation
when it is one flaw echoed twice (for example, Gemini and the Auditor both miss the
clustering and both call the package sound). Two models agreeing on a reading they
did without running anything is not two votes — it is one, counted twice. Your own
run is the only evidence that settles it.

> **A question that often comes up here:** *"If the Auditor and Gemini both say the
> package reproduces, can I report that it reproduces?"* No. Neither tool executed
> the code. A package reproduces when **you** run it and the number comes back,
> full stop. Reporting a reproduction on the strength of two AI readings is exactly
> the correlated-error trap, and the rubric caps it.

### 5. Prioritized recommendations and the most-threatening weakness

Order your findings by how much each one threatens the headline claim, **not** by
how easy each is to fix. These are your **prioritized recommendations** (also
called **triaged recommendations**): a clustering error that could dissolve the
result outranks a rounding stretch, even though the rounding is faster to repair.
Ease is the author's concern when they sit down to revise; your job is to tell them
where the claim is in the most danger.

Then name the single weakness you would put at the **top of the board**: the one
most likely to move, weaken, or break the claim, and the **one check** that would
confirm or dissolve it. This is what you post to the async discussion board. If you
cannot yet rank a finding because a check is still unrun, that is a finding too — it
names the run you still owe before Sunday.

### 6. AI Research Ledger rows

Every use of AI in building this report gets a row in your **AI Research Ledger**
(the eight-field table: task delegated · tool used · prompt · output summary ·
decision · verification method · remaining concern · responsible researcher).
Walking through a reproduction cell, building a claim-to-output table, and the
required GenAI Studio pass are all delegable tasks, and each one you delegated needs
a row that names how you verified the result **against your own run**. The pattern
this milestone grades hardest: the AI proposes suspects, your run confirms. "No AI
used" is a legitimate entry if it is true.

**A missing ledger is not a minor lapse.** Per the course rule, a missing AI
Research Ledger entry scores the Craft criterion **0** and the submission is
**returned** for completion before it is graded.

### 7. Dossier update line

End with one line recording what this milestone adds to your **Research Project
Dossier**: your replication record now carries a reproduction log, a claim-to-output
trace, an alternative-specification and hidden-assumption stress test, a verified
GenAI Studio pass, and a threat-ranked recommendation list for a peer's package.
Name the file or section where each now lives. That record is the audit you will
turn inward at M14, when the package under the microscope is your own.

---

## Submission Expectations

| Item | Specification |
|---|---|
| **Length** | The five-part report + ledger rows (typically 2–4 pages PDF, or the equivalent notebook sections) |
| **Reproduction** | A real restart-and-run-all on the assigned package; the reproduced headline number stated as *your* run produced it, with every break logged to the exact cell |
| **Exchange** | The async board post (your most-threatening weakness + the check that settles it) and one substantive reply to a classmate — both part of the grade |
| **Style** | Plain language; every finding points at a number you actually produced; the alternative specification and hidden assumption each say whether they move, widen, or break the claim |
| **Filename** | `lastname_m13_redteam.pdf` (or a shared Colab link) |
| **Location** | Brightspace → Assignments → M13 |

---

## Grading Rubric (100 points)

Four bands on the course's five shared virtues (`planning/ASSESSMENT_ARCHITECTURE.md`).

| Criterion | Exemplary | Proficient | Developing | Beginning |
|---|---|---|---|---|
| **Reproduction & red-team correctness** (30) | Headline number cold-reproduced and logged as *your* run produced it; claim-to-output trace flags every gap; one alternative specification and one hidden assumption each stress-tested with the number both ways; recommendations ranked by threat, not ease; the report stays inside what reproduction and a red-team can establish (26–30) | Reproduction and trace correct; one of the two stress tests thin, or the ranking slips once toward ease (21–25) | Reproduction present but the trace or a stress test missing, or the ranking ordered by ease throughout (13–20) | "It ran, so it's fine" — a clean run reported as if it settled the claim; no trace, no stress test (0–12) |
| **Evidence integrity** (20) | Every number in the report traces to the package or to your own run; any source or claim you name is real and retrievable; the reader can follow each figure back to where it came from (18–20) | Real and traceable; one number lightly sourced (14–17) | A reported figure asserted without a path back to the package or your run (8–13) | A fabricated or unretrievable source, or a headline number the package does not actually produce reported as if it did (0–7) |
| **Verification of AI-assisted parts** (20) | Every AI-assisted step (Gemini, the GenAI Studio Auditor) has a ledger row with a named, non-vague verification method; the reproduced number is confirmed by *your* run, not the tool's trace; the correlated-error trap is named and avoided (18–20) | Ledger present; one method vague or one step unlogged (14–17) | AI outputs used but verification not named; the Auditor's trace accepted without an independent run (8–13) | A reproduction "pass" reported on two AI readings with no run behind it, or an AI-drafted finding reproduced with no verification (0–7) |
| **Uncertainty & limitations** (20) | The report states what reproduction does *not* establish (regeneration, not truth); the missing-uncertainty gap is flagged; residuals or unrun checks are named honestly; no finding oversold beyond the number that supports it (18–20) | Boundaries and residuals present; uncertainty or an overstatement stated loosely (14–17) | Limits gestured at; an unrun check hidden, or a modest swing described as damning (8–13) | No boundary — reproduction treated as proof the science is right, or a residual concealed (0–7) |
| **Craft, ledger & communication** (10) | On-format, on-time; board post + one reply completed; complete AI Research Ledger; dossier line present (9–10) | Minor format lapses; ledger complete (7–8) | Missing pieces, no board reply, or a rushed report (4–6) | Missing AI Research Ledger (Craft scored 0, submission returned) (0–3) |

**Hard caps (a single failure caps the row regardless of the rest):**

- A **fabricated or unretrievable source** caps *Evidence integrity* at Beginning.
- An **untraceable number** — a figure in your report with no path back to the
  package or to your own run — caps *Verification of AI-assisted parts* at
  Beginning.
- A **non-reproducing result you report as reproduced** — claiming a clean
  reproduction the package cannot actually deliver — caps *Verification of
  AI-assisted parts* at Beginning. An honest "it did not reproduce, and here is
  what broke" never triggers this; the cap is for the false pass, not the failure.
- A **missing AI Research Ledger entry** scores *Craft, ledger & communication*
  **0** and the submission is **returned** unread until it is supplied.

**Revision:** eligible under the standing policy — a revised report within **7
days** of feedback recovers up to half the lost points.

## Penalties

- Late: −10 points per day, up to 3 days; not accepted after (documented
  emergencies: talk to me first, per the syllabus).
- Reporting a clean reproduction the package cannot actually deliver is an
  evidence-integrity violation: *Verification of AI-assisted parts* scores
  Beginning regardless of the rest. An honest residuals log never triggers this.
- Any source you cite that turns out not to exist or not to say what you claim:
  *Evidence integrity* scores Beginning regardless of the rest.
- Missing AI Research Ledger entry: *Craft* scores 0 and the submission is returned
  for completion before grading.

## Common Pitfalls

1. **"It ran, so it's fine."** The definitional failure of M13. A clean
   restart-and-run-all proves the code executes; it says nothing about whether the
   write-up's sentence matches the output, whether a different choice moves the
   number, or whether a buried assumption is false. Reproduction earns you a
   number; the red-team is the grade.
2. **Trusting the tool's trace instead of your run.** The GenAI Studio Auditor and
   Gemini both read; neither runs code. If both call the package sound, that is the
   correlated-error trap, not confirmation — one flaw echoed twice. Confirm every
   flag that survives against a number *you* produced, and log the run that decided
   it.
3. **Ranking by ease instead of threat.** Leading with the quick typo fix and
   burying the clustering assumption that could dissolve the claim. Your peer can
   decide the repair order; your job is to tell them where the claim is in the most
   danger. Rank by threat to the headline, every time.

---

*Previous: [M12 — Conference Reflection & Poster-Criticism Portfolio](milestone_12_conference_reflection.md) ·
Next: [M14 — Research-Note Draft & Reproducibility Capsule](milestone_14_research_note_capsule.md) —
the cold audit you just ran on a peer turns inward: the package under the
microscope becomes your own, and every claim you write has to survive the exact
trace you used here.*
