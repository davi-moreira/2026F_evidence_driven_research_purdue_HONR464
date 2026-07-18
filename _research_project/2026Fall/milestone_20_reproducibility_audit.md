# Milestone 20 — Reproducibility Audit

## About the Research Project

Your semester project is **individual**: one researcher, one question, carried
from curiosity to a defended, reproducible claim. It runs through milestones
M00–M23, peaks publicly at the **Purdue Fall Undergraduate Research Expo
poster session (Tuesday, November 17 — required)**, and closes with an oral
**Evidence Defense** and a final research dossier in December. Every milestone
follows the same cadence: **develop in class → present → submit → revise**.
Milestone weights and the revision policy are in the syllabus; instructions
and rubrics live one page per milestone, like this one.

This milestone is part of the **post-conference research dossier** component and
is worth **5% of the course grade** (the dossier splits into M19 5%, M20 5%,
M21 4%, and the M23 final dossier 6%). It is **revision-eligible** under the
standing policy, with residuals logged.

---

## What to Submit on Brightspace

Due: **Wednesday, December 2, 11:59 PM** (developed across M39 Mon Nov 30 and
M40 Wed Dec 2 — package studio plus two partner exchange rounds).

| # | File | Description |
|---|---|---|
| 1 | **`lastname_m20_repro.pdf`** | Your partner-exchange record and the signed reproduction attestation (or residuals log), plus your AI-use disclosure block. |
| 2 | **The reproducibility package** | The runnable notebook + data provenance statement + seed/environment note + decision log + finalized AI-use ledger (a folder or zip). |

---

## Purpose

"It works on my machine" is not reproducibility — it is a rumor. This milestone
tests the real thing: could a **competent stranger rebuild your headline number
from what you hand them, alone**? You assemble a **reproducibility package** and
then a classmate actually tries to reproduce your central result from it, cold,
while you watch and say nothing. What breaks in that exchange is the audit's most
valuable output — the hard-coded path, the missing seed, the by-hand edit you
forgot you made. You fix it, they re-run, and if it reproduces they **sign**.
The signature is the point: reproducibility is a claim, and like every claim in
this course it must be **exercised by another human**, not asserted. If it
doesn't fully reproduce, you log the **residuals honestly** — and the rubric
weighs the honesty of that log as heavily as a clean pass, because a documented
failure is science and a hidden one is not.

## Components

### 1. The reproducibility package

Everything a stranger needs, and nothing they'd have to guess:

- **Runnable notebook** — passes **restart-and-run-all clean**: no manual steps,
  no cells run out of order, no leftover state. Top to bottom, one click.
- **Data provenance statement** — where each dataset came from, its version/date,
  and any access conditions. A reader must be able to obtain the same inputs.
- **Seed + environment note** — the random seed(s) fixed in-code, and the
  environment (Colab / package versions) recorded so results are stable.
- **Decision log** — the by-hand choices that shaped the result (exclusions,
  recodes, cut points, filters), each with its reason.
- **Finalized AI-use ledger** — the full-project record of which AI tool did
  which task and how each output was verified, closed out for the dossier.

### 2. The partner exchange record

Document both rounds:

- **Round 1 (M39)** — your partner attempts your headline number from the
  package alone while you watch silently. Log **what broke** and in what order.
- **The fixes** — what you changed in response to each breakage.

### 3. The signed reproduction attestation (or residuals log)

From **Round 2 (M40)**, one of two honest outcomes:

- **A signed attestation** — your partner re-runs the fixed package and it
  reproduces. Record it in their words, dated and specific.
- **A residuals log** — if some part still doesn't reproduce, log exactly what,
  why (as far as you can tell), and what a fix would require. This is not a
  failing outcome; concealing it would be.

**Honest sign-off (concrete example):** *"Priya Nair reproduced my headline
number — the 18-point office-hours gap — from my package alone on Dec 2, 2026.
Restart-and-run-all returned 61% and 43% exactly. One residual: Figure 2 needed a
seed she found in my decision log but not in the cell; now fixed in cell 12."*

**Cosmetic sign-off (non-example):** *"Reproduced ✓"* — no name, no date, no
number, no residuals. A rubber stamp attests nothing; the rubric reads it as an
exchange that never really happened.

### 4. AI-use disclosure block (required on every deliverable)

A short table: which AI tool(s) you used, for what task (locate / draft /
critique / none), and how you verified the output. "No AI used" is a fine
entry; an undisclosed AI contribution is an academic-integrity violation. (For
this milestone, the finalized AI-use ledger in the package satisfies this at
full project scope; the PDF still carries the short block.)

---

## Submission Expectations

| Item | Specification |
|---|---|
| **Package** | Notebook passes restart-and-run-all; provenance, seed/environment, decision log, AI ledger all present |
| **PDF** | Exchange record (round 1 breakage + fixes) + round-2 attestation or residuals log, plus the disclosure block |
| **Exchange** | Both rounds performed in class (M39, M40) — participation is part of the grade |
| **Style** | The attestation is specific and dated; the residuals log (if any) names causes, not just symptoms |
| **Filenames** | `lastname_m20_repro.pdf` + the package (folder or zip) |
| **Location** | Brightspace → Assignments → M20 |

---

## Grading Rubric (100 points)

| Criterion | Exemplary | Proficient | Developing | Beginning |
|---|---|---|---|---|
| **Package completeness & clean run** (25) | Restart-and-run-all clean, top to bottom, no manual steps (22–25) | Runs with one minor documented manual step (18–21) | Runs only after undocumented fiddling (11–17) | Does not run for a stranger (0–10) |
| **Provenance, seed & environment** (15) | Data sources, versions, seeds, and environment fully recorded and sufficient to obtain identical inputs (13–15) | Mostly recorded; one gap (10–12) | Provenance vague or seed/environment missing (6–9) | No provenance or reproducibility metadata (0–5) |
| **Decision log & AI-use ledger** (15) | Every result-shaping choice logged with a reason; AI ledger finalized and verification-complete (13–15) | Log present; a few choices unexplained (10–12) | Sparse log or unfinalized AI ledger (6–9) | Neither log nor ledger (0–5) |
| **Partner exchange record** (15) | Round-1 breakages logged in order with the exact fixes (13–15) | Exchange recorded; fixes lightly described (10–12) | Vague account of the exchange (6–9) | No exchange record (0–5) |
| **Attestation / honesty of residuals** (20) | Specific, dated, named sign-off — or a residuals log so honest it is itself audit evidence (18–20) | Sign-off present; slightly thin on specifics (14–17) | Generic "reproduced" with no detail (8–13) | Missing, or a clean-pass claim contradicted by the package (0–7) |
| **Craft & communication** (10) | On-format, on-time, complete disclosure block (9–10) | Minor lapses (7–8) | Disorganized package or missing pieces (4–6) | Missing disclosure block (0–3) |

**Revision:** eligible under the standing policy — a revised package + PDF within
7 days of feedback recovers up to half the lost points; a re-exchange may be
arranged for a genuine reproduction failure.

## Penalties

- Late: −10 points per day, up to 3 days; not accepted after (documented
  emergencies: talk to me first, per the syllabus).
- Claiming a clean reproduction the package cannot actually deliver is an
  evidence-integrity violation: the Attestation criterion scores Beginning
  (0–7) regardless of the rest. An honest residuals log never triggers this — the
  penalty is for the false pass, not the failure.
- Missing AI-disclosure block: Craft scores 0 and the submission is returned
  for completion before grading.

## Common Pitfalls

1. **"Works on my machine."** The definitional failure. Until a stranger runs
   it from your package alone, you have a rumor, not reproducibility.
2. **The invisible by-hand step.** The edit you made once and forgot is exactly
   what breaks in Round 1. The decision log exists to catch it.
3. **Hidden state.** A notebook that only works if cells run in the order you
   happened to click fails restart-and-run-all. Test it before the exchange.
4. **The rubber-stamp sign-off.** "Reproduced ✓" with no number or date attests
   nothing and scores as if the exchange never happened.
5. **Faking the pass.** A residual you hide costs more than one you log — the
   rubric rewards the honest residuals log and punishes the false clean pass.

---

*Previous: [M19 — Poster-to-Dossier Module](milestone_19_poster_to_dossier.md) ·
Next: [M21 — Research Brief](milestone_21_research_brief.md) — the verified
package becomes one page a decision-maker can act on.*
