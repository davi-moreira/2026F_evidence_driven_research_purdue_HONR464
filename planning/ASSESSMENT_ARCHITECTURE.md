# ASSESSMENT_ARCHITECTURE — what is graded, why, and how it adds up

Authoritative reconciliation of the v2 grading system for `syllabus.qmd`.
Philosophy: **no conventional midterm or final exam.** The course assesses one
semester-long research project carried through sixteen milestones (M1–M16),
presented at the Purdue Fall Undergraduate Research Expo, and closed with a
reproducible package, a bounded research note, and a written reflection. Individual work is
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
| **Participation** (one undivided block) | **9%** | Studio feedback surveys, the book's "It is your turn" submissions, the student profile survey, the course reflection, and other constructive contributions — every item one equal credit, graded for completion (D57) |
| **Quizzes** | **20%** | Weekly Friday printed MC topic quizzes |
| **Student Research Lead (SRL)** | **20%** | Flipped-lecture leads scored on the SRL rubric (`project/srl/srl_rubric.md`) |
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
| **Milestone Deliverables** | 30% | 15 | Equal-weight mean of M1–M16's sixteen 0–100 milestone scores |
| **Peer Evaluation** | 20% | 10 | Confidential per-student evaluation by every teammate (group project) or two assigned project peers (individual project) |
| **Peer Review** | 10% | 5 | M12 Final Project Peer Review rubric; each student completes the required reviews |
| **Poster Presentation at the Purdue Undergraduate Research Conference** | 20% | 10 | `0.70 ×` M13 poster-quality score + `0.30 ×` each student's M15 live-presentation score |
| **Instructor/TA Evaluation** | 20% | 10 | `1.00 ×` the instructor's evaluation of the final poster submission locked at M13 (D54) |
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
| 6 | item 5, "your instructor and the TA will evaluate" | "your instructor will evaluate" | HONR has no TA (D52: "The instructor records the last item if no TA is assigned.") |

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
| Per-component scoring rules: Milestone Deliverables = equal-weight mean of the sixteen M1–M16 scores; Poster item = `0.70 ×` M13 poster quality + `0.30 ×` M15 live presentation; Instructor/TA = the instructor's evaluation of the M13 final poster submission | the same two files, plus the "Deterministic Final Project scoring rules" table below |
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

- **Milestone Deliverables.** An individual researcher receives their own M1–M16
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
Attendance 1, Participation 9, Quizzes 20, and SRL 20, the course total is
**1 + 9 + 20 + 20 + 50 = 100**.

Several milestones produce evidence later evaluated in another Final Project
component. Never copy one raw rubric score into two places. M12's milestone score
records completion, timeliness, versioning, and response; its separate Peer
Review rubric scores the quality of criticism. M13's milestone score records the
on-time, gate-cleared lock; its poster-quality rubric feeds the conference item.
M13's poster is read a second time, as research communication, for
Instructor/TA Evaluation — a different judgement from poster quality, and the
one place a single artifact feeds two components (D54).

## Deterministic Final Project scoring rules

Each component produces one 0–100 score:

| Final Project item | Scoring rule |
|---|---|
| Milestone Deliverables | `mean(M1, M2, …, M16)`; all sixteen scores are equally weighted |
| Peer Evaluation | `0.80 × min(100, 100 × mean received rating / 3) + submission points`, where complete required evaluations with usable comments earn 20 submission points and non-submission earns 0; documented instructor moderation may correct strategic ratings |
| Peer Review | M12 **Final Project Peer Review rubric** (100 points) |
| Poster Presentation at the Purdue Undergraduate Research Conference | `0.70 ×` M13 **poster-quality rubric** + `0.30 ×` M15 **live Expo presentation rubric** |
| Instructor/TA Evaluation | `1.00 ×` the instructor's evaluation of the **M13 final poster submission**, judged as research communication (D54) |

The `70/30` poster/live split is an HONR
operational rule inside the imported QM474 items; they do not create additional
Final Project components. A normal Peer Evaluation mean of 3 (met expectations),
plus a complete evaluation submission, yields 100. Ratings above 3 do not create
bonus credit; ratings below 3 lower the received-rating portion. If evaluator
non-submission leaves no valid rating after instructor follow-up, use a neutral
mean of 3 for the intended recipient rather than zero or a substitute evaluator;
the non-submitter still loses their own submission points.

## Participation — one undivided block (D57, 2026-08-23)

Participation is **9%, undivided**. Every required item is worth the same single
credit and the block is their sum. **No internal split is published, and none is
applied.** An earlier draft proposed 5% reading feedback + 2% lecture-notebook
completion + 2% class contribution; that split is rejected and must not be
reinstated.

| # | Item | Count (typical student) | Due | Graded |
|---|---|---:|---|---|
| 1 | EDR\|AI **"It is your turn"** submissions | 36 | 11:59 PM on the date that chapter's reading was due | completion |
| 2 | **Studio feedback survey** (one Qualtrics link, 12 responses) | 12 | 11:59 PM on the Sunday that ends the studio week | completion |
| 3 | **Student profile survey** | 1 | Sun Aug 30, 2026 | completion |
| 4 | **Course reflection** | 1 | Fri Dec 11, 2026 | completion |
| 5 | **Scored Synthetic Colleague audits** | 10 | at each audit's session | completion; the four-row rubric decides validity |
| | **Baseline N** | **60** | | |

Credit is `1.0` on time, `0.5` within seven days, `0` otherwise; the lowest
`d = ⌈0.10 × N⌉` credits are dropped automatically (**d = 6**), and

```
participation points = 9.0 × (sum of the highest N − d credits) / (N − d)
```

The syllabus clause "other constructive contributions to the course" is a
**documented adjustment of at most ±0.9 points** on the ledger result, not a
separate bucket with a weight.

**Two things were retired to make this work.** Lecture notebooks are **not
collected** — they are class instruments, and nothing is graded on them. Reading
feedback is no longer per chapter: 40 responses competed with the work they were
meant to improve, so 12 per-studio responses replace them, closing the same
Sunday night as the studio's milestone.

**Why "It is your turn" moved out of the milestones.** The book's closing
sections were previously handed in bundled into the Friday milestone, days after
the reading they belong to. Collecting them on the reading date does three
things at once: it makes the reading deadline real, it puts the practice next to
the chapter that teaches it, and it gives Studio 12 — which D54 left teaching
but collecting nothing — something to collect. The milestone still names its
chapters in its Book Anchor and still carries the work forward into the dossier;
it just no longer re-collects it.

The full contract is `surveys/participation_grading.md`. The two dated schedules
are generated by `scripts/build_participation_schedules.py` into
`planning/IYT_SUBMISSION_SCHEDULE.md` and
`planning/STUDIO_FEEDBACK_SCHEDULE.md`.

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
11:59 PM) and the live **Expo presentation** (Tue Nov 17, recorded through
M15). Every other milestone is worked at its Friday studio and due the Sunday
after, 11:59 PM (D55); M11 (Wed, at class) and M12 (Fri, 5:00 PM) keep weekday
deadlines the conference block depends on.

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
  (research audit) and **M16** (research note, the last milestone).
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
