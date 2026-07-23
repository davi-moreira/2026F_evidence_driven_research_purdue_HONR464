# Milestone 14 — Research-Note Draft and Reproducibility Capsule

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

This milestone is the **Research note** component. It is where your claim ledger
is graded a second time (after M9, before M15), because a note is where a claim
either stays sized to its evidence or quietly grows past it. It is
**revision-eligible** under the standing policy.

---

## What to Submit on Brightspace

Due: **Friday, December 4, 11:59 PM** (you table-read your draft at the Friday
studio that day, leaving and receiving margin notes).

| # | File | Description |
|---|---|---|
| 1 | **`lastname_m14_research_note.pdf`** *or* a shared Colab notebook link | Your research-note draft: the problem–gap–question spine in prose, your results hierarchy with the headline finding at its real boundary, your limitations sized to the evidence, and your AI-edit log. This is the graded prose artifact. |
| 2 | **`lastname_m14_capsule.ipynb`** *or* a shared Colab notebook link | Your reproducibility capsule: a notebook that passes restart-and-run-all, its data-provenance note, a fixed seed, a decision log, and your finalized AI-use ledger — audited against the five package sins. |
| 3 | **The table-read margin notes + your revision** | The two margin notes each reader left on your draft (sharpest sentence, weakest claim) and the revision you made in response. |

If you submit a notebook link, set sharing so the instructor can open it, and
make sure the capsule runs top to bottom when opened cold. Attach your **AI
Research Ledger** rows inside the note. The capsule is your reproducibility
proof: if a stranger cannot rerun it, it is not yet a capsule.

---

## Purpose

Your poster made its argument to a reader you could coach in real time. A
**research note** makes the same argument to a stranger who has only the page,
and a **reproducibility capsule** lets that stranger rebuild your number without
you in the room. This milestone turns your finished study into both.

The move from poster to note is not "add more words." A poster is allowed to
**imply** its reasoning; a note has to **argue** it, in order, so a reader reaches
your conclusion by the same steps you did. Every claim has to be earned in prose,
every source has to be real and retrievable, and every sentence has to stay sized
to the evidence beneath it. The failure this milestone exists to catch is the
quiet one: a disciplined, caveated finding sliding back into a clean, confident,
caveat-free sentence because the clean version reads better. A sharper sentence
is not a bigger finding. If a sentence outgrows its evidence, the evidence has to
grow first, or the caveat stays on the page.

The capsule tests the other half of trust. A note a reader believes and cannot
rerun is still half a claim. Restart-and-run-all proves your notebook executes;
it does not prove the number is right, which is why your capsule is exercised by
a **partner** at the studio, not just by you. Together the note makes your work
**readable** and the capsule makes it **runnable**, and only you, holding the pen,
keep both sized to your evidence.

> **A question that often comes up here:** *"My poster already made the point.
> Why rewrite it as prose at all?"* Because the poster made it to a reader you
> could coach in real time, and the note makes it to a reader who only has the
> page. Everything your voice used to supply — the tone that said *this gap
> matters*, the gesture that linked two boxes — is gone. Prose is where you put
> it back. The note is not longer for its own sake. It is longer because it has
> to do the work your presence was doing.

## Components

### 1. The problem–gap–question spine, in prose

Build your note's backbone as three linked, argued paragraphs, not five boxes.

- **Problem** — the real-world or scholarly trouble your work responds to.
- **Gap** — the specific thing prior, retrievable work has not yet established.
  Your gap paragraph must do three things a poster box could leave implied: name
  what prior work **did** cover, name what it **left out**, and say **why** the
  missing piece matters.
- **Question** — the answerable question that closes exactly that gap.

The spine holds only if the gap is real, and a gap is real only when you show
what is already known. That is **literature synthesis**: a few real, retrievable
sources woven into an argument about what is settled and what is missing, never a
name-drop. Measure your own paragraph by its **evidence density** — the share of
its sentences that rest on a source a reader could retrieve, versus bare
assertion. A paragraph of confident claims with nothing to retrieve is not a
synthesis; it is *"as everyone knows"* in a lab coat, and this milestone catches
it.

> **A question that often comes up here:** *"My gap is genuinely under-studied —
> only two or three sources sit near it. Doesn't a thin literature look weak?"*
> Padding it with ten loosely related citations looks deep and reads as evasion.
> Synthesize the two or three genuinely adjacent sources, each retrieved and
> confirmed, and state plainly that the gap is thinly studied. Honesty about a
> thin literature is a strength a reviewer trusts; a decorative citation doing no
> real work is a weakness they catch.

### 2. The results hierarchy, with uncertainty attached

Order your findings by how much evidence backs each one, strongest and
best-supported first, exploratory and fragile last. This is your **results
hierarchy**. Present your **headline finding** at the top, at its real boundary,
with its uncertainty in the same breath — for a numeric finding, its interval
(for example, a **95% bootstrap interval**, the range you get when you resample
your own data many times). Any exploratory finding — one from a small slice, a
wide interval, an unusual subgroup — is clearly labeled and placed last, never
leading.

The ranking tracks evidence, not surprise. Your most surprising result is often
your least supported one. Name and forbid the **inflated contribution**: the
tempting sentence written to sound like a bigger finding than the evidence
supports (leading with a fragile forty-person result because it is the most
surprising thing you found). Write the honest headline your evidence licenses,
and write the inflated version beside it so you can refuse it on sight.

### 3. Limitations sized to the evidence

State your two or three limitations **in proportion to what actually threatens
your claim**, neither hidden nor performed. A generic *"more research is needed"*
is not a limitation. Name the specific caveat that most bends your headline — the
resample caveat, the coverage gap, the interval width — and, for a numeric claim,
say which limitation would most **widen** that interval if a reviewer pushed on
it. Your single most important limitation should be one a reader could not have
guessed without you naming it.

### 4. The AI-edit log

You may use an AI tool as a **writing critic**, not a ghostwriter (the course
role is the **Research Note Reviewer**; see Components below). Keep a short record
of which AI edits you **kept, changed, or rejected**, and why for each. The rule
that governs the log: **a cleaner sentence is not a bigger finding.** Keep only
edits that sharpen the prose while leaving the claim exactly its size; reject
every edit that quietly upgrades a claim — *related* becoming *drives*, *in this
sample* silently dropped. Which claim leads, how big it is allowed to be, which
sources are real, and the words you put your name on are never delegable.

> **A question that often comes up here:** *"If the tool writes cleaner prose than
> I do, why not let it draft the note?"* Because a note is an argument you are
> responsible for, and clean prose is exactly how an overclaim sneaks in. If the
> tool writes the sentence, you cannot tell whether it stayed inside your
> evidence, and you will defend it as if you can. Write first, then let the tool
> attack what you wrote. That keeps you the author and the tool the critic.

### 5. The reproducibility capsule

Assemble everything a stranger needs to rebuild your numbers, and nothing they
would have to guess. Five parts:

- A **runnable notebook** that passes **restart-and-run-all** — clear the kernel,
  run every cell top to bottom, no manual fixes, and your headline number comes
  back.
- A **data-provenance note**: where each dataset came from, its version, and how
  it may be used.
- A **fixed seed** (`SEED = 464`), so every random step returns the same numbers.
- A **decision log** of the by-hand choices that shaped the result — every
  exclusion, recode, and cut point — each with its reason.
- Your finalized **AI-use ledger**: every tool, its task, and how you verified it.

Then audit your own capsule against the **five package sins**: a **hard-coded
path** that exists only on your laptop, a **missing seed** that moves every run, a
**by-hand edit** no clean run reproduces, an **undocumented exclusion** with no
logged reason, and **stale or unversioned data** a reader cannot reobtain. Report
the one sin you found and fixed in your own notebook.

> **A question that often comes up here:** *"The capsule passed with zero flags.
> Isn't it done?"* A zero-flag capsule is **runnable**, not **correct**. The
> auditor cannot see that your seed is fixed on the wrong sample, that a logged
> reason is a bad reason, or that your analysis answers a different question than
> the one you declared. Those are the failures a partner finds when they run your
> work cold, which is why the capsule is exercised by a person at the studio, not
> just by a script.

### 6. Claim-to-evidence traceability

Every sentence in the note traces to a row in your **claim ledger** (from M9):
claim · evidence · verification · boundary · sensitivity survival. Nothing on the
page exceeds what the ledger licenses. When you compress three caveated sentences
into one, the caveat rides along. This is where the milestone's second graded
pass on your claim ledger lives.

### 7. AI Research Ledger rows

Every use of AI in building this note and capsule gets a row in your **AI Research
Ledger** (the eight-field table: task delegated · tool used · prompt · output
summary · decision · verification method · remaining concern · responsible
researcher). Red-teaming a discussion paragraph, ranking limitations, and auditing
the capsule are all delegable tasks, and each one you delegated needs a row that
names how you verified the result. "No AI used" is a legitimate entry if it is
true.

**A missing ledger is not a minor lapse.** Per the course rule, a missing AI
Research Ledger entry scores the Craft criterion **0** and the submission is
**returned** for completion before it is graded.

### 8. Dossier update line

End with one line recording what this milestone finalizes in your **Research
Project Dossier**: your research record now carries a research-note draft with an
argued spine, a results hierarchy, evidence-sized limitations, and a runnable
reproducibility capsule. Name the file or section where each now lives.

---

## Submission Expectations

| Item | Specification |
|---|---|
| **Length** | The research note (typically 4–6 pages PDF, or the equivalent notebook sections) plus the capsule notebook |
| **Capsule** | A real restart-and-run-all; the headline number reruns from the seeded notebook; provenance note, decision log, and AI-use ledger included; the one sin you found and fixed named |
| **Table read** | At the Friday studio (Dec 4), a partner table-reads your note and reruns your capsule; you leave and receive margin notes — part of the grade |
| **Style** | Plain language; every technical term used as defined; each claim carries its uncertainty; every source real and retrievable |
| **Filename** | `lastname_m14_research_note.pdf` and `lastname_m14_capsule.ipynb` (or shared Colab links) |
| **Location** | Brightspace → Assignments → M14 |

---

## Grading Rubric (100 points)

Four bands on the course's five shared virtues (`planning/ASSESSMENT_ARCHITECTURE.md`).

| Criterion | Exemplary | Proficient | Developing | Beginning |
|---|---|---|---|---|
| **Compass / pathway alignment** (20) | The note argues the problem–gap–question spine in order; the headline claim states its compass position and stays inside its boundary; the results hierarchy leads with the best-supported finding and labels the exploratory one last (18–20) | Spine and hierarchy correct; one arrow under-argued or the compass position stated loosely (14–17) | Spine present but a link collapsed, or a fragile finding leads, or the boundary never stated (8–13) | The note reads as a shrunk poster, or an exploratory finding leads as the headline, or the claim ignores its compass position (0–7) |
| **Evidence integrity** (20) | Every source in the synthesis is real and retrievable; the gap paragraph names prior coverage, the omission, and why it matters; the reader can trace each claim to its origin (18–20) | Real and traceable; one provenance link thin or one synthesis citation lightly sourced (14–17) | A claimed source asserted without a locatable origin, or a synthesis resting on bare assertion (8–13) | A cited source that does not exist or does not say what you claim, or an *"as everyone knows"* synthesis with nothing to retrieve (0–7) |
| **Verification** (25) | The headline number reruns from the seeded capsule via restart-and-run-all; the capsule carries provenance, decision log, and fixed seed; every AI-assisted step has a ledger row with a named, non-vague verification method; the one package sin found and fixed is reported (22–25) | Capsule reproduces; one part thin (a loose decision log) or one ledger verification vague (18–21) | Capsule present but does not cleanly restart-and-run-all, or AI outputs used with verification unnamed (11–17) | The headline number does not rerun from the capsule, or an AI-edited claim reproduced with no verification (0–10) |
| **Uncertainty & limitations** (20) | The headline carries its uncertainty in the same breath; limitations are sized to what threatens the claim; the honest sentence and the forbidden inflated contribution are both written out precisely (18–20) | Uncertainty and limitations present; one stated loosely or the forbidden version left implicit (14–17) | The headline reported without its interval, or limitations generic (*"more research is needed"*), or only the honest sentence with no inflated version named (8–13) | No uncertainty on the headline, or a caveated finding silently upgraded to a bigger or cleaner claim (0–7) |
| **Craft & AI Research Ledger** (15) | On-format, on-time, clear table-read participation, complete AI-edit log and AI Research Ledger, margin notes incorporated, dossier line present (14–15) | Minor format lapses; ledger complete; light revision from the table read (11–13) | Missing pieces, a rushed table read, or margin notes ignored (6–10) | Missing AI Research Ledger (Craft scored 0, submission returned) (0–5) |

**Hard caps (a single failure caps the row regardless of the rest):**

- A **fabricated or unretrievable source** caps *Evidence integrity* at Beginning.
- An **untraceable number** — a figure with no path back to your data — caps
  *Verification* at Beginning.
- A **non-reproducing result** — the headline number does not rerun from your
  seeded capsule — caps *Verification* at Beginning.
- A **missing AI Research Ledger entry** scores *Craft & AI Research Ledger* **0**
  and the submission is **returned** unread until it is supplied.

**Revision:** eligible under the standing policy — a revised submission within **7
days** of feedback recovers up to half the lost points.

## Penalties

- Late: −10 points per day, up to 3 days; not accepted after (documented
  emergencies: talk to me first, per the syllabus).
- Any source you cite that turns out not to exist or not to say what you claim:
  *Evidence integrity* scores Beginning regardless of the rest — the course's
  evidence-integrity rule with teeth.
- A headline number that does not rerun from your seeded capsule: *Verification*
  scores Beginning regardless of the rest. An honest "this part did not reproduce,
  and here is what broke" never triggers this; the cap is for the false pass.
- Missing AI Research Ledger entry: *Craft* scores 0 and the submission is
  returned for completion before grading.

## Common Pitfalls

1. **The caveat that fell off under polish.** The single most common failure: a
   disciplined, caveated finding reappears clean and confident because the clean
   version scans better, or an AI edit quietly turned *related* into *drives*. A
   sharper sentence is not a bigger finding. Put the caveat back, and keep only
   edits that leave the claim its size.
2. **"It runs for me" offered as reproducibility.** A capsule that runs on your
   laptop, in the click-order you remember, and was never rerun cold by anyone
   else. Restart-and-run-all is the floor, not the proof; a zero-flag capsule is
   runnable, not correct. Hand it to a partner before you hand it to me.
3. **The synthesis that cites nothing retrievable.** *"As everyone knows…"* or ten
   decorative citations standing in for an argument about what prior work settled
   and left open. A paragraph a reader cannot retrieve anything from is an opinion,
   not a synthesis. Cite the two or three real sources and be honest that the gap
   is thin.

---

*Previous: [M13 — Replication and Red-Team Report](milestone_13_replication_redteam.md) ·
Next: [M15 — Final Research Chapter and AI-Management Portfolio](milestone_15_final_chapter_portfolio.md) —
the note you just wrote and the capsule you just sealed expand into your final
chapter, and your full-semester AI Research Ledger becomes the portfolio you
defend.*
