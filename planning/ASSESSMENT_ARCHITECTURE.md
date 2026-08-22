# ASSESSMENT_ARCHITECTURE — what is graded, why, and how it adds up

Authoritative reconciliation of the v2 grading system for `syllabus.qmd`.
Philosophy: **no conventional midterm or final exam.** The course assesses the
research chain itself — a semester-long individual project carried through
seventeen milestones (M1–M17), presented at the Purdue Fall Undergraduate Research
Expo, and closed with a public evidence defense and a reproducible final chapter.
Grading rewards correctness, transparency, reproducibility, question-design
(compass) alignment, and responsible interpretation — **never coding elegance**
(no computing background is assumed; all machinery is provided).

The v1 six-component / M01–M23 system is preserved at git tag `v1-compass-build`.
Component weights were **CONFIRMED 2026-07-27 (D22)**, split attendance/
participation **2026-07-29 (D31)**, then revised by **D51 (2026-08-22)** to
adopt QM474's operative Final Project grading proportions. D51 removes the
standalone Research artifact category, moves its 10 course points into Final
Project, and preserves the paper/chapter/note as a named Final Project
deliverable. This file, `course_config.yaml assessment:`, and the syllabus
Assessments table must match exactly.

## The confirmed course components (100%) — D51

| Component | Weight | What it contains |
|---|---:|---|
| **Attendance** (iClicker) | **1%** | 85% attendance target |
| **Participation** (rubric) | **9%** | Feedback surveys, lecture-notebook completion, and other constructive contributions to the course; colleague audits remain one form of constructive contribution |
| **Quizzes** | **20%** | Weekly Friday printed MC topic quizzes |
| **Student Research Lead (SRL) performance** | **20%** | Flipped-lecture leads scored on the SRL rubric (`project/srl/srl_rubric.md`) |
| **Final Project Milestones** | **20%** | M1–M17 submissions (each presenting a book Milestone version; kick off → develop → submit → revise) |
| **Final Project** | **30%** | Final paper/chapter/note, individual research-process and AI-management portfolio, peer review, poster and Expo presentation, instructor evaluation, and Evidence Defense |
| | **100%** | |

## QM474 → HONR 46400 Final Project mapping

The reference is QM474's Fall 2026 canonical project contract,
`../../predictive_analytics/2026F_predictive_analytics_QM474/_final_project/2026F/final_project_milestone_reference.md`:
Milestone Deliverables 30% · Peer Evaluation 20% · Peer Review 10% · Conference
Poster Presentation 20% · Instructor/TA Evaluation 20%. HONR preserves those
proportions, but its five projects are individual (`course.project_mode`), and
its M1–M17 developmental chain already has a separate 20% course category.

| QM474 component and function | HONR individual-project equivalent | Share of Final Project | Course points | Grading home |
|---|---|---:|---:|---|
| Milestone Deliverables — integrate the work produced across the project | **Final Research Artifact and Milestone Synthesis** — the final paper, chapter, or research note | 30% | 9 | M17 final research artifact; the separate M1–M17 category continues to grade development |
| Peer Evaluation — establish accountability for the work | **Individual Research Process and AI-Management Portfolio** — the student's own ledger, decisions, checks, conflicts, and overrides | 20% | 6 | Full-semester AI Research Ledger and M17 portfolio; no teammate ratings |
| Peer Review — improve another project's communication | **Peer Review** — each student reviews classmates' posters and records how criticism was used | 10% | 3 | M12 structured review submission and its carry-forward record |
| Conference Poster Presentation | **Poster and Expo Presentation** — one individual poster and its required public presentation | 20% | 6 | M13 locked poster plus the live Expo presentation recorded through M15 |
| Instructor/TA Evaluation — evaluate the finished submission | **Instructor Evaluation and Evidence Defense** — the instructor evaluates integrative command of the final dossier through the individual oral defense | 20% | 6 | Evidence Defense Protocol rubric; no TA is assumed |
| | **Total** | **100%** | **30** | |

The QM474 group contract, confidential intra-group peer evaluation, group-member
score adjustments, group meeting cycle, and Poster-to-Product assessment do not
transfer. HONR's structured review of classmates' posters is cross-project peer
critique, not a group-project requirement.

## Final Project gradebook arithmetic

The five project shares are exact QM474 proportions and sum to 100. Applied to
HONR's 30% Final Project category, they contribute **9 + 6 + 3 + 6 + 6 = 30**
course points. The final paper/chapter/note therefore remains explicitly graded
inside Final Project at 9 course points. Davi's instruction moves all 10 points
from the former standalone category into the 30% Final Project umbrella; the
QM474 proportions redistribute one of those points across the other terminal
evidence rather than preserving a separate 10-point artifact line.

Some milestones produce evidence later assessed in a Final Project item. The
two scores answer different questions: **Final Project Milestones** grades the
checkpoint's completion, timeliness, versioning, and response to feedback;
**Final Project** grades the resulting review, artifact, portfolio,
presentation, or defense at terminal quality. Never copy the same rubric score
into both categories. For example, M12 records completion of the four-review
cycle and response record while the Final Project Peer Review item scores the
quality of the criticism; M13 records the on-time, gate-cleared poster lock
while the Poster and Expo item scores the locked poster and live presentation.

## Deterministic Final Project scoring rules

Each Brightspace item receives one independently computable 0–100 score:

| Final Project item | Scoring rule |
|---|---|
| Final Research Artifact and Milestone Synthesis | M17 **Final Research Artifact rubric** (100 points) |
| Individual Research Process and AI-Management Portfolio | M17 **Individual Research Process and AI-Management Portfolio rubric** (100 points) |
| Peer Review | M12 **Final Project Peer Review rubric** (100 points) |
| Poster and Expo Presentation | `0.70 ×` M13 **poster-quality rubric** + `0.30 ×` M15 **live Expo presentation rubric** |
| Instructor Evaluation and Evidence Defense | **Evidence Defense Protocol rubric** (100 points), scored by the instructor using the final dossier as the evidence base |

The `70/30` poster/live split is an HONR operational ruling inside the imported
20% Poster Presentation slot, not an additional QM474 weight: it gives the
persistent, auditable poster most of the item while reserving a material share
for public explanation and question handling. The item remains 20% of Final
Project (6 course points).

The M12/M13/M15/M17 milestone scores are separate process scores. None is an
input to these formulas, and no Final Project score is copied into the milestone
category.

## Why these weights

- **Development and synthesis stay distinct.** The separate 20% milestone
  category rewards the versioned research chain; the 30% Final Project rewards
  what that chain produces and what the student can defend at the end.
- **The final artifact remains load-bearing.** The paper/chapter/note is the
  largest single Final Project component (9 course points), with another 6
  points evaluating the individual process and AI-management record behind it.
- **Public criticism matters twice without becoming group work.** Peer Review
  grades the quality of criticism given; Poster and Expo Presentation grades the
  individual artifact and public communication.
- **The flipped classroom remains 20%.** Leading research investigations is a
  repeated rehearsal of the same judgment and defense expected in the project.

## Rubric DNA — five virtues, one menu

Every milestone rubric in `_research_project/2026Fall/` is a **100-point,
four-band** instrument (Exemplary / Proficient / Developing / Beginning) whose
criterion rows are drawn from this fixed menu, so the same virtues are rewarded
all semester. Each maps to a CLAUDE.md critical rule:

1. **Compass alignment** — the work matches its declared compass position (kind ×
   reach) and design pathway, and stays inside its claim boundary
   (*Inquiry-Declaration Justification*).
2. **Evidence integrity** — every empirical claim traces to a real, retrievable
   source or a reproducible computation (*Evidence-Integrity & Results-
   Verification*).
3. **Verification** — the deliverable records how outputs were cross-checked, and
   AI use is disclosed Specify→Delegate→Interrogate→Inspect→Verify→Document→
   Defend (*Evidence-Integrity* + *AI Research Ledger & SDIIVDD*).
4. **Uncertainty & limitations** — stated and calibrated, neither hidden nor
   spiraling (*Uncertainty & Limitations in Communication*).
5. **Craft & communication** — organized, on-format, on-time, audience-aware; the
   AI Research Ledger is complete (*AI Research Ledger & SDIIVDD*).

## Hard-cap penalty doctrine

Certain failures cap a rubric criterion regardless of the rest of the row — the
teeth behind the course's discipline:

- **Fabricated or unretrievable source** → Evidence integrity capped at Beginning.
- **Untraceable number** (no path from datum to reported figure) → Verification
  capped at Beginning.
- **Non-reproducing result** (headline number does not rerun from the package) →
  Verification capped at Beginning.
- **Missing AI Research Ledger entry** → Craft scored **0** and the submission
  **returned** unread (per the CLAUDE.md AI-Ledger rule).
- **SRL live cap** — presenting an AI answer as settled without verifying it caps
  SRL rubric row 4 (Productive use of AI) at Beginning (`srl_rubric.md`).

## Grade bands & policies

Letter bands follow the standard Purdue scale: A ≥ 93, A− ≥ 90, B+ ≥ 87, B ≥ 83,
B− ≥ 80, C+ ≥ 77, C ≥ 73, C− ≥ 70, D ≥ 60, F < 60. **No curve** (n = 5).

**Revision.** Feedback returns within 3 days of each milestone; most milestones
accept a revised version within **7 days** of feedback for up to half the lost
points (revising is part of the graded craft). **Terminal artifacts have no
revision window** — the deadline governs: **M13** final poster (Sun Nov 8,
11:59 PM), **M17** final chapter + portfolio (Fri Dec 11), and the live **Expo
presentation** (Tue Nov 17, recorded through M15).

**Late.** −10% per day up to 3 days, then not accepted; documented emergencies
handled individually per Purdue policy.

**Honors GPA cap.** The Daniels School GPA-3.3 grading cap does **not** apply
(this is an Honors College course; the cap was removed from the seeded syllabus).
Confirm once with the Honors College before publishing — tracked on the course
board.

## Integrity instruments — where they are graded

- **AI Research Ledger** (what AI did and how it was checked) — appended to every
  deliverable and every notebook session; **audited at every milestone under the
  Craft criterion**, with a missing entry triggering the hard cap above. This is
  a graded habit, not a formality.
- **Claim ledger** (what the research asserts: claim · evidence · verification ·
  boundary · sensitivity survival) — a separate instrument, graded at **M10**
  (research audit), **M16** (research note), and **M17** (final chapter).
- **Reproduction sign-off** — at **M16**, a classmate attests whether the peer's
  headline number reproduces from the package alone.

## SRL grading pipeline

The Student Research Lead score (Component 2) is produced per slot:

1. The lead receives their SRL page **five days ahead** and submits a
   **preparation template two days ahead** for instructor review; the template
   pre-loads rows 2 (Socratic questions), 3 (assumption-probe), 4–5 (AI plan),
   7 (timing), and 8 (project connection).
2. The lead runs the room **live** and is scored on all nine rubric rows
   (`project/srl/srl_rubric.md`, 100 points) during the session.
3. **Revision does not apply** to a live performance; the next of the five slots
   is the improvement window, informed by peer feedback
   (`srl_peer_feedback_form.md`) and the instructor's notes.

Each slot's 100-point score scales to its 4-point course share; the five slots
sum to the 20% component.
