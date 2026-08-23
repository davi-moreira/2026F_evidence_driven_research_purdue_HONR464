# ASSESSMENT_ARCHITECTURE — what is graded, why, and how it adds up

Authoritative reconciliation of the v2 grading system for `syllabus.qmd`.
Philosophy: **no conventional midterm or final exam.** The course assesses one
semester-long research project carried through seventeen milestones (M1–M17),
presented at the Purdue Fall Undergraduate Research Expo, and closed with a
public evidence defense and a reproducible final chapter. Individual work is
the default; students may complete a group project with instructor approval.
Grading rewards correctness, transparency, reproducibility, question-design
(compass) alignment, and responsible interpretation — **never coding elegance**
(no computing background is assumed; all machinery is provided).

The v1 six-component / M01–M23 system is preserved at git tag `v1-compass-build`.
Component weights were **CONFIRMED 2026-07-27 (D22)**, split attendance/
participation **2026-07-29 (D31)**, revised by **D51 (2026-08-22)**, clarified
by **D52 (2026-08-23)**, and given their published syllabus wording by **D53
(2026-08-23)**. D52 supersedes D51's split between Final Project Milestones and
Final Project. All project grading now lives in one 50% Final Project category,
using QM474's exact five component items and shares. D53 then replaced the
syllabus prose for that category with QM474's own text and moved the
operational machinery out of the syllabus (see "Syllabus prose" below).
This file, `course_config.yaml assessment:`, and the syllabus Assessments table
must match exactly.

## The confirmed course components (100%) — D52

| Component | Weight | What it contains |
|---|---:|---|
| **Attendance** (iClicker) | **1%** | 85% attendance target |
| **Participation** (rubric) | **9%** | Feedback surveys, lecture-notebook completion, and other constructive contributions to the course |
| **Quizzes** | **20%** | Weekly Friday printed MC topic quizzes |
| **Student Research Lead (SRL) performance** | **20%** | Flipped-lecture leads scored on the SRL rubric (`project/srl/srl_rubric.md`) |
| **Final Project** | **50%** | Milestone Deliverables, Peer Evaluation, Peer Review, Poster Presentation at the Purdue Undergraduate Research Conference, and Instructor/TA Evaluation |
| **Total** | **100%** | |

## QM474 authority and the five Final Project items

QM474's Fall 2026 public
`../../../predictive_analytics/2026F_predictive_analytics_QM474/syllabus.qmd`
supplies the exact component labels, and
its canonical project contract,
`../../../predictive_analytics/2026F_predictive_analytics_QM474/_final_project/2026F/final_project_milestone_reference.md`,
confirms the 30/20/10/20/20 shares (while abbreviating the last two labels).
The five items are **Milestone Deliverables 30% · Peer Evaluation 20% · Peer
Review 10% · Poster Presentation at the Purdue Undergraduate Research Conference
20% · Instructor/TA Evaluation 20%**. HONR uses those component names and shares
without replacing any item:

| Final Project component | Share of Final Project | Course points | HONR grading home |
|---|---:|---:|---|
| **Milestone Deliverables** | 30% | 15 | Equal-weight mean of M1–M17's seventeen 0–100 milestone scores |
| **Peer Evaluation** | 20% | 10 | Confidential per-student evaluation by every teammate (group project) or two assigned project peers (individual project) |
| **Peer Review** | 10% | 5 | M12 Final Project Peer Review rubric; each student completes the required reviews |
| **Poster Presentation at the Purdue Undergraduate Research Conference** | 20% | 10 | `0.70 ×` M13 poster-quality score + `0.30 ×` each student's M15 live-presentation score |
| **Instructor/TA Evaluation** | 20% | 10 | `0.50 ×` M17 Final Research Artifact + `0.25 ×` M17 AI-management portfolio + `0.25 ×` individual Evidence Defense |
| **Total** | **100%** | **50** | |

## Syllabus prose — QM474 adopted verbatim (D53, 2026-08-23)

`syllabus.qmd`'s `### Final Project (50%)` section is QM 47400's Fall 2026 Final
Project text adopted **verbatim**, with only the six deviations recorded below.
Any other difference between the two sections is a defect. Source of the
wording:
`../../../predictive_analytics/2026F_predictive_analytics_QM474/syllabus.qmd`.

| # | QM 47400 | HONR 46400 | Why |
|---|---|---|---|
| 1 | `### Final Project (35%)` | `### Final Project (50%)` | the percentage; HONR's Final Project is 50% under D52 |
| 2 | "In groups, students will complete a practical predictive analytics project" | "Students will complete a practical evidence-driven research project", followed by the individual-default / approved-group sentence | HONR is individual-by-default (D52), and the subject is not predictive analytics |
| 3 | item 2, "productive teamwork" | "productive research work" | "teamwork" is false for a solo researcher |
| 4 | item 3, "Each group will review … other teams' posters" | "Each student will review … the other projects' posters" | no teams by default |
| 5 | item 4, "due date indicated in the syllabus" | "due date indicated in the course schedule" | D13 confines dates to `schedule.qmd` |
| 6 | item 5, "your instructor and the TA will evaluate" | "your instructor will evaluate" | HONR has no TA (D52: "No TA is assumed") |

The five internal shares — 30 / 20 / 10 / 20 / 20 — are **identical in both
courses**, so nothing inside the numbered list changed.

Two adopted QM474 sentences were verified against `planning/MEETING_SCHEDULE.csv`
before being kept, not assumed: the class immediately after the Expo is genuinely
cancelled (HONR meets Mon Nov 16, skips Wed Nov 18, resumes asynchronously Fri
Nov 20), and the printed posters are genuinely distributed in a dedicated
preparation class (meeting 34, Fri 2026-11-13, "the printed poster arrives:
rehearse on the real thing"). One adopted sentence is a forward promise: "A
poster template and assessment rubric will be shared" — the rubric exists
(`project/poster/poster_rubric.md`, M13), the **template does not yet exist**.
It is due by M11 (Wed 2026-11-04) and tracked as workstream L3 on the private
course tracker.

### What the syllabus no longer carries

The syllabus now states only the five component names and their shares of the
Final Project, exactly as QM474 does, and promises that "a comprehensive set of
project guidelines will be provided." The operational machinery moved out of it.
**Nothing is repealed** — D52 remains the ruling decision and every rule below
is still in force; the syllabus governs the weights, and the guidelines document
governs the operational detail.

| Machinery removed from `syllabus.qmd` | Authoritative home now |
|---|---|
| The five-row component table with the share-of-course column (15 / 10 / 5 / 10 / 10) | `_research_project/2026Fall/final_project_grading_and_project_modes.md`; `brightspace/gradebook_spec.md` |
| Per-component scoring rules: Milestone Deliverables = equal-weight mean of the seventeen M1–M17 scores; Poster item = `0.70 ×` M13 poster quality + `0.30 ×` M15 live presentation; Instructor/TA = `0.50 ×` M17 Final Research Artifact + `0.25 ×` M17 AI-management portfolio + `0.25 ×` individual Evidence Defense | the same two files, plus the "Deterministic Final Project scoring rules" table below |
| "How the same five components work in both project modes" (shared vs individual rows) | `_research_project/2026Fall/final_project_grading_and_project_modes.md` |
| "Peer Evaluation is not Peer Review", including `received_rating_score = min(100, 100 × mean received rating / 3)`, `item = 0.80 × received_rating_score +` submission points, the rule that a missing rating never costs its recipient, and the neutral 80 after failed follow-up | `_research_project/2026Fall/final_project_grading_and_project_modes.md`; `project/final_dossier/peer_evaluation_instrument.md` |
| The group-approval conditions: at most one group of two or three, at least three active projects remaining, and a feasible Peer Evaluation plan | `_research_project/2026Fall/final_project_grading_and_project_modes.md`; `course_config.yaml course.project_mode:` |
| The "Final Research Artifact" paragraph and "if no TA is assigned, the instructor records this item" | `_research_project/2026Fall/final_project_grading_and_project_modes.md` |

The standalone conference-URL line that used to follow the grading scale was
deleted as a duplicate: item 4 of the new text carries that URL.

This file stays the internal reconciliation of all of it; the sections below are
the operational detail the syllabus no longer prints.

## Individual-default and group-allowed operation

Students work individually unless the instructor approves a group before shared
work begins. With five students, at most one group of two or three may be
approved. Approval changes who owns shared evidence, not the five components or
their weights. It must preserve at least three active projects so every
student can review at least two other live projects and permit a Peer Evaluation
plan in which each individual researcher has two observers and every student
has a nonempty submission set.

- **Milestone Deliverables.** An individual researcher receives their own M1–M17
  scores. An approved group submits one shared artifact naming every member.
  Shared rubric rows receive a common score; requirements marked individual,
  including each member's AI Research Ledger evidence, are scored per member,
  so recorded milestone scores may differ only on those rows.
- **Peer Evaluation.** Every student has real peer evaluators and there is no
  self-rating. Group members evaluate every teammate. Each individual researcher
  is assigned two project peers who observe their preparation, substantive
  research contribution, communication, dependability, and reciprocal support
  during scheduled studios and checks. The instructor also gives every student
  a nonempty set of required evaluations to submit; received and submission
  sets need not be reciprocal. Ratings are confidential and scored per student.
  This is not Peer Review.
- **Peer Review.** Every student completes the M12 structured criticism, including
  every member of a group. It evaluates criticism of other projects, not
  contribution to one's own project.
- **Poster Presentation at the Purdue Undergraduate Research Conference.** A group's M13 poster-quality score is
  shared; every student is scored individually on live delivery and must present.
- **Instructor/TA Evaluation.** A group's final research artifact subscore is
  shared. The AI-management portfolio and Evidence Defense are individual. The
  instructor records the item; a TA may co-score if one is assigned.

The Peer Evaluation instrument lives at
`project/final_dossier/peer_evaluation_instrument.md`. Its five 1–5 dimensions
follow QM474's accountability instrument, adapted only so assigned project peers
can evaluate observable solo-project practice. Missing evaluations are omitted
from the recipient's mean and never penalize the intended recipient. If
evaluator non-submission leaves no valid received rating after instructor
follow-up, the received-rating portion is the neutral 80 points (equivalent to
a mean of 3); no substitute evaluator is added after observation ends.

## Final Project gradebook arithmetic

The five project shares sum to 100. Applied to HONR's single 50% Final Project,
they contribute **15 + 10 + 5 + 10 + 10 = 50** course points. Together with
Attendance 1, Participation 9, Quizzes 20, and SRL Performance 20, the course
total is **1 + 9 + 20 + 20 + 50 = 100**.

Several milestones produce evidence later evaluated in another Final Project
component. Never copy one raw rubric score into two places. M12's milestone score
records completion, timeliness, versioning, and response; its separate Peer
Review rubric scores the quality of criticism. M13's milestone score records the
on-time, gate-cleared lock; its poster-quality rubric feeds the conference item.
M17's milestone score records the release package; its three terminal rubrics
feed Instructor/TA Evaluation.

## Deterministic Final Project scoring rules

Each component produces one 0–100 score:

| Final Project item | Scoring rule |
|---|---|
| Milestone Deliverables | `mean(M1, M2, …, M17)`; all seventeen scores are equally weighted |
| Peer Evaluation | `0.80 × min(100, 100 × mean received rating / 3) + submission points`, where complete required evaluations with usable comments earn 20 submission points and non-submission earns 0; documented instructor moderation may correct strategic ratings |
| Peer Review | M12 **Final Project Peer Review rubric** (100 points) |
| Poster Presentation at the Purdue Undergraduate Research Conference | `0.70 ×` M13 **poster-quality rubric** + `0.30 ×` M15 **live Expo presentation rubric** |
| Instructor/TA Evaluation | `0.50 ×` M17 **Final Research Artifact rubric** + `0.25 ×` M17 **AI-management portfolio rubric** + `0.25 ×` **Evidence Defense Protocol rubric** |

The `70/30` poster/live split and the `50/25/25` final-evaluation split are HONR
operational rules inside the imported QM474 items; they do not create additional
Final Project components. A normal Peer Evaluation mean of 3 (met expectations),
plus a complete evaluation submission, yields 100. Ratings above 3 do not create
bonus credit; ratings below 3 lower the received-rating portion. If evaluator
non-submission leaves no valid rating after instructor follow-up, use a neutral
mean of 3 for the intended recipient rather than zero or a substitute evaluator;
the non-submitter still loses their own submission points.

## Why these weights

- **There is one project, not a project plus a milestone category.** The 17-step
  development chain is the Milestone Deliverables component of the single 50%
  Final Project.
- **The five QM474 items remain visible and functional.** HONR does not rename
  Peer Evaluation into a portfolio or rename Instructor/TA Evaluation into a
  defense; those artifacts are evidence used inside the named items.
- **Individual accountability survives either project mode.** Actual peers rate
  contribution and follow-through, while the portfolio and defense stay
  individual even when the research artifact is shared.
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
- **Missing AI Research Ledger entry** → the affected student's individual
  Craft/ledger row identified by the milestone brief scores **0**, and that
  submission is **returned** unread (per the CLAUDE.md AI-Ledger rule). A
  separate shared terminal-rubric score changes only when that rubric says so.
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
  individual Craft/ledger row named by that brief**, with a missing entry
  triggering the hard cap above. This is a graded habit, not a formality.
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
