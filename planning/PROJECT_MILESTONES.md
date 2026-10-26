# PROJECT MILESTONES — HONR 46400 Fall 2026 (v4: M1–M17, D91)

Four students, **individual projects by default** (one group of two may
be approved by the instructor before shared work begins), one semester-long
chain: every milestone is a graded, submittable artifact with **kick off →
develop → submit → revise** cadence (D30 retired weekly milestone presentations; the
"Presented / reviewed" moments below are studio work-and-review formats).
**Every milestone is due on a Sunday (D54)**: students work the milestone at
its Friday studio and submit by **Sunday, 11:59 PM**. **D91 (2026-10-26) rebuilt
the conference block on QM 47400's post-lock sequence**, so its deadlines follow
the Expo rather than the Sunday rule: M11, the final poster and the print file
(Sun Nov 8, **terminal**, no revision window), M12 presentation planning (Wed Nov
11), M13 peer review (Thu Nov 12; the questions are asked at the Fri Nov 13
practice presentations), M14 the LinkedIn invitation (Sun Nov 15), M15 the Expo
presentation confirmation (Tue Nov 17), and M16 the conference reflection (the
two asynchronous sessions after the Expo, due Mon Nov 23). Since **D49** the semester runs **one Studio per week**: Monday and Wednesday
teach that Studio's lessons with their "It is your turn" work, and **Friday IS
that Studio's milestone**. Studios 1–12 fall on Weeks 1–12, so course milestone
**M(n) presents book Milestone (n)** for n = 1..10 (D50), the conference block
(M11–M16) revisits and practises Book Milestone 10, and **M17 presents Book
Milestone 11** on Week 15. **Week 16
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
tag `v1-compass-build`; the D54 M17 brief (release audit) is archived under
`_research_project/2026Fall/_retired_d54/`, and the five D50/D90 conference-block
briefs D91 replaced under `_research_project/2026Fall/_retired_d91/`.

**Kickoff cadence.** Every milestone is kicked off from its Brightspace brief
at the opening of a Friday studio's sprint block, developed across Mon/Wed
lectures (project-transfer moments) and the studio sprint, red-teamed by peers
+ an assigned GenAI Studio reviewer role where designated (M5, M8, M9, M11, M17),
and **submitted by the Sunday after that studio, 11:59 PM** (D54). Kickoff
exceptions: M1 (assigned in class on day 1) and the conference block M11–M16
(D91), whose deadlines follow the Expo; M17's packages are exchanged in the
Week-15 Wednesday class.

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
are `M1…M17`.

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
| M11 | Final poster (the print file) | M29–M31 | production lab (M29) + ungraded reading round of the near-final posters (M30) + revision studio and print-scale check (M31); graded with the poster rubric (D90) | Sun Nov 8, 11:59 PM — TERMINAL | 10 (v2, the final poster, printed; course-only instructions) |
| M12 | Presentation planning: audience, pitches, and questions | M32–M33 | pitch drafting (M32) + typed-panel questioning (M33) | Wed Nov 11, 11:59 PM | 10 — spoken-editions practice |
| M13 | Peer review | M33 | feedback and questions for every other poster, from the shared folder (opens M33); questions asked at the practice presentations (M34) | Thu Nov 12, 11:59 PM | 10 — peer-criticism practice |
| M14 | LinkedIn invitation | M34 | practice presentations at the printed board (M34) + the invitation kickoff | Sun Nov 15, 11:59 PM | 10 — the public invitation |
| M15 | Expo presentation confirmation | M35 | dress rehearsal (M35); the Expo (Tue Nov 17) — photo in front of the poster; the live presentation is scored there | Tue Nov 17, 11:59 PM | 10 (v3, the publicly presented edition) |
| M16 | Conference reflection: the audience and the plan for the research | M36–M37 | async survey (M36) + async plan (M37) | Mon Nov 23, 11:59 PM | 10 (v4, what the room returned) |
| M17 | Reproducible package and the peer cold run | M38–M40 | solo cold run (M38) + the in-class package exchange (M39) + the repair block, two blocking gates and second clean run (M40) | Sun Dec 6, 11:59 PM | 11 — Your reproducible package (v1) |

## The mentor-meeting cycle (D69)

Two required meetings with the instructor, who is the **faculty mentor of
record** named on every student's Expo application. Calibrated one-to-one
against QM 47400's INSTRUCTOR rounds; HONR 46400 has no TA, so that course's TA
leg is dropped and only the instructor legs remain. Each round is requested in
one milestone and confirmed in a later one, and both are collected inside those
milestones (no new milestone ID — the chain is M1–M17).

| Round | Meeting window | Requested at | Confirmed at | QM 47400 counterparts |
|---|---|---|---|---|
| Round 01 | Mon Oct 5 – Sun Oct 11 | **M4** (Sun Sep 20) | **M7** (Tue Oct 13) | M00 (Sep 20) → M04 (Oct 11) |
| Round 02 | Mon Nov 2 – Sat Nov 7 | **M8** (Sun Oct 18) | **M12** (Wed Nov 11; D91) | M07 (Oct 18) → M13 (Nov 15) |

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
artifact (M10), the final poster (M11), the presentation plan (M12), the
conference reflection and the plan for the research (M16), and the repaired
reproducible package with its cold-run and gate records (M17), which closes the
dossier. The **AI Research Ledger** accumulates across all seventeen. D54 retired the release audit, the
final research chapter, and the AI-management portfolio: they are no longer
dossier components and appear nowhere in student-facing material.

## Notes

- The Expo presentation (Tue Nov 17) is graded only in Final Project's **Poster
  Presentation at the Purdue Undergraduate Research Conference** item (`70%`
  the M11 final poster's poster-rubric score + `30%` live delivery, scored at the
  Expo with the rubric in the M15 brief). M15 records proof of presentation (the
  photo, graded on completion); the live score is not the M15 milestone score.
- M17's package exchange is anonymized: each student receives a peer's
  reproducibility package with identifying headers stripped by the instructor.
- Revision policy: all milestones are revisable within 7 days of feedback for up
  to half the lost points EXCEPT M11 (terminal, the print file) and the
  completion-graded M14 and M15 (D91). M17 (Sun Dec 6) is the last milestone, so
  its window closes at the end of the term. The policy is restated in each
  revisable brief's **Revision:** line; M12, M13 and M16 now carry one.
- Carry-forward record (D80/D82): applies from M4 on except the conference block
  M12–M16 (D91), whose one-to-three-day cadence makes the 48-hour rule unmeetable;
  numbered requests issued in those weeks are answered at M17.
- Hard external anchors: URC abstract draft in M6 (Sun Oct 4) and the final
  abstract + Expo application in M7 (Tue Oct 13), D84 (Expo deadline Wed Oct 14, 11:59 PM, via OURConnect; D85); poster print submission Sun Nov 8, 11:59 PM; Expo Tue Nov 17.
- Fri Dec 11, the last class, is the course-closing **reflection session**
  (D54). It collects a light reflection deliverable scored under
  **participation**, not as a milestone, and it is not part of the M-mean.
- How these seventeen scores become a grade — the five Final Project components,
  their shares, and how each works in either project mode:
  `_research_project/2026Fall/final_project_grading_and_project_modes.md`
  (student-facing) and `planning/ASSESSMENT_ARCHITECTURE.md` (design).
  **D74 raised the stakes of this chain, and D79 raised them again.** Retiring
  the 25% Student Research Lead category freed 25 points. D74 put 20 in a new
  Lecture Notebooks contract and forced 5 inside the Final Project; **D79
  (2026-09-04) retired that contract too**, so all 25 sit inside the project and
  **Milestone Deliverables rises from 15 to 33 course points** while the **Final
  Project rises from 50% to 75%**. The weight went mostly here because it came
  off weekly collected work, and M1–M16 is the weekly deliverable chain that
  remains. Milestone Deliverables is still the equally
  weighted mean of the milestone scores (M1–M16 then, M1–M17 since D91), no component was renamed, and no
  scoring rule inside a component changed.
  Student-facing surfaces print **course** percentages of the final grade
  rather than project shares: Milestone Deliverables 33% · Peer Evaluation 12% ·
  Peer Review 6% · Poster Presentation at the Purdue Undergraduate Research
  Conference 12% · Instructor/TA Evaluation 12%. The project shares
  (44 / 16 / 8 / 16 / 16) survive only as the machine record in
  `course_config.yaml final_project_breakdown:`.
