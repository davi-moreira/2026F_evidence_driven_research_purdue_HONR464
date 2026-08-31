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
by **D52 (2026-08-23)**, given their published syllabus wording by **D53
(2026-08-23)**, turned into a completion contract for Participation by **D57
(2026-08-23)**, amended by **D58 (2026-08-23)**, amended again by **D61
(2026-08-23)**, amended by **D74 (2026-08-31)**, and last amended by **D75
(2026-08-31)**, which changed no weight at all. D52 supersedes D51's
split between Final Project Milestones and Final Project. All project grading now
lives in one 55% Final Project category, using QM474's exact five component items
under names that were never renamed. D53 then replaced the syllabus prose for
that category with QM474's own text and moved the operational machinery out of
the syllabus (see "Syllabus prose" below). **D58 retired the quiz category for
this edition**, created **IYT Practice at 10%** to carry the book's "It is your
turn" sections, and raised **Student Research Lead from 20% to 30%**. **D61
amended those two weights only**: IYT Practice rose from **10% to 15%** and
Student Research Lead fell from **30% to 25%**. Every other D58 mechanic is
unchanged — the undivided completion contracts, the credit and drop rules, the
retired quiz category, and the Friday studio frame.

**D74 (2026-08-31) is the current ruling on the weights.** The **Student Research
Lead category is retired for this edition**, and with it the live nine-row rubric.
Every Mon/Wed lecture from Week 2 now opens with a ten-minute **lab meeting**, and
**D75 (2026-08-31) is the current ruling on what happens inside it**: the
instructor asks the room how the projects are going, and the room answers — what
was decided since last time, what the evidence looks like, where somebody is
stuck. **Nothing said there is graded**, and the instructor leads the lesson from
minute 10. D74 had filled those same ten minutes with a designated **reporter**
(seven minutes on a decision from their own project, three minutes of questions
from the room); **D75 withdrew the assignment entirely** — no reporter on any
lecture, no slot draw, no assigned question, and no preparation of any kind before
class, by anyone. In the retired category's place stands **Lecture Notebooks at
20%**, the course's **third undivided completion contract**: the notebook `nbNN`
worked in class is now collected once a week per student and graded on completion
only. The five points that remain — `1 + 9 + 15 + 20 = 45` — are forced inside the
Final Project, which rises from **50% to 55%** with **Milestone Deliverables
rising from 15 to 20 course points**. No Final Project component was renamed, and
no scoring rule inside a component changed. **D75 moved no weight, no formula, no
`N` and no drop count** — it changed only how the ten-minute opener is populated.
**Nothing was deleted:** every SRL artefact stays on disk for a future edition,
exactly as D58 kept the quiz banks (see "SRL grading pipeline — retired for this
edition" at the end of this file), and D75 added the drawn roster and the
notebook generator's report-plan constant to that kept-on-disk list.

This file, `course_config.yaml assessment:`, and the syllabus Assessments table
must match exactly.

## The confirmed course components (100%) — D52, amended D58, D61 and D74

| Component | Weight | What it contains |
|---|---:|---|
| **Attendance** (iClicker) | **1%** | 85% attendance target |
| **Participation** (one undivided block) | **9%** | Studio feedback surveys (12), the student profile survey, the course reflection, and other constructive contributions — every item one equal credit, graded for completion (D57, amended D58) |
| **IYT Practice** (one undivided block) | **15%** | The EDR\|AI "It is your turn" sections of the required chapters, each due 11:59 PM on the date that chapter's reading was due, graded for completion (D58, amended D61) |
| **Lecture Notebooks** (one undivided block) | **20%** | The weekly lecture notebook `nbNN` worked in class, one submission per week per student, due 11:59 PM on the Sunday that ends the studio week, graded for completion (D74) |
| **Final Project** | **55%** | Milestone Deliverables, Peer Evaluation, Peer Review, Poster Presentation at the Purdue Undergraduate Research Conference, and Instructor/TA Evaluation |
| **Total** | **100%** | |

**No quiz category.** D58 retired it for this edition: no quiz is administered and
nothing is scored on one. The banks under `_quizzes/` (gitignored), their builders,
and `scripts/audit_answer_length.py` are kept for a future edition and are never
deleted — see "Quizzes — retired for this edition" below.

**No Student Research Lead category.** D74 retired it for this edition: no live
lead is scored, and the nine-row rubric is not applied. The lecture opener is now
the ungraded ten-minute lab meeting, which since **D75** carries no assignment at
all — no reporter, no draw, no assigned question, no preparation. All of
`project/srl/` — handbook, rubric, Socratic question bank, AI integration guide,
prep template, peer feedback form, submission instructions, absent-lead and
instructor-intervention protocols — plus `scripts/assign_srl_slots.py`,
`scripts/build_srl_packet.py`, the drawn roster in `_adm/roster/`, and
`scripts/nbbuild.py`'s `REPORT_PLAN` constant (now gated by
`INJECT_REPORT_PLAN = False`) are kept for a future edition and are never
deleted. The per-lecture questions guide is kept in full and re-owned to the
instructor. See "SRL grading pipeline — retired for this edition" below.

## QM474 authority and the five Final Project items

QM474's Fall 2026 public
`../../../predictive_analytics/2026F_predictive_analytics_QM474/syllabus.qmd`
supplies the exact component labels, and
its canonical project contract,
`../../../predictive_analytics/2026F_predictive_analytics_QM474/_final_project/2026F/final_project_milestone_reference.md`,
confirms the 30/20/10/20/20 shares (while abbreviating the last two labels).
QM474's five items are **Milestone Deliverables 30% · Peer Evaluation 20% · Peer
Review 10% · Poster Presentation at the Purdue Undergraduate Research Conference
20% · Instructor/TA Evaluation 20%**. HONR uses those component names without
replacing or renaming any item. **D74 changed one thing about the shares and
nothing else:** the five course points freed by retiring the SRL category went to
**Milestone Deliverables**, which rose from 15 to 20 course points, so HONR's
project-share column no longer reads 30/20/10/20/20.

Because `20 / 55` does not terminate, **student-facing surfaces now print
percentages of the final grade** rather than shares of the Final Project. The
exact project shares are kept in `course_config.yaml
final_project_breakdown:` as the machine record only:

| Final Project component | Share of the final grade (student-facing) | Course points | Exact project share (machine record) | HONR grading home |
|---|---:|---:|---:|---|
| **Milestone Deliverables** | 20% | 20 | 36.37% | Equal-weight mean of M1–M16's sixteen 0–100 milestone scores |
| **Peer Evaluation** | 10% | 10 | 18.18% | Confidential per-student evaluation by every teammate (group project) or two assigned project peers (individual project) |
| **Peer Review** | 5% | 5 | 9.09% | M12 Final Project Peer Review rubric; each student completes the required reviews |
| **Poster Presentation at the Purdue Undergraduate Research Conference** | 10% | 10 | 18.18% | `0.70 ×` M13 poster-quality score + `0.30 ×` each student's M15 live-presentation score |
| **Instructor/TA Evaluation** | 10% | 10 | 18.18% | `1.00 ×` the instructor's evaluation of the final poster submission locked at M13 (D54) |
| **Total** | **55%** | **55** | **100.00%** | |

Milestone Deliverables carries the rounding remainder (36.37 rather than 36.36) so
the machine column sums to exactly 100.00. Nothing inside a component changed:
Milestone Deliverables is still the equally weighted mean of the M1–M16 milestone
scores, and the four other scoring rules are word for word what D52 and D54 set.

## Syllabus prose — QM474 adopted verbatim (D53, 2026-08-23; seventh deviation D74)

`syllabus.qmd`'s `### Final Project (55%)` section is QM 47400's Fall 2026 Final
Project text adopted **verbatim**, with only the seven deviations recorded below.
Any other difference between the two sections is a defect. Source of the
wording:
`../../../predictive_analytics/2026F_predictive_analytics_QM474/syllabus.qmd`.

| # | QM 47400 | HONR 46400 | Why |
|---|---|---|---|
| 1 | `### Final Project (35%)` | `### Final Project (55%)` | the percentage; HONR's Final Project is 55% under D74 (it was 50% from D52 until D74 moved the freed SRL points into it) |
| 2 | "In groups, students will complete a practical predictive analytics project" | "Students will complete a practical evidence-driven research project", followed by the individual-default / approved-group sentence | HONR is individual-by-default (D52), and the subject is not predictive analytics |
| 3 | item 2, "productive teamwork" | "productive research work" | "teamwork" is false for a solo researcher |
| 4 | item 3, "Each group will review … other teams' posters" | "Each student will review … the other projects' posters" | no teams by default |
| 5 | item 4, "due date indicated in the syllabus" | "due date indicated in the course schedule" | D13 confines dates to `schedule.qmd` |
| 6 | item 5, "your instructor and the TA will evaluate" | "your instructor will evaluate" | HONR has no TA (D52: "The instructor records the last item if no TA is assigned.") |
| 7 | the five numbered items print **shares of the Final Project** — 30 / 20 / 10 / 20 / 20 | the five numbered items print **shares of the final grade** — **20 / 10 / 5 / 10 / 10** | D74 gave Milestone Deliverables the 5 course points freed by retiring the SRL category, so the project shares are no longer QM474's and no longer terminate (`20 / 55 = 36.36…`); a course percentage is exact, and it is the number a student can check against the Assessments table |

**The seventh deviation, in full.** From D53 until D74 the five internal shares
were **identical in both courses**, so nothing inside the numbered list had
changed. That is no longer true. HONR's shares of the Final Project are now
36.37 / 18.18 / 9.09 / 18.18 / 18.18, and those figures appear **only** in
`course_config.yaml final_project_breakdown:`. Every student-facing surface — the
syllabus, the milestone briefs, the Brightspace spec, the project-guidelines
document — prints the course percentages instead. **No component was renamed and
no scoring rule inside a component changed**; the deviation is a change of
denominator and of the number printed, nothing more.

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

The syllabus now states only the five component names and their percentages, in
QM474's own numbered-list form, and promises that "a comprehensive set of project
guidelines will be provided." Since D74 the percentages printed there are shares
of the **final grade** (20 / 10 / 5 / 10 / 10) rather than of the Final Project;
the list itself is otherwise unchanged. The operational machinery moved out of it.
**Nothing is repealed** — D52 remains the ruling decision and every rule below
is still in force; the syllabus governs the weights, and the guidelines document
governs the operational detail.

| Machinery removed from `syllabus.qmd` | Authoritative home now |
|---|---|
| The five-row component table with both columns — share of the Final Project and share of the course (D74: 20 / 10 / 5 / 10 / 10 course points, from 15 / 10 / 5 / 10 / 10) | `_research_project/2026Fall/final_project_grading_and_project_modes.md`; `brightspace/gradebook_spec.md` |
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
work begins. With six students, at most one group of two or three may be
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

The five project shares sum to 100.00. Applied to HONR's single 55% Final Project,
they contribute **20 + 10 + 5 + 10 + 10 = 55** course points. Together with
Attendance 1, Participation 9, IYT Practice 15, and Lecture Notebooks 20, the
course total is **1 + 9 + 15 + 20 + 55 = 100**.

D74's arithmetic is worth stating once in the open, because it is what forced the
Final Project up. Retiring the 25% SRL category left 25 points to place. Twenty
went to the new Lecture Notebooks contract. That fixes the four non-project
categories at `1 + 9 + 15 + 20 = 45`, so the remaining **5 points had nowhere to
go but inside the Final Project** — and they went to Milestone Deliverables, the
component that already scores the sixteen-step chain those notebooks feed.

Several milestones produce evidence later evaluated in another Final Project
component. Never copy one raw rubric score into two places. M12's milestone score
records completion, timeliness, versioning, and response; its separate Peer
Review rubric scores the quality of criticism. M13's milestone score records the
on-time, gate-cleared lock; its poster-quality rubric feeds the conference item.
M13's poster is read a second time, as research communication, for
Instructor/TA Evaluation — a different judgement from poster quality, and the
one place a single artifact feeds two components (D54).

## Deterministic Final Project scoring rules

Each component produces one 0–100 score. **D74 left every rule in this table
untouched** — it changed what each 0–100 score is worth in the course, never how
the score itself is produced:

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

## Participation — one undivided block (D57, amended D58 and D74)

Participation is **9%, undivided**. Every required item is worth the same single
credit and the block is their sum. **No internal split is published, and none is
applied.** An earlier draft proposed 5% reading feedback + 2% lecture-notebook
completion + 2% class contribution; that split is rejected and must not be
reinstated. **D58 moved the "It is your turn" family out of this block** into its
own IYT Practice category — 10% under D58, **15%** under D61 — stated in the next
section; the 9%, its mechanics, and its refusal to split internally are otherwise
unchanged. **D74 changed nothing here either** — not the weight, not the item
list, not N, not d, not the formula, not the ±0.9 adjustment.

| # | Item | Count (typical student) | Due | Graded |
|---|---|---:|---|---|
| 1 | **Studio feedback survey** (one Qualtrics link, 12 responses) | 12 | 11:59 PM on the Sunday that ends the studio week | completion |
| 2 | **Student profile survey** | 1 | Sun Aug 30, 2026 | completion |
| 3 | **Course reflection** | 1 | Fri Dec 11, 2026 | completion |
| | **Baseline N** | **14** | | |

Credit is `1.0` on time, `0.5` within seven days, `0` otherwise; the lowest
`d = ⌈0.10 × N⌉` credits are dropped automatically (**d = 2**), and

```
participation points = 9.0 × (sum of the highest N − d credits) / (N − d)
                     = 9.0 × (sum of the highest 12 credits) / 12
```

The syllabus clause "other constructive contributions to the course" is a
**documented adjustment of at most ±0.9 points** on the ledger result, not a
separate bucket with a weight.

**Two things were retired to make this work.** Lecture notebooks were **not
collected** — they were class instruments, and nothing was graded on them.
Reading feedback is no longer per chapter: 40 responses competed with the work
they were meant to improve, so 12 per-studio responses replace them, closing the
same Sunday night as the studio's milestone.

> **Amended by D74 (2026-08-31).** The first of those two retirements now stands
> in a narrower form. Lecture notebooks **are** collected, weekly, under their own
> **Lecture Notebooks (20%)** category described two sections below. What D57
> banned and D74 keeps banned is lecture-notebook completion **as a participation
> item**: it never re-enters this 9% block, never joins this block's credit pool,
> and never carries the ±0.9 contribution adjustment. The second retirement —
> per-chapter reading feedback — is untouched.

The full contract for this block is `surveys/participation_grading.md`. The dated
schedule is generated by `scripts/build_participation_schedules.py` into
`planning/STUDIO_FEEDBACK_SCHEDULE.md`; the same script writes the IYT Practice
schedule described below.

## IYT Practice — 15% (D58, amended D61, 2026-08-23)

IYT Practice is its own top-level category, holding the one item family that D58
took out of Participation: the EDR|AI **"It is your turn"** sections of the
required chapters. The mechanics are Participation's, with their own credit pool.

| # | Item | Count (typical student) | Due | Graded |
|---|---|---:|---|---|
| 1 | EDR\|AI **"It is your turn"** submissions | 35 | 11:59 PM on the date that chapter's reading was due | completion |
| | **Baseline N** | **35** | | |

The 35 is 34 chapters everyone reads plus **one** pathway chapter, the student's
own declared route. The contrast route the instructor assigns is still required reading, and it is still worked in Wednesday's jigsaw and in the milestone's mandated-contrast section, but its "It is your turn" section is not collected (D60). A declared design with stages owes one
more (N = 36), and `⌈0.10 × 36⌉` is still 4, so the drop count does not grow with
it. Credit is `1.0` on time, `0.5` within seven days,
`0` otherwise; the lowest `d = ⌈0.10 × N⌉` credits are dropped automatically
(**d = 4**), and

```
iyt points = 15.0 × (sum of the highest N − d credits) / (N − d)
           = 15.0 × (sum of the highest 31 credits) / 31
```

The ±0.9-point contribution adjustment belongs to Participation alone and is never
applied here. The dated schedule is `planning/IYT_SUBMISSION_SCHEDULE.md`,
generated by `scripts/build_participation_schedules.py`; the student-facing
contract is `surveys/participation_grading.md`.

**Why "It is your turn" moved out of the milestones, and then out of
Participation.** The book's closing sections were previously handed in bundled
into the Friday milestone, days after the reading they belong to. Collecting them
on the reading date does three things at once: it makes the reading deadline real,
it puts the practice next to the chapter that teaches it, and it gives Studio 12 —
which D54 left teaching but collecting nothing — something to collect. The
milestone still names its chapters in its Book Anchor and still carries the work
forward into the dossier; it just no longer re-collects it. D58 then gave the
family its own category, at 10% and then 15% under D61, because it was by far the
largest family in the participation block, and a body of required practice that
size should be named for what it is rather than hidden inside participation.

## Lecture Notebooks — 20% (D74, 2026-08-31)

Lecture Notebooks is the course's **third undivided completion contract**, and it
is the category that replaces the retired 25% Student Research Lead. It holds one
item family: the weekly lecture notebook `nbNN` a student works in class. The
mechanics are Participation's and IYT Practice's, with their own credit pool.

| # | Item | Count (typical student) | Due | Graded |
|---|---|---:|---|---|
| 1 | **Weekly lecture notebook** (`nb01`–`nb16`, worked in class and handed in) | 16 | 11:59 PM on the Sunday that ends the studio week; Week 16 closes **Fri Dec 11**, the last class day | completion |
| | **Baseline N** | **16** | | |

Credit is `1.0` on time, `0.5` within seven days, `0` otherwise; the lowest
`d = ⌈0.10 × N⌉` credits are dropped automatically (**d = 2**), and

```
lecture notebook points = 20.0 × (sum of the highest N − d credits) / (N − d)
                        = 20.0 × (sum of the highest 14 credits) / 14
```

**Completion means completion.** A notebook earns its credit when it has been
worked through and handed in. It is never scored on whether the answers came out
right, never scored on the quality of the reasoning inside it, and **never scored
on anything said in that week's lab meeting** — the lab meeting carries no grade
at all. The submission covers the whole week's work in that notebook: **the seven
in-class moves and the `📒` AI Research Ledger row for each lecture**. That is the
whole content list; it names no lab-meeting cell.

> **Amended by D75 (2026-08-31).** This list carried a third item until D75: the
> injected `📣 My Report Plan` cell, filled lines 1–4 when the lab-meeting slot was
> yours and line 5 otherwise, so the whole room arrived with a question. **That
> cell no longer exists.** D75 withdrew the reporter assignment, and
> `scripts/nbbuild.py` stops injecting the cell (`INJECT_REPORT_PLAN = False`), so
> it can no longer be part of what is collected — nothing about the lab meeting is
> prepared, by anyone. The `REPORT_PLAN` constant stays in the script, unapplied,
> for a future edition. **Every number in this contract is untouched:** `N = 16`,
> `d = 2`, the credit rule, the Sunday rule with D74a's Fri Sep 4 Week-1 override
> and the Fri Dec 11 Week-16 close, and the `20.0 × …` formula are exactly as D74
> set them.

This is **not participation**. It has its own N, its own drop allowance and its
own formula, it never joins the participation credit pool, and it never carries
participation's ±0.9 contribution adjustment. D57's ban survives in that amended
form: lecture-notebook completion may never return **as a participation item**.

The machine spine is `course_config.yaml lecture_notebooks:`; the dated schedule
is `planning/LECTURE_NOTEBOOK_SCHEDULE.md`, generated alongside the other two
completion schedules and never hand-edited. The student-facing contract sits with
the other two in `surveys/participation_grading.md`, which since D74 is the whole
contract for all **three** completion categories.

**Why this category exists.** Students were afraid of leading sessions, and the
largest source of that fear was being graded on teaching unfamiliar quantitative
content to peers. D74 removed the source rather than softening it: the graded
thing is now the work itself, which every student does every week anyway and
which is the direct input to the milestone chain. Twenty points is close to the
twenty-five it replaces, so the course still weights sustained weekly effort
heavily — it simply stops paying for a performance and starts paying for the
record of the work. And because the notebook is where the AI Research Ledger rows
accumulate, collecting it weekly makes the course's central discipline visible on
a weekly cadence instead of only at milestones.

## Quizzes — retired for this edition (D58, 2026-08-23)

There is **no quiz category**. No quiz is administered, no quiz is printed, and
nothing in the gradebook is scored on one. The Friday studio lost its 0–10 quiz
block with it, and the milestone sprint absorbed those ten minutes.

The **material is kept**. The banks under `_quizzes/` (gitignored), every
quiz-building script, and the `scripts/audit_answer_length.py` option-length gate
stay in the repository for a future edition, and CLAUDE.md's dormant *MC
Option-Length Parity* rule still governs them if quizzes ever return. Retiring the
category is never permission to delete a quiz file or a quiz script.

## Why these weights

- **There is one project, not a project plus a milestone category.** The 16-step
  development chain (M1–M16) is the Milestone Deliverables component of the single
  55% Final Project.
- **The five QM474 items remain visible and functional.** HONR does not rename
  Peer Evaluation into a portfolio or rename Instructor/TA Evaluation into a
  defense; those artifacts are evidence used inside the named items.
- **Individual accountability survives either project mode.** Actual peers rate
  contribution and follow-through, while the portfolio and defense stay
  individual even when the research artifact is shared.
- **The flipped classroom rose to 30%** *(superseded by D74; kept as the record of
  why the weight was where it was)*. Leading research investigations was a
  repeated rehearsal of the same judgment and defense expected in the project, and
  it was the second-largest thing the course graded. (D61 later settled it at 25%;
  it was still second-largest.)
- **The retired quiz weight went where the work is.** D58 removed the 20% quiz
  category, and its weight was redistributed to the two places that already carry
  real, repeated practice: 10 points to **Student Research Lead** (20 → 30) and 10
  points to the new **IYT Practice** category, which collects the book's "It is
  your turn" sections on the date each chapter's reading was due. Nothing new was
  added to the workload; what was already being done is now what is weighted.
- **D61 rebalanced those two, and only those two.** Five points moved from
  **Student Research Lead** (30 → 25) to **IYT Practice** (10 → 15): the "It is
  your turn" family is the most frequent required practice in the course — 35
  submissions against the four or five lecture slots a student drew — and its
  weight now reflects that cadence. Both remained completion-and-rubric contracts
  exactly as D58 defined them.
- **D74 stopped paying for a performance and started paying for the work.** The
  25% Student Research Lead category is retired for this edition. Twenty of its
  points became **Lecture Notebooks**, a completion contract over the sixteen
  notebooks every student already works in class; the lab meeting that replaced
  the lead carries **no grade at all**. This is the third completion
  contract in a course that now grades three kinds of steady effort by completion —
  showing up to the shared instruments (9%), practising the book (15%), and doing
  the weekly lab work (20%) — and reserves judgment-based scoring for the project
  itself.
- **The last 5 points had one place to go.** With the four non-project categories
  fixed at `1 + 9 + 15 + 20 = 45`, the remainder had to sit inside the Final
  Project. It went to **Milestone Deliverables** (15 → 20 course points), the
  component the notebooks feed most directly, so the course's largest single
  weight is still the sixteen-step chain that builds the research. The Final
  Project as a whole rises 50% → 55%.
- **D75 moved nothing in this table.** Withdrawing the reporter assignment did not
  touch a weight, a formula, an `N`, a drop count or a scoring rule; the four
  completion and project categories stand exactly as D74 left them. It is recorded
  here only because it is the reason the Lecture Notebooks content list no longer
  names a lab-meeting cell: the graded thing was never the report, and now there
  is no report to not grade.

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
- **SRL live cap — not applied this edition (D74), kept for a future one.**
  Presenting an AI answer as settled without verifying it capped SRL rubric row 4
  (Productive use of AI) at Beginning (`srl_rubric.md`). The rubric is not applied
  this edition, so the cap has nothing to bite on: nothing said in the lab meeting
  is graded, and since D75 nobody is even assigned to speak in it. The rule and
  the rubric stay on disk unchanged. The discipline itself
  does not lapse — an unverified AI answer presented as settled still meets the
  evidence-integrity and verification caps above wherever it reaches a graded
  deliverable, and the instructor still corrects it live under the accuracy lock.

None of these caps touches a completion contract. Participation, IYT Practice and
Lecture Notebooks are graded on whether the work was submitted, so a capped
criterion in a milestone rubric never reduces a completion credit — and a
completion credit never excuses a capped criterion.

## Grade bands & policies

Letter bands follow the standard Purdue scale: A ≥ 93, A− ≥ 90, B+ ≥ 87, B ≥ 83,
B− ≥ 80, C+ ≥ 77, C ≥ 73, C− ≥ 70, D ≥ 60, F < 60. **No curve** (n = 6).

**Revision.** Feedback returns within 3 days of each milestone; most milestones
accept a revised version within **7 days** of feedback for up to half the lost
points (revising is part of the graded craft). **Terminal artifacts have no
revision window** — the deadline governs: **M13** final poster (Sun Nov 8,
11:59 PM) and the live **Expo presentation** (Tue Nov 17, recorded through
M15). Every other milestone is worked at its Friday studio and due the Sunday
after, 11:59 PM (D55); M11 (Wed, at class) and M12 (Fri, 2:30 PM) keep weekday
deadlines the conference block depends on.

**Revision and lateness do not reach the completion contracts.** Participation,
IYT Practice and Lecture Notebooks have no revision window and no per-day
deduction, because there is nothing to revise toward: each item is worth one
credit, and the credit rule *is* the late policy — `1.0` on time, `0.5` within
seven days, `0` after that, with the lowest `d` credits dropped automatically.
The two rules below govern the rubric-scored milestones.

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

## The lab meeting — ungraded, and what it replaced (D74, amended D75)

Every Mon/Wed lecture from Week 2 opens with a **ten-minute lab meeting**. Since
**D75** it is an **open round**: the instructor asks the room how the projects are
going, and the room answers — what was decided since last time, what the evidence
looks like, where somebody is stuck. **Nobody is designated to present, on any
lecture. Nothing is prepared in advance, by anyone.** From minute 10 the
instructor leads the lesson, owning accuracy, the AI tooling and the clock.

**Nothing said in the lab meeting is scored.** There is no rubric, no per-slot
points, no preparation grade and no penalty for having little to say on a given
day. The one graded thing in the neighbourhood is the notebook itself, collected
weekly under **Lecture Notebooks (20%)** on completion — and that credit is earned
by working the notebook through, never by anything that happened in the opening
ten minutes.

### The reporter and the draw — withdrawn by D75, kept here as the record

*Not in force.* What follows is how D74 populated these same ten minutes, kept as
the record and as the starting point if a future edition brings the assignment
back.

> One student was that lecture's **reporter**: seven minutes on a decision from
> their own project and the evidence behind it, then three minutes of questions
> from the room. The reporter did not teach the lecture's concept. The report was
> already ungraded under D74 — no rubric, no per-slot points, no preparation
> grade — so a student who reported badly and handed in a worked notebook lost
> nothing. The draw was unchanged from D69/D71: **25 reporting lectures over the
> enrolled students, drawn `4/4/4/4/4/5` at six**, one reporter per lecture,
> assigned at random at the start of the semester with no rotation and no seats.
> D74 renamed what the draw produced — each lecture had a reporter rather than a
> lead — and did not re-run it. Each lecture's notebook carried an injected
> **📣 My Report Plan** cell, filled lines 1–4 by that lecture's reporter and line
> 5 by everyone else.

**D75 withdrew all of it for this edition** — the designation, the draw, the
assigned question and the preparation cell — because a designated, dated,
individually-owned slot is still a performance with your name on a calendar, and
Davi asked for the moment without the assignment. An open round needs no draw, no
packet, no announcement and no swap rule, and it reaches every student every
lecture instead of one student every fourth lecture.

**Deleted: nothing.** `scripts/assign_srl_slots.py`, `scripts/build_srl_packet.py`,
the drawn roster in `_adm/roster/`, `planning/SRL_ASSIGNMENT_SCHEDULE.md` and
`scripts/nbbuild.py`'s `REPORT_PLAN` constant all stay on disk, unapplied.
Restoring the reporter model in a future edition costs setting
`INJECT_REPORT_PLAN = True` and re-running the draw. The machine record of the
current arrangement is `course_config.yaml lab_meeting:` (the block was named
`srl:` before D74), where `reporter: none`, `assignment: none` and
`prepared_in_advance: false` are the operative fields.

**One thing D75 cannot do from this repository.** If the Week-1 announcement
telling students they hold slots on named dates was already posted, those slots
are withdrawn and the students need to hear it on the course platform: the lab
meeting stays, no one is assigned, nothing is prepared, and nothing about it is
graded.

The notebook cell that opens each lecture is now headed **`### 📣 Lab Meeting`**
(it read `### 📣 Lab Meeting: Today's Reporter` under D74). The 🧩 Research Puzzle
and the 🔎 Questions to Keep You Thinking guide are untouched.

### SRL grading pipeline — retired for this edition, kept for a future one

**No SRL score is produced this edition.** The 25% category is retired and the
nine-row rubric is not applied. **D75 went further and withdrew the slot draw
itself**, so not even the ungraded reporter designation survives: no student holds
a lecture. What follows is the pipeline as it stood, kept here as the record and
as the starting point if a future edition brings the role back. It is not in
force, and every count in it describes the draw as it was run, not the roster as
it stands.

1. The lead worked from the SRL brief **about one week ahead** and submitted a
   **filled notebook by 11:59 PM the calendar day before the lecture** for
   instructor review — `lecture − 1 day`, with no class-day snapping, so a Sunday
   or a holiday was a perfectly good submission date (**D66**, which corrected
   D18's "two days ahead" to match the course platform). The template pre-loaded
   rows 2 (Socratic questions), 3 (assumption-probe), 4–5 (AI plan), 7 (timing),
   and 8 (project connection).
2. The lead ran the room **live** and was scored on all nine rubric rows
   (`project/srl/srl_rubric.md`, 100 points) during the session.
3. **Revision did not apply** to a live performance; the student's next drawn slot
   was the improvement window, informed by peer feedback
   (`srl_peer_feedback_form.md`) and the instructor's notes.

The component was the **equal-weight mean of a student's own slot scores**, scaled
to the 25 course points — one scored gradebook item per student, entered after
each of their leads and averaged, which is what made an uneven draw harmless
(`brightspace/gradebook_spec.md`). **There was never a fixed per-slot point
value.** An earlier version of this section said each slot scaled to a 5-point
course share because `srl.leads_per_student: 5` implied five slots each; the D69
draw gives **four or five** slots over six students, so a fixed 5 points per slot
would have paid a five-slot student 25 and a four-slot student 20 for identical
work. Any surface that printed a per-slot point value, or that said every student
leads five times, was wrong on both counts.

**Kept on disk, never deleted** (D74 Ruling 5, exactly as D58 kept the quiz banks):
all of `project/srl/` — `srl_handbook.md`, `srl_rubric.md`,
`socratic_question_bank.md`, `srl_ai_integration_guide.md`, `srl_prep_template.md`,
`srl_peer_feedback_form.md`, `srl_submission_instructions.md`,
`absent_lead_protocol.md`, `instructor_intervention_protocol.md` and their PDFs —
together with `scripts/assign_srl_slots.py` and `scripts/build_srl_packet.py`, and
since **D75** the drawn roster in `_adm/roster/`,
`planning/SRL_ASSIGNMENT_SCHEDULE.md`, and `scripts/nbbuild.py`'s `REPORT_PLAN`
constant behind `INJECT_REPORT_PLAN = False`. The
per-lecture questions guide is kept **in full** and re-owned to the instructor, who
now runs those questions from minute 10. Retiring the category is never permission
to delete an SRL file, an SRL script, or an SRL section.

## Open question carried forward (D74)

With SRL retired, the individual oral **Evidence Defense** carries no grade weight,
and the only graded live performance left in the course is the M15 Expo
presentation — 30% of a 10-point component, so **3 course points**. Whether the
defense should stay ungraded practice, gain weight, or be retired is **not yet
ruled**. Do not resolve it in this file; record the ruling here once Davi makes
it. **D75 does not touch it**, and leaves the other questions carried forward from
D74a open as well: moving the notebook deadline off Sunday, splitting the 10-point
Instructor/TA Evaluation between the M13 poster and the Evidence Defense, and
finishing the D54 propagation.
