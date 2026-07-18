# Reproducibility Audit Protocol — M39–M40 (Nov 30 & Dec 2)

*Assemble a package a stranger can rebuild your findings from, then have a
classmate actually do it and sign. Governs
[milestone_20 — Reproducibility Audit](../../_research_project/2026Fall/milestone_20_reproducibility_audit.md).
Round 1 in class M39; sign-off in class M40; M20 due Dec 2. Reading: RDSS ch. 21–22.*

## Purpose

"It works on my machine" is not reproducibility — it is an untested claim. If you
vanished today, could a competent stranger reproduce every number in your
dossier? This audit answers that empirically: you build the package, a partner
attempts your headline number cold, and on the second round they sign an
attestation (or log the residuals honestly). Verification is the graded habit,
not a formality.

## Materials

- Your project notebook, and everything needed to run it.
- The reproducibility-package checklist (nb18 §1–2).
- A partner (rotated from your red-team pairings).
- The attestation form (below).

## Package anatomy (assemble all five)

1. **Runnable notebook** — passes **restart-and-run-all** from a clean kernel,
   top to bottom, no manual intervention.
2. **Data provenance statement** — where each dataset came from, its version/date,
   and how it may be used (license, attribution — e.g., the lapop_brazil 10k
   resample caveat if you used it).
3. **Seed + environment note** — every random step seeded; the key package
   versions recorded so results don't drift.
4. **Decision log** — the choices behind the numbers: which sources, which
   operationalization, which exclusions, and why (decisions, not just outcomes).
5. **AI-use ledger** — finalized: every tool, its task, and how you verified its
   output (Ask → Verify → Document).

## The five package sins (find and kill them before the exchange)

| Sin | What it looks like | Fix |
|---|---|---|
| **Hard-coded path** | `/Users/me/Desktop/data.csv` | relative path or documented source URL |
| **Missing seed** | a random draw that differs every run | seed every stochastic step |
| **By-hand edit** | a number "corrected" in the cell, not the code | do it in code, or log it in the decision log |
| **Undocumented exclusion** | rows dropped with no reason recorded | state the rule and its rationale |
| **Stale data** | the notebook reads an old file the numbers no longer match | re-point to the current data; note the version |

## The two-round partner exchange

**Round 1 — cold reproduction (M39).**
1. Swap packages. Your partner opens yours with no coaching.
2. They attempt to reproduce your **headline number** from the package alone.
3. **You watch silently** — do not rescue them. Their confusion IS the audit.
4. Log every break: what failed, at which step, and why.

**Round 2 — re-run and sign (M40).**
1. You fix everything the breakage log exposed.
2. Your partner re-runs the fixed package.
3. If the headline number reproduces, they **sign the attestation**.
4. If it doesn't fully reproduce, they **log the residuals** (what still differs,
   and the suspected cause) — an honest residual log is graded on its honesty,
   not penalized for a non-clean pass.

## The attestation form (inline — complete at M40)

```
REPRODUCTION ATTESTATION — M20

Author: __________________     Reproducer: __________________
Headline number claimed: _______________________________
Value I obtained from the package alone: _______________________________

[ ] REPRODUCED — the value matches within stated tolerance.
[ ] REPRODUCED WITH RESIDUALS — differences below, with suspected cause:
      _____________________________________________________________
      _____________________________________________________________

Package completeness (check each):
  [ ] restart-and-run-all passed   [ ] data provenance present
  [ ] seed + environment noted     [ ] decision log present
  [ ] AI-use ledger finalized

Reproducer signature: __________________   Date: __________________
```

## Procedure

**M39 (Mon Nov 30, 50 min)**

| Time | Activity |
|---|---|
| 0–5 | December map: three weeks, three artifacts (package, brief, defense). |
| 5–12 | Mini-lesson: the checklist on a real example; where projects break (paths, seeds, by-hand steps). |
| 12–30 | **Package studio:** restart-and-run-all, fix breaks, write provenance + decision-log stubs. |
| 30–44 | **Exchange round 1:** partner reproduces your headline number cold; you watch silently. |
| 44–48 | Log what broke. |
| 48–50 | Exit ticket (first thing that broke + your fix). |

**M40 (Wed Dec 2, first \~17 min)**

| Time | Activity |
|---|---|
| 0–5 | Breakage-fix reports (one line each). |
| 5–17 | **Exchange round 2:** partner re-runs the fixed package and **signs** the attestation (or logs residuals). M20 completes. |

Then the research brief begins — see
[research_brief_template.md](research_brief_template.md).

## Roles

- **Author:** assemble the package, kill the five sins, watch silently in round 1, fix, then present the fixed package for signing.
- **Reproducer:** run it cold, log every break specifically, and sign only what actually reproduced.

### Session flow (for the record)

Professor Moreira builds a sample "sinful" package for the mini-lesson, sets the
pairing plan (rotated from red-team), and distributes checklists and sign-off
forms. Each person reproduces one package and has one reproduced.

## Common failure modes

1. **Rescuing your reproducer.** Coaching hides the break you needed to find. Stay silent in round 1.
2. **A clean pass claimed but never exercised.** If no stranger ran it, it isn't reproducible — the exchange is the proof.
3. **Signing a non-reproduction.** If it didn't reproduce, log residuals honestly; a false signature is an integrity failure.
4. **Fixing the symptom, not the cause.** Patching one number by hand re-commits the by-hand-edit sin. Fix it in code.
5. **Leaving the AI ledger for later.** It is part of the package; finalize it now, not at the dossier deadline.

*Governs the dossier's reproducibility package. Next: [research_brief_template.md](research_brief_template.md) · then [evidence_defense_protocol.md](evidence_defense_protocol.md).*
