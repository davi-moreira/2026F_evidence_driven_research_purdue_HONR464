# PROJECT MILESTONES — HONR 46400 Fall 2026 (v3: M1–M16)

Six students, **individual projects by default** (one group of two or three may
be approved by the instructor before shared work begins), one semester-long
chain: every milestone is a graded, submittable artifact with **kick off →
develop → submit → revise** cadence (D30 retired weekly milestone presentations; the
"Presented / reviewed" moments below are studio work-and-review formats).
**Every milestone is due on a Sunday (D54)**: students work the milestone at
its Friday studio and submit by **Sunday, 11:59 PM**. Three exceptions keep
their weekday deadlines because the conference block depends on them — M11
(due at class Wednesday Nov 4), M12 (Friday Nov 6, 2:30 PM, so peer criticism
reaches authors before the lock), and M13 (Sunday Nov 8, terminal). M13 is
**terminal** — no revision window. Since **D49** the semester runs **one Studio per week**: Monday and Wednesday
teach that Studio's lessons with their "It is your turn" work, and **Friday IS
that Studio's milestone**. Studios 1–12 fall on Weeks 1–12, so course milestone
**M(n) presents book Milestone (n+1)** straight through M16; the four
date-driven weeks (13–16) revisit what the studios already built. **Week 16
teaches Studio 12 but carries no milestone (D54)**: its Friday, Dec 11, is the
course-closing reflection session, collected as a light participation
deliverable rather than a graded milestone. Each course
milestone presents a **book Milestone version** (EDR|AI's Milestones 1–12, D40): the bridge is the
`book_milestones:` block of `planning/COURSE_BOOK_CROSSWALK.yml`, shown in
the last column below. Every milestone updates the
cumulative **Research Project Dossier** and requires an **AI Research Ledger**
entry. Student-facing briefs + rubrics live one file per milestone in
`_research_project/2026Fall/milestone_NN_*.md` (Brightspace replicates from
there); machine anchors in `course_config.yaml milestones:`; validated by
`scripts/validate_milestones.py`. The v1 M01–M23 system is preserved at git
tag `v1-compass-build`; the retired M17 brief is archived under
`_research_project/2026Fall/_retired_d54/`.

**Kickoff cadence.** Every milestone is kicked off from its Brightspace brief
at the opening of a Friday studio's sprint block, developed across Mon/Wed
lectures (project-transfer moments) and the studio sprint, red-teamed by peers
+ an assigned GenAI Studio reviewer role where designated (M5, M8, M9, M13, M16),
and **submitted by the Sunday after that studio, 11:59 PM** (D54). Kickoff
exceptions: M1 (assigned in class on day 1), M16 (packages exchanged at the
Week-13 studio; brief posted with the async module).

Since **D74** the Mon/Wed development moments also include the **ten-minute lab
meeting** that opens each lecture from Week 2, and since **D75** that meeting is
an **open round with nothing assigned**: the instructor asks the room how the
projects are going, and the room answers — what was decided since last time, what
the evidence looks like, where somebody is stuck. It is the
milestone-in-progress said out loud, by whoever has something to say. **No
student is designated to report, on any lecture; there is no slot draw, no
assigned question, and nothing is prepared before class.** Nothing said there is
**graded** — the instructor leads the lesson from minute 10. What *is* collected
from those lectures is the weekly notebook itself, under the separate **Lecture
Notebooks** completion contract (20%, one `nbNN` per week, due the Sunday that
ends the studio week, graded on completion only). A lecture notebook is **not** a
milestone and never enters the M-mean; a milestone is never scored on anything
said in a lab meeting.

*Retired in place.* D74 had populated those ten minutes with a designated
**reporter** — seven minutes on a decision from their own project, three minutes
on the room's questions, prepared in a **📣 My Report Plan** notebook cell. D75
withdrew the designation, the draw and the cell; the drawn roster, both SRL
scripts and the generator's report-plan constant are kept on disk, unapplied, for
a future edition. **No milestone, due date, rubric or weight changed with it** —
the chain below is exactly as D55, D66 and D74 left it.

Meeting numbers `M2…M43` below are MEETINGS (calendar backbone); milestone IDs
are `M1…M16`.

## The chain

| ID | Milestone | Develops (meetings) | Studio work / review | Due | Book Milestone (version) |
|---|---|---|---|---|---|
| M1 | Curiosity committed and the research problem | M1–M3 | curiosity share + 30-sec pitch at the Week-1 studio (M3) | Sun Aug 30, 11:59 PM | 1 — Your curiosity, committed (v1) |
| M2 | Your rules and your question | M4–M6 | working-agreement swap + question declaration (M6) | Mon Sep 7, 11:59 PM | 2 — Your rules and your question (v1) |
| M3 | Verified evidence and contribution map | M7–M8 | contribution-map gallery walk (M8) | Sun Sep 13, 11:59 PM | 3 — Your evidence base (v1) |
| M4 | Research Contract v0 and permission determination | M9–M11 | 3-min contract declaration (M11) | Sun Sep 20, 11:59 PM | 4 — Your research contract, v0 (v1) |
| M5 | Pathway declaration and mandated contrast (Contract v1) | M12–M14 | route jigsaw + pathway defense (M14) | Sun Sep 27, 11:59 PM | 5 — Your pathway, declared (v1) |
| M6 | Data and measurement governance | M14–M17 | provenance clinic + measurement spec review (M17) | Sun Oct 4, 11:59 PM | 6 — Your data and measurement, governed (v1) |
| M7 | First reproducible analysis | M17–M20 | pipeline clinic + conference-application gate (M20) | Tue Oct 13, 11:59 PM | 7 — Your first reproducible analysis (v1) |
| M8 | Robustness audit | M20–M22 | audit walkthrough + adjudication round (M22) | Sun Oct 18, 11:59 PM | 8 — Your robustness audit (v1) |
| M9 | Bounded research note and claim-evidence table | M22–M25 | note red-team + trace-or-cut drill (M25) | Sun Oct 25, 11:59 PM | 9 — Your bounded claims (v1) |
| M10 | Venue contract and the publication-ready artifact | M25–M28 | artifact criticism gallery + defense rehearsal (M28) | Sun Nov 1, 11:59 PM | 10 — Your artifact, ready to publish or present (v1) |
| M11 | Poster first draft | M29–M30 | storyboard + traceability sweep (M29); the draft is due AT CLASS (M30) | Wed Nov 4, at class | 10 (v2, the peer-reviewed draft) |
| M12 | Peer review submission | M30–M31 | silent active-project review circuit (M30) + revision studio (M31) | Fri Nov 6, 2:30 PM | 10 — peer-criticism practice |
| M13 | Final poster lock | M28–M31 | pre-lock gate sweep + print-scale check (M31) | Sun Nov 8, 11:59 PM — TERMINAL | 10 (v3, the locked print edition) |
| M14 | Go-public package: presentation plan and invitation | M32–M34 | pitch drafting (M32) + typed-panel questioning (M33) + rehearsal at the printed board (M34) | Sun Nov 15, 11:59 PM | 10 — spoken-editions practice |
| M15 | Conference reflection | M35–M37 | dress rehearsal (M35); the Expo (Tue Nov 17) supplies the separate Final Project live-presentation score; M15 grades async capture (M36), adjudication (M37), and the written reflection | Sun Nov 29, 11:59 PM | 10 (v4, the publicly presented edition) |
| M16 | Reproducible package and the peer cold run | M38–M40 | cold-run clinic + the in-class package exchange (M39) + the repair block (M40) | Sun Dec 6, 11:59 PM | 11 — Your reproducible package (v1) + 9 (v2) |

## The mentor-meeting cycle (D69)

Two required meetings with the instructor, who is the **faculty mentor of
record** named on every student's Expo application. Calibrated one-to-one
against QM 47400's INSTRUCTOR rounds; HONR 46400 has no TA, so that course's TA
leg is dropped and only the instructor legs remain. Each round is requested in
one milestone and confirmed in a later one, and both are collected inside those
milestones (no new milestone ID — the chain is still M1–M16).

| Round | Meeting window | Requested at | Confirmed at | QM 47400 counterparts |
|---|---|---|---|---|
| Round 01 | Mon Oct 5 – Sun Oct 11 | **M4** (Sun Sep 20) | **M7** (Tue Oct 13) | M00 (Sep 20) → M04 (Oct 11) |
| Round 02 | Mon Nov 2 – Sat Nov 7 | **M8** (Sun Oct 18) | **M14** (Sun Nov 15) | M07 (Oct 18) → M13 (Nov 15) |

Windows and the request/confirm assignment live in `course_config.yaml`
`mentor_meetings:`. The four milestones carry the ✚ schedule mark and a
"What this course adds" section, driven by
`_research_project/milestone_course_additions.yml`. The milestone PDFs may not
print calendar dates, so they point at the course platform; the dated windows
are published in the briefs, in
`_research_project/2026Fall/final_project_grading_and_project_modes.md`, and on
Brightspace.

## Dossier mapping

Each milestone finalizes dossier components (D49, one studio per week):
research charter and committed curiosity (M1), working agreement + declared
question (M2), evidence map (M3), Contract v0 (M4), Contract v1 with the
declared pathway (M5), data + measurement documentation (M6), reproducible
analysis notebook (M7), robustness + diagnostic record (M8), claim–evidence
table + bounded research note (M9), venue contract + publication-ready
artifact (M10), reproducibility package + locked poster (M13), conference
reflection + defense revision (M15), replication record (M16), and research
note v1 + repaired package (M16), which closes the dossier. The **AI Research
Ledger** accumulates across all sixteen. D54 retired the release audit, the
final research chapter, and the AI-management portfolio: they are no longer
dossier components and appear nowhere in student-facing material.

## Notes

- The Expo presentation (Tue Nov 17) is graded only in Final Project's **Poster
  Presentation at the Purdue Undergraduate Research Conference** item (`70%`
  M13 poster quality + `30%` live delivery).
  M15 grades the reflection checkpoint and records proof of participation; there
  is no separate milestone ID for the event itself.
- M16's package exchange is anonymized: each student receives a peer's
  reproducibility package with identifying headers stripped by the instructor.
- Revision policy: all milestones except M13 are revisable within 7
  days of feedback for up to half the lost points. M16 (Sun Dec 6) is the last
  milestone, so its window closes at the end of the term. The policy is restated in
  each revisable brief's **Revision:** line. It has never appeared on the
  syllabus, so the briefs are its only student-facing statement.
  **Open (2026-08-23):** M11, M12, and M14 carry no **Revision:** line, so for
  those three the policy above is stated nowhere a student can read it. All
  three sit inside the conference block, where a 7-day window would run past
  the terminal Sun Nov 8 poster lock or the Tue Nov 17 Expo — so the omission
  may be deliberate. Davi rules whether they are revisable; until he does, do
  not assume either way.
- Hard external anchors: URC abstract internal gate Tue Oct 13 (external
  deadline TBD); poster print submission Sun Nov 8, 11:59 PM; Expo Tue Nov 17.
- Fri Dec 11, the last class, is the course-closing **reflection session**
  (D54). It collects a light reflection deliverable scored under
  **participation**, not as a milestone, and it is not part of the M-mean.
- How these sixteen scores become a grade — the five Final Project components,
  their shares, and how each works in either project mode:
  `_research_project/2026Fall/final_project_grading_and_project_modes.md`
  (student-facing) and `planning/ASSESSMENT_ARCHITECTURE.md` (design).
  **D74 raised the stakes of this chain.** Retiring the 25% Student Research
  Lead category freed five points that are forced inside the Final Project, so
  **Milestone Deliverables rises from 15 to 20 course points** and the **Final
  Project rises from 50% to 55%**. Milestone Deliverables is still the equally
  weighted mean of the M1–M16 milestone scores, no component was renamed, and no
  scoring rule inside a component changed. Because `20 / 55` does not terminate,
  student-facing surfaces now print **course** percentages of the final grade
  rather than project shares: Milestone Deliverables 20% · Peer Evaluation 10% ·
  Peer Review 5% · Poster Presentation at the Purdue Undergraduate Research
  Conference 10% · Instructor/TA Evaluation 10%. The exact project shares
  (36.37 / 18.18 / 9.09 / 18.18 / 18.18) survive only as the machine record in
  `course_config.yaml final_project_breakdown:`.
