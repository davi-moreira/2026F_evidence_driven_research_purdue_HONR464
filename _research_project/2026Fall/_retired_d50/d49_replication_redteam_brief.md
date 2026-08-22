# Course milestone M16 — Replication and Red-Team Report

<!-- book-milestone-bridge:begin -->
> **Book Milestone bridge** — course milestone **M16**.
> This submission presents **Book Milestone 11 — Your reproducible package** (peer cold-run practice, applied to another researcher's package): work from its [milestone page](https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464/book/studios/milestone11-reproduce-and-package.html#milestone).
<!-- book-milestone-bridge:end -->

## About the Research Project

Your semester project is **individual**: one researcher, one question, carried
from curiosity to a defended, reproducible claim. It runs through milestones
**M1–M17**, peaks publicly at the **Purdue Fall Undergraduate Research Expo
poster session (Tuesday, November 17 — required)**, and closes with an oral
**Evidence Defense** and a final research chapter in December. Every milestone
follows the same cadence: **Friday-studio kickoff → develop across the week →
submit → revise (where eligible)**. Every milestone also updates your
cumulative **Research Project Dossier** and appends at least one row to your
**AI Research Ledger** — the running record of what you handed to AI and how you
checked it. Milestone weights live in the syllabus;
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
| 1 | **`lastname_m13_redteam.pdf`** *or* a shared Colab notebook link | The eight-part **Replication and Red-Team Report** below on the package you were assigned: your intake and privacy check, your environment-recreation record, your cold run, your output comparison including the uncertainty, your undocumented-instruction log, your red-team of the claims, the required Reproducibility Auditor pass verified by your own run, and your repair handoff. This is the graded artifact. |
| 2 | **The board post + one reply** | Post your single **most-threatening weakness** (with the check that would settle it) to the async board, and reply substantively to **one** classmate's post. Both are part of the grade. |
| 3 | **EDR\|AI "It is your turn" — ch. 36** | The completed "It is your turn" sections of this milestone's book chapters, worked in their companion Colab notebooks (share the links) or included in your artifact. See "The Book Anchor" below. |

If you submit a notebook link, set sharing so the instructor can open it, and make
sure every reproduction cell runs top to bottom when opened. Attach your **AI
Research Ledger** rows inside the report. The package you were assigned is
anonymized: **do not** try to identify the author, **do not** contact them for
help, and paste only the cleared contents the instructor handed you into any AI
tool. A run the author helped with is not the run this milestone asks for.

---

## The Book Anchor — "It Is Your Turn"

This milestone is anchored in the course book, **EDR\|AI**. Read the chapters
below as you develop the milestone, and complete each chapter's closing **"It
is your turn"** section in its companion Colab notebook (or carry the same
work inside your project notebook):

- Ch. 36 — [Replication and Reproduction](https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464/book/part6-after-conference/32-replication-and-reproduction.html) · [companion notebook](https://colab.research.google.com/github/davi-moreira/2026F_evidence_driven_research_purdue_HONR464/blob/main/notebooks/book/ch32_replication_and_reproduction.ipynb)

These sections are the point of the reading, not extra work: across the
semester, the book's "It is your turn" sections — one per lesson, collected by the twelve Book Milestones — chain into your final
research chapter, so what you complete here is a draft piece of your final
artifact. Include the completed sections in this milestone's submission (see
the submission table above) and carry them forward in your Research Project
Dossier.

---

## Purpose

Your own package already exists. You assembled it, ran it cold, and locked it at
M13, and it comes back for repair at M16. So this week is not a checkpoint on your
work. It is the same job carried out on someone else's, and that is the one
version of the test you can never run on yourself.

"It works on my machine" is not reproducibility; it is a rumor. The question here
is whether **you**, a cold stranger, can rebuild a classmate's headline number and
its uncertainty from the package they shipped, using nothing outside it, and then
say honestly where that number is fragile. You do two jobs that a green check
cannot do for you. First **reproduction**: regenerating a study's reported result
from the same data and code it shipped, run by a different person. (This is not
**replication**, which is a similar result from a *new* study or new data. This is
the same package, the same number, your hands.) Second the **red-team**: once the
number regenerates, you attack it — you line each written claim against the output
behind it, you swap one defensible choice the author never disclosed, you push on
one assumption the analysis quietly leans on, and you rank what you find by how
much each weakness threatens the claim.

One rule governs the whole module. **An author-assisted run is never independent
verification.** The moment you ask the author what to run, or they tell you which
cell to repair, your run stops measuring the package and starts measuring the
conversation. The package is anonymized precisely so that conversation cannot
happen. Every question you would have needed to ask is a **missing line of
documentation**, and it belongs in your log rather than in a message.

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
> point of M16. A clean run certifies that code executes. It never certifies that
> the sentence on the poster is true. Reproduction earns you a trustworthy number;
> the red-team is where you find out what that number can and cannot hold. Your job
> is not to advance a claim of your own. It is to test whether theirs survives the
> same trace your own package meets again at M16.

## Components

### 1. The intake and privacy check

Before you run anything, confirm what you were handed. Open the assigned package,
check that it carries no identifying information, and confirm it is the cleared
version the instructor distributed. Log three lines: the package identifier, the
date you received it, and your confirmation that it is identity-stripped and
cleared for this exercise.

Two rules bind from here on. Do not try to identify the author and do not contact
them. And paste only cleared package contents into any AI tool, because anything
you paste leaves your control. If the package contains something that looks like
personal or restricted data, stop and tell the instructor before you run a single
cell. A permission problem caught at intake costs one email; the same problem
caught after you pasted the data costs far more.

### 2. Environment recreation

A package that runs only inside its author's already-configured machine has not
been tested. **Environment recreation** means rebuilding the software conditions
the code needs from the record inside the package, before you run it: the language
version, the libraries and their versions, and the random seed. Do this in a clean
session, and a fresh Colab runtime is the simplest clean room you have.

Log what the package told you and what it did not. Which versions were pinned,
which you had to guess, and whether any guess changed a result. A missing
environment record is a finding on its own, and it is one of the most common
reasons a number fails to come back.

### 3. The cold run

Now run it. **Restart-and-run-all** means clearing the session's memory and running
every cell from the top with no manual intervention. Follow only the written
instructions inside the package. Then log, plainly:

- **Did it run?** Whether the run completed top to bottom without intervention,
  and every break you hit, with the **exact cell** where it broke.
- **What you had to do anyway.** Any fix you applied to get past a break, written
  as the instruction the package should have carried.
- **Was the run independent?** Sign a one-line attestation that no author help
  reached you. If any did, say so plainly, and report the run as assisted rather
  than independent.

This log is your **attestation**: you are the cold replicator, and you sign off on
whether the package regenerates its own headline result. If part of it does **not**
reproduce, that is a finding rather than a failure. Log the residual honestly, name
what broke and where, and say what a fix would require. Concealing a break costs
more than reporting one.

> **A question that often comes up here:** *"The package reproduced cleanly. Isn't
> the audit basically done?"* No — a clean reproduction is the *start* of the
> audit, not the end. It buys you a trustworthy number to interrogate. Everything
> in the rest of this report is what you do *after* the number regenerates, and it
> is where the real findings live.

### 4. The output comparison, including the uncertainty

Put the package's reported numbers beside the numbers your run produced, in one
table, so agreement and disagreement sit on one screen instead of in your memory.
Three things get compared:

- **The point estimate.** The single figure the main claim rests on (for example,
  "canvassing raised turnout by 4 points"), as **your** run produced it, not as
  the write-up states it. Say whether it matches, and if not, by how much.
- **The uncertainty around it.** The interval, the standard error, or whatever the
  package reports about how firm that number is. **Reproducing a point estimate
  while ignoring its uncertainty is a half-reproduction**, because the same
  estimate with a much wider interval is a different result. If the package reports
  no uncertainty at all, that absence is itself a finding.
- **Every other claim in the write-up.** This is the **claim-to-output trace**:
  each sentence the write-up asserts, laid beside the output that is supposed to
  back it. Flag every gap.

Two gaps recur and both belong here:

- **A rounded or restated number.** The write-up says one figure; the code
  produces another (for example, the poster says 4 points and the code says 3.41).
  Small on its own, it tells you the author reported a number the package does not
  produce.
- **Missing uncertainty.** A single settled number reported with no interval and
  no statement of how firm it is. A reader cannot tell signal from noise, so a
  point estimate with no uncertainty is a reporting gap, not a detail.

### 5. The undocumented-instruction log

Every place you had to guess, infer, or would have had to ask the author is a
missing line of documentation, and this log is where each one lands. Write the
question you would have asked, the guess you made instead, and whether that guess
changed the result.

This log is often the most useful thing you hand back. Authors cannot see the
instructions they never wrote down, because they already know them; you can,
because you do not. Ordinary entries: which file to open first, what the run order
is, where the data comes from and whether it ships with the package, what a filter
step excludes and why, and where the outputs are supposed to appear.

### 6. The red-team of the claims

Once a number regenerates, attack it. Push on it two ways, exactly as the module
rehearsed.

- **One alternative specification** — a different, equally defensible way to
  compute the same headline, to see whether the answer depends on a choice the
  author never disclosed (for example, weighting the data or leaving it
  unweighted). Report the number both ways and the size of the swing between them.
  Neither endpoint is automatically "the truth"; the finding is that the choice
  moves the number and was not disclosed.
- **One hidden assumption** — a claim the analysis quietly relies on and never
  states, which the result would not survive without (for example, treating every
  observation as independent when the data are **clustered**, grouped so that
  members of a group are more alike than members of different groups and so carry
  less independent information than their raw count suggests). Show what happens to
  the number, or to the certainty around it, when you honor the assumption instead
  of ignoring it.

For each, say in one phrase whether it **moves** the estimate, **widens** its
uncertainty, or **breaks** the claim outright. And stay inside your remit. You are
testing whether the author's claim survives, not advancing a claim of your own.

### 7. The required GenAI Studio pass, verified by your own run

M16 **requires** one pass through Purdue's **GenAI Studio Reproducibility
Auditor**, the course-configured role that reads a package the way a cold
replicator would and returns a **reproduction gap list** and a **claim-to-output
trace** (`genai_studio/roles/reproducibility_auditor.md`). Paste only the cleared
package contents. The role proposes; it cannot run code, so every gap it names is
a **suspect you test yourself**, not a verdict. Report which of its flags
**survived your own run**, and which you added or dropped.

Name the trap the module warned you about. **Correlated errors across tools** means
two AI readers make the *same* mistake, so their agreement feels like confirmation
when it is one flaw echoed twice (for example, your AI and the Auditor both miss the
clustering and both call the package sound). Two models agreeing on a reading they
did without running anything is not two votes — it is one, counted twice. Your own
run is the only evidence that settles it.

> **A question that often comes up here:** *"If the Auditor and your AI both say the
> package reproduces, can I report that it reproduces?"* No. Neither tool executed
> the code. A package reproduces when **you** run it and the number comes back,
> full stop. Reporting a reproduction on the strength of two AI readings is exactly
> the correlated-error trap, and the rubric caps it.

### 8. The repair handoff

Order your findings by how much each one threatens the headline claim, **not** by
how easy each is to fix. This is the **repair handoff**, the document the author
actually works from when they rebuild their package at M16. A clustering error that
could dissolve the result outranks a rounding stretch, even though the rounding is
faster to repair. Ease is the author's concern once they sit down to revise; your
job is to say where the claim is in the most danger.

Give each entry three parts: the finding, why it threatens the claim, and the one
check that would confirm or dissolve it. Attach your undocumented-instruction log,
because every line in it is a documentation repair the author can make immediately.

Then name the single weakness you would put at the **top of the board**: the one
most likely to move, weaken, or break the claim, and the **one check** that would
confirm or dissolve it. That is what you post to the async discussion board. If you
cannot yet rank a finding because a check is still unrun, that is a finding too, and
it names the run you still owe before Sunday.

Write it the way you would want to receive it. Someone is writing the same document
about a package like yours this week, and the handoff you produce is the standard
you are asking for in return.

### 9. AI Research Ledger rows

Every use of AI in building this report gets a row in your **AI Research Ledger**
(the eight-field table: task delegated · tool used · prompt · output summary ·
decision · verification method · remaining concern · responsible researcher).
Walking through a reproduction cell, rebuilding an environment from a thin record,
building the claim-to-output table, and the required GenAI Studio pass are all
delegable tasks, and each one you delegated needs a row that names how you verified
the result **against your own run**. The pattern this milestone grades hardest: the
AI proposes suspects, your run confirms. "No AI used" is a legitimate entry if it is
true.

Two entries are never legitimate. A reproduction verdict a tool produced, because
no tool ran the code. And a documentation gap an author filled in for you, because
that gap was the finding.

**A missing ledger is not a minor lapse.** Per the course rule, a missing AI
Research Ledger entry scores the Craft criterion **0** and the submission is
**returned** for completion before it is graded.

### 10. The dossier update line and the version line

Open the report with its version line: **Replication and red-team report, version
1**, dated, with a reason a reader could use to reconstruct your thinking. Name
what it is in the book's terms as well: **Book Milestone 11 practice**, run on
another researcher's package. It does not version your own package, which was
frozen at M13 and reissues as version 2 at M16.

Then end with one line recording what this milestone adds to your **Research
Project Dossier**: your replication record now carries an intake and privacy check,
an environment-recreation record, a cold-run log with its independence attestation,
an output comparison including the uncertainty, an undocumented-instruction log, a
red-team of the claims, a verified Reproducibility Auditor pass, and a threat-ranked
repair handoff. Name the file or section where each now lives. That record is the
audit you turn inward at M16, when the package under the microscope is your own.

---

## Definition of Done

You are done when your submission carries all of the following. Use this as a
pre-submission checklist.

| Item | Specification |
|---|---|
| **Intake and privacy check** | Package identifier, date received, and your confirmation that it is identity-stripped and cleared; no attempt to identify or contact the author |
| **Environment record** | What the package pinned, what you had to guess, and whether any guess moved a result |
| **Cold run** | A real restart-and-run-all in a clean session, instructions only, with every break logged to the exact cell and a signed one-line independence attestation |
| **Output comparison** | The point estimate and its uncertainty as *your* run produced them, beside the reported values, plus a claim-to-output trace flagging every gap |
| **Undocumented-instruction log** | Every question you would have had to ask, the guess you made instead, and whether it changed the result |
| **Red-team** | One alternative specification and one hidden assumption, each with the number both ways and a verdict of moves, widens, or breaks |
| **Required AI review** | GenAI Studio **Reproducibility Auditor** pass run and logged; each flag confirmed or dropped by *your* run; the correlated-error trap named |
| **Repair handoff** | Findings ranked by threat to the claim, each with its settling check, with the undocumented-instruction log attached |
| **Exchange** | The async board post (your most-threatening weakness plus the check that settles it) and one substantive reply to a classmate, both part of the grade |
| **Version line** | Replication and red-team report, version 1, dated, with its reason, named as Book Milestone 11 practice on another researcher's package |
| **Style** | Plain language; every finding points at a number you actually produced |
| **AI Research Ledger** | One row per AI-assisted step; every verification method named and non-vague; no reproduction verdict taken from a tool |
| **Dossier line** | Each piece of the replication record located by file or section |
| **Length** | Typically 2–4 pages PDF, or the equivalent notebook sections |
| **Filename** | `lastname_m13_redteam.pdf` (or a shared Colab link) |
| **Location** | Brightspace → Assignments → M16 |

---

## Grading Rubric (100 points)

Four bands on the course's five shared virtues
(`planning/ASSESSMENT_ARCHITECTURE.md`), grounded in the studio's authored
criteria for this checkpoint (`planning/BOOK_ASSESSMENTS.yml`, `package-v1`,
worked here as practice on another researcher's package).

| Criterion | Exemplary | Proficient | Developing | Beginning |
|---|---|---|---|---|
| **Reproduction & red-team correctness** (30) | Intake and privacy check logged; environment recreated from the package's own record; a real cold run with every break traced to its cell; the headline estimate **and its uncertainty** reported as *your* run produced them; claim-to-output trace flags every gap; the undocumented-instruction log is specific; one alternative specification and one hidden assumption each stress-tested with the number both ways; the handoff is ranked by threat rather than ease (26–30) | Reproduction, comparison, and trace correct; one stress test thin, the instruction log sparse, or the ranking slips once toward ease (21–25) | Reproduction present but the uncertainty, the trace, a stress test, or the instruction log is missing; or the handoff is ordered by ease throughout (13–20) | "It ran, so it's fine" — a clean run reported as if it settled the claim; no trace, no stress test, no handoff (0–12) |
| **Evidence integrity** (20) | Every number in the report traces to the package or to your own run; the independence attestation is accurate; any source or claim you name is real and retrievable; a reader can follow each figure back to where it came from (18–20) | Real and traceable; one number lightly sourced (14–17) | A reported figure asserted without a path back to the package or your run (8–13) | A fabricated or unretrievable source; a headline number the package does not produce reported as if it did; or an author-assisted run attested as independent (0–7) |
| **Verification of AI-assisted parts** (20) | The required Reproducibility Auditor pass is run and logged; every AI-assisted step has a ledger row with a named, non-vague verification method; every surviving flag is confirmed by *your* run rather than the tool's trace; the correlated-error trap is named and avoided (18–20) | Auditor pass and ledger present; one method vague or one step unlogged (14–17) | AI outputs used but verification not named; the Auditor's trace accepted without an independent run; or the required pass skipped (8–13) | A reproduction "pass" reported on AI readings with no run behind it, or an AI-drafted finding reproduced with no verification (0–7) |
| **Uncertainty & limitations** (20) | The report states what reproduction does *not* establish (regeneration, not truth); the uncertainty is compared, not only the point estimate; a missing-uncertainty gap is flagged as a finding; residuals and unrun checks are named honestly; no finding is oversold beyond the number supporting it (18–20) | Boundaries and residuals present; uncertainty or an overstatement stated loosely (14–17) | Limits gestured at; the uncertainty comparison skipped, an unrun check hidden, or a modest swing described as damning (8–13) | No boundary: reproduction treated as proof the science is right, or a residual concealed (0–7) |
| **Craft, ledger & communication** (10) | Versioned with its reason, on-format, on-time; board post and one reply completed; complete AI Research Ledger; dossier line present; the handoff is written to be used (9–10) | Minor format lapses; ledger complete (7–8) | Missing pieces, no board reply, a decorative version reason, or a rushed report (4–6) | Missing AI Research Ledger (Craft scored 0, submission returned) (0–3) |

**Hard caps (a single failure caps the row regardless of the rest):**

- A **fabricated or unretrievable source** caps *Evidence integrity* at Beginning.
- An **untraceable number** — a figure in your report with no path back to the
  package or to your own run — caps *Verification of AI-assisted parts* at
  Beginning.
- A **non-reproducing result you report as reproduced** — claiming a clean
  reproduction the package cannot actually deliver — caps *Verification of
  AI-assisted parts* at Beginning. An honest "it did not reproduce, and here is
  what broke" never triggers this; the cap is for the false pass, not the failure.
- An **author-assisted run attested as independent** caps *Evidence integrity* at
  Beginning. Reporting the assistance honestly never triggers this cap.
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
- Contacting the author, attempting to identify them, or reporting an assisted run
  as independent: *Evidence integrity* scores Beginning regardless of the rest.
- Pasting uncleared package contents into any AI tool: the permission rail is
  broken, and the submission is returned pending a conversation with me.
- Skipping the required Reproducibility Auditor pass: *Verification of AI-assisted
  parts* scores Developing at best.
- Any source you cite that turns out not to exist or not to say what you claim:
  *Evidence integrity* scores Beginning regardless of the rest.
- Missing AI Research Ledger entry: *Craft* scores 0 and the submission is returned
  for completion before grading.

## Common Pitfalls

1. **"It ran, so it's fine."** The definitional failure of M16. A clean
   restart-and-run-all proves the code executes; it says nothing about whether the
   write-up's sentence matches the output, whether a different choice moves the
   number, or whether a buried assumption is false. Reproduction earns you a
   number; the red-team is the grade.
2. **The assisted run called independent.** One clarifying message to the author,
   and the thing you tested is no longer the package. Every question you wanted to
   ask is a documentation gap, which is exactly the finding the author needs from
   you. Log the question; do not send it.
3. **The half-reproduction.** Matching the point estimate and stopping there. The
   same estimate with a much wider interval is a different result, and a package
   that reports no uncertainty has a reporting gap you are the first person
   positioned to catch. Reproduce the uncertainty, not only the number.
4. **Trusting the tool's trace instead of your run.** The GenAI Studio Auditor and
   your AI both read; neither runs code. If both call the package sound, that is the
   correlated-error trap, not confirmation — one flaw echoed twice. Confirm every
   flag that survives against a number *you* produced, and log the run that decided
   it.
5. **Ranking by ease instead of threat.** Leading with the quick typo fix and
   burying the clustering assumption that could dissolve the claim. The author can
   decide the repair order; your job is to say where the claim is in the most
   danger. Rank by threat to the headline, every time.

---

*Previous: [M15 — Conference Reflection and Defense Revision](milestone_12_conference_reflection.md) ·
Next: [M16 — Research Note v1 and Reusable Package](milestone_14_research_note_capsule.md) —
the cold audit you just ran on a classmate turns inward: your own package is
repaired against the handoff you receive, and every claim in your note has to
survive the exact trace you used here.*
