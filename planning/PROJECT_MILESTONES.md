# PROJECT_MILESTONES — the M00–M23 system (planning source of truth)

Five students, five **individual** projects, one semester-long chain: every
milestone is a graded, submittable artifact with **develop → present → submit →
revise** cadence. Student-facing instructions + rubrics live one file per
milestone in `_research_project/2026Fall/` (Brightspace replicates from there).
Dates below are pinned to the verified calendar (`CALENDAR_BACKBONE.csv`);
per-meeting development detail is in `MEETING_SCHEDULE.csv` (milestone columns).
Presentation formats per milestone: `MILESTONE_PRESENTATION_MAP.md`.

**Kickoff cadence (studio-Friday rhythm).** Every milestone is kicked off from its
Brightspace brief in the 10–20 min slot of a Friday studio, developed across
Mon/Wed lectures (short transfer moments) and studio work blocks, and in most
cases presented and due at a Friday studio. Kickoff exceptions: M00 (assigned in
class on day 1, M1), M06 (brief posted with the async M17 module), M11 and M12
(rolling kickoffs inside the poster sprint, M29/M30), M18 (kicked off Wed M36
immediately after the conference debrief), M21 (kicked off Wed M40 with the brief
template). M07's abstract thread starts at studio M14 and the async M17 module;
its declaration assembly is kicked off at studio M20.

## The chain at a glance

| ID | Milestone | Developed (meetings) | Presented | Due (11:59 PM) | Feeds |
|---|---|---|---|---|---|
| M00 | Kickoff: Curiosity Map + tool readiness | M1–M2 | M3 studio (30-sec curiosity pitch) | Fri Aug 28 | M01 |
| M01 | Research Question Pitch (gap → problem → question + candidate approach) | M4–M6 | M6 studio (2-min pitch + compass vote) | Fri Sep 4 | M02, M03 |
| M02 | Literature & Claim Map (verified sources, citation integrity) | M7–M8 | M8 studio (gallery walk) | Fri Sep 11 | M03 |
| M03 | Model & Inquiry Declaration (DAG + estimand) | M9–M11 | M11 studio (3-min declaration) | Fri Sep 18 | M07 |
| M04 | Measurement & Operationalization Plan | M12–M14 | M14 studio (walkthrough + two-line reviews) | Fri Sep 25 | M05, M07 |
| M05 | Data Strategy + Feasibility & Ethics Checkpoint | M15–M17 | M17 async board (90-sec recorded statement) | Fri Oct 2 | M07 |
| M06 | Answer Strategy Declaration | M18–M21 | M20 studio clinic (during the work block) | Wed Oct 14 | M07 |
| M07 | URC Abstract **(gate Fri Oct 9)** + Full Design Declaration | M18–M22 | M20 studio (abstract workshop), M22 studio (assembly consults) | abstract **Fri Oct 9**; declaration **Fri Oct 16** | M08–M12 |
| M08 | Design Diagnosis & Redesign Memo | M23–M25 | M25 studio (60-sec redesign pitch) | Fri Oct 23 | M09 |
| M09 | Pilot Analysis — **branches by approach** | M26–M28 | M28 studio (4-min walkthrough) | Fri Oct 30 | M10–M12, M19 |
| M10 | Poster Storyboard | M29 | M29 (Mon, in class; 90-sec storyboard pitch) | Mon Nov 2 | M11 |
| M11 | Poster Draft + Red-Team Review | M30 | M30 (Wed, in class; structured red-team) | Wed Nov 4 | M12 |
| M12 | Final Poster | M31 (production studio) | M31 studio (final-checklist consults) | **Fri Nov 6** | M13–M16 |
| M13 | Presentation Plan (1-min + 3-min scripts + walk map) | M32–M33 | M32 (Mon, in class; partner delivery rounds) | Wed Nov 11 | M15, M16 |
| M14 | Uncertainty & Limitations Statement + Question Bank | M33–M34 | M34 studio (hot seat) | Fri Nov 13 | M15, M16 |
| M15 | Dress Rehearsal + Readiness Audit | M35 | M35 (Mon, in class; full simulation) | Mon Nov 16 (in class) | M16 |
| M16 | **URC Expo Presentation** (required) | M32–M35 | **Tue Nov 17, URC Expo** | event attendance + presentation | M17–M19 |
| M17 | Conference Reflection (coded audience data) | M36 | M36 (Wed, in class; story round + pair analysis) | Wed Nov 18 | M18 |
| M18 | Feedback-to-Redesign Plan | M36–M37 | M37 studio (2-min redesign declaration) | Fri Nov 20 | M19–M23 |
| M19 | Poster-to-Dossier Module (sensitivity + claim ledger) | M38 (async) | async board (fragile-row post + reply) | Mon Nov 30 | M20–M23 |
| M20 | Reproducibility Audit (partner-verified) | M39–M40 | M39/M40 (Mon/Wed reproduction exchange + sign-off) | Wed Dec 2 | M23 |
| M21 | Research Brief (one page) | M40–M41 | M41 studio (table read) | Fri Dec 4 | M22, M23 |
| M22 | Evidence Defense (10-min defense + 5-min cross-examination) | M41–M43 | **M42 (Dec 7) / M43 (Dec 9)** | performed in class | M23 |
| M23 | Final Research Dossier + Claim Ledger | M43–M44 | M44 studio (submission ceremony) | **Fri Dec 11** | — |

## Design invariants (quality gates — checked by `scripts/validate_milestones.py`)

1. **Every milestone has ≥1 prior in-class development meeting** before its due
   date (M16 is the event itself; its development spans meetings M32–M35,
   carried by the M13–M15 chain).
2. **Every milestone is kicked off at a Friday studio** from its Brightspace
   brief (10–20 min slot), with the exceptions listed in the kickoff-cadence
   note above (M00, M06, M11, M12, M18, M21).
3. **Every milestone has a presentation/review activity**, normally inside the
   Friday-studio work block. Honest asterisk — hard dates force some onto
   Mon/Wed: M10 (Mon M29), M11 (Wed M30), M13 (Mon M32), M15 (Mon M35),
   M17 (Wed M36), and M20 (Mon/Wed M39–M40) present in class on lecture days,
   and M06 presents in the studio M20 clinic but keeps its Wed Oct 14 due date.
   M16 (Tue Nov 17 Expo) and M22 (Dec 7/9 defenses) are scheduled performance
   events. Formats vary — see `MILESTONE_PRESENTATION_MAP.md`; with 5 students,
   every student presents every time.
4. **Submission dates never precede development**, and no two written milestones
   are due on the same day.
5. **Poster work is NOT delayed to November:** the poster's inputs (abstract
   Oct 9, declaration Oct 16, diagnosis Oct 23, pilot Oct 30) are all October
   artifacts; November's M10–M12 is assembly and polish, by design.
6. **Post-conference work is substantive:** M17–M23 comprise sensitivity
   analysis, a partner-verified reproducibility audit, a research brief, an oral
   Evidence Defense, and the final dossier — ~35% of the course's graded weight
   (see `ASSESSMENT_ARCHITECTURE.md`).

## Revision policy (standing)

Feedback returns within 3 calendar days of each submission. For M00–M11, M13–M14,
and M17–M21, a revised version may be submitted within 7 days of feedback for up
to half the lost points (the revision habit is itself part of the milestone
grade bucket). M12 (poster), M16 (Expo), M22 (defense), and M23 (dossier) are
performance/terminal artifacts — no post-hoc revision, which is announced from
week 1.

## The M09 approach branches

The pilot analysis is one milestone with four rubric branches — the student
executes the branch their declared approach requires:

- **Description branch:** honest summary tables + distributions of the actual
  data; claims bounded to the data at hand.
- **Inference branch:** estimate + uncertainty interval + a generalization
  argument bounded by the sampling frame.
- **Prediction branch:** baseline + model + held-out comparison + leakage check.
- **Causal branch:** identification argument + effect estimate + one assumption
  probe (or, for observational projects, the honest "association only" analysis
  with the causal design that WOULD identify it sketched).

Mixed-approach projects execute their primary branch fully and any secondary
branch's core check. Full rubrics: `_research_project/2026Fall/milestone_09_*.md`.

## External dependency (tracked, non-blocking)

The official **URC abstract deadline is TBD** (external). The internal gate —
abstract complete Fri Oct 9 (meeting M20) — binds regardless; abstracts are
submitted on Brightspace and forwarded when the URC portal opens. The URC Expo
date (Tue Nov 17) and poster deadline (Fri Nov 6) are fixed anchors from the brief.
