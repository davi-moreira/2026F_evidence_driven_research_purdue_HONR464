# INSTRUCTOR IMPLEMENTATION GUIDE — HONR 46400 (Fall 2026, v2)

*How to RUN the course week by week.* This is the operating manual, not the
design rationale. For **why** the course is shaped this way, read
`planning/COURSE_MASTER_PLAN.md` and `_project_docs/DECISIONS.md` (D17–D21 for
the v2 build; **D74** for the current class format, the minute frames and the
weights).
For the machine-readable spine (dates, weights, milestone IDs), read
`course_config.yaml`. On any conflict, dates defer to
`planning/CALENDAR_BACKBONE.csv` and intent defers to the master plan.

The course is a 6-student honors seminar meeting **Mon/Wed/Fri, 50 minutes**,
across **43 meetings** (41 in person + 2 async). Individual projects are the
default; students may form a project group with instructor approval before
shared work begins. Since D74 the instructor's job is to **chair** the ten-minute
lab meeting that opens each Mon/Wed lecture, **lead** the investigation from
minute 10 with accuracy, the AI tooling and the clock in your hands, **run** the
Friday studios, and **grade the chain** on a fast, predictable cadence.

---

## 1. The weekly rhythm

Each day of the week has one fixed job. The 50-minute section frames are
enforced by the session-guide generator and printed in each meeting's guide.

### Monday — lab meeting, then guided investigation (10 / 21 / 12 / 7)

The lecture opens with the ten-minute **lab meeting**; from minute 10 the room is
yours (D74).

- **0–10 — lab meeting.** One student is today's **reporter**: seven minutes on a
  decision their own project has actually reached and the evidence behind it,
  then three minutes of questions from the room. Keep the clock. Do not let the
  report become a lesson on the day's concept, and do not score it. If the
  questions stall, put the first one yourself and hand it straight back to the
  room.
- **10–31 — guided AI investigation.** Yours. Open the 🧩 Research Puzzle, make
  everyone commit an answer in writing before any AI opens, then steer the
  investigation and monitor the AI output for factual errors as it appears.
- **31–43 — human verification + formalization.** Lock down the correct version
  of the concept and connect it to the room's committed answers.
- **43–50 — decision and defense.** Force a defended decision; confirm every
  student records an AI Research Ledger line in the notebook and closes on the
  spoken Claim Ticket.

### Wednesday — lab meeting, then applied AI laboratory (10 / 20 / 12 / 8)

- **0–10 — lab meeting** (the day's reporter, then the room's questions) ·
  **10–30 — retrieval challenge and applied AI laboratory** (yours; open with the
  spoken retrieval drill) · **30–38 — peer defense and adversarial questioning**
  (you keep the questions coming and the answers honest) · **38–42 — synthesis +
  accuracy lock (D34):** the room states its conclusion and its uncertainty, and
  you correct any claim that survived challenge but is wrong BEFORE it can enter
  a ledger — Wednesday's consolidation moment · **42–50 — transfer to projects**,
  closing with a ledger line and Claim Ticket.

Both frames still sum to 50, and section boundaries 3 and 4 are unchanged
(31–43 / 43–50 Monday, 30–42 / 42–50 Wednesday), so D22's and D34's rulings on
those blocks stand exactly as before.

### Friday — project studio (you run it)

**No new topic content, ever.** The studio opens with the stand-up and is a working
session for the week's milestone (D22/D30, amended D58):

- **0–5 — research stand-up.** Each student states last week's decision and
  this week's blocker.
- **5–45 — milestone kickoff + AI-supported work.** Present the week's
  milestone from its Brightspace brief (about 3 minutes), then students WORK ON
  the milestone with their AI assistant while you run rotating consults. The
  old peer red-team block is retired (D30); at designated milestones an
  assigned GenAI Studio reviewer role is still required (see §5).
- **45–50 — revise, update ledger + dossier, submit.** The milestone is
  submitted at close.

**Nothing is printed and nothing is scored for Friday.** D58 retired the weekly
quiz category and its 0–10 class-time block for this edition, and the sprint
absorbed those ten minutes. The banks in `_quizzes/2026Fall/weekly/` and the
`scripts/audit_answer_length.py` gate are kept for a future edition; never delete
them, and do not print or grade anything from them this term.

**Week 1 is instructor-led** (both lectures) and carries no reporter; it models
the format before the lab meetings begin in Week 2.

### The async module

Two meetings are asynchronous online (the calendar backbone is authoritative):

- **Fri Nov 20 (meeting 36)** — post-Expo audience-data capture.
- **Mon Nov 23 (meeting 37)** — the Thanksgiving replication + red-team module
  (M16).

Fri Oct 2 (meeting 17) is a **regular in-person studio** on the standard
5/40/5 frame; M6 is submitted there like any other milestone.

**No class Wed Nov 18**, the day after the Expo.

---

## 2. The lab meeting pipeline (D74)

**Assign the reporter slots first — randomly.** There are **25 reporting
lectures** (all Mon/Wed except Week 1's two launch meetings) and 6 students, so
**each student reports 4 or 5 times** — 25 does not divide by 6, and which
student carries the extra slot was drawn with the rest of the assignment. Nothing
about the report is scored, so an uneven count cannot affect a grade. **D74
carries the D69/D71 draw over unchanged: no re-draw.** Slot 1 is **meeting 4
(Mon Aug 31**, nb02 Lecture 1). The slot-to-meeting mapping and the
Monday/Wednesday format live in the schedule data
(`scripts/schedule_data/part1–4.py`, in the fields whose keys are still
`srl_slot` + `srl_focus` for machine continuity) and surface on the public
**Schedule** page; students read their dates there.

**What the reporter brings.** Seven minutes on a decision **their own project**
has actually reached since the last lab meeting, the evidence behind it, and the
part they are still unsure about; then three minutes of questions from the room.
They are the only person present who has been inside that project, so there is no
concept they can get wrong in front of peers. This is also the rehearsal for the
poster conversation the Expo grades in November.

**The cadence** (per reporter):

1. **Before class** — the reporter fills lines 1–4 of the student-visible
   `### 📣 My Report Plan` cell that sits beside the `### 📣 Lab Meeting:
   Today's Reporter` brief opening their lecture (right after `# Lecture N`).
   Everyone else fills line 5, so the whole room arrives with a question. There
   is no day-before preparation submission and no overnight review to return:
   both retired with the role, and the notebook itself is collected at the end of
   the week (§3).
2. **Day of** — you chair the ten minutes and keep the clock, then lead from
   minute 10 (§1) and on Wednesdays run the 38–42 accuracy lock.

**Nothing to grade live.** The report carries no score. What is collected is the
**weekly lecture notebook**, from every student, on completion (§3). Say this out
loud in Week 1 and again at the first lab meeting: the fear this format was
designed to remove comes back the moment the room suspects the report is being
marked.

**The questions guide is yours now.** Each lecture's three questions live in the
notebook's `### 🔎 Questions to Keep You Thinking` cell, every one of them kept
verbatim from the earlier design, each with its `Ask after:` moment and its
listen-for hint. Open each item only when its moment is reached.

**Retired in place — delete nothing (D74 Ruling 5).** The Student Research Lead
grade category and the live nine-row rubric are **not applied this edition**, and
no SRL file is removed. `project/srl/` (handbook, rubric, Socratic question bank,
AI integration guide, prep template, peer feedback form, submission instructions,
absent-lead and instructor-intervention protocols), `scripts/assign_srl_slots.py`
and `scripts/build_srl_packet.py` all stay on disk for a future edition, exactly
as D58 kept the quiz banks. The rubric's nine criteria (conceptual correctness,
quality of Socratic questions, exposing assumptions, productive use of AI,
interrogating AI output, inclusion of classmates, time management, connection to
research decisions, and handling incorrect or uncertain answers) and the
classmate feedback form (`project/srl/srl_peer_feedback_form.md`) are intact on
disk for whoever brings the role back. Do not score anything on
`project/srl/srl_rubric.md` this term. The intervention protocol in
`project/srl/srl_handbook.md` ("How the instructor will step in") still reads
usefully for the moments a peer discussion needs a hand, but the room is yours
from minute 10 and needs no handing back.

---

## 3. Milestone grading cadence

Sixteen milestones (**M1–M16**), one graded artifact each, on a **studio
kickoff → develop → work it at the Friday studio → submit Sunday → revise where
eligible** cadence. D55 put every deadline on a Sunday at 11:59 PM except the
three the conference block pins to weekdays and the two D66 moved off a holiday
weekend. Due dates are fixed in `course_config.yaml milestones:`:

| M1 Sun Aug 30 · **M2 Mon Sep 7 (Labor Day)** · M3 Sun Sep 13 · M4 Sun Sep 20 ·
M5 Sun Sep 27 · M6 Sun Oct 4 · **M7 Tue Oct 13 (October Break)** ·
M8 Sun Oct 18 · M9 Sun Oct 25 · M10 Sun Nov 1 ·
**M11 Wed Nov 4 (at class)** · **M12 Fri Nov 6, 2:30 PM** ·
**M13 Sun Nov 8, 11:59 PM (terminal)** · M14 Sun Nov 15 ·
M15 Sun Nov 29 (async) · M16 Sun Dec 6 (the final milestone) |

There is no M17: D54 retired it. The last Friday, Dec 11, is the course-closing
reflection session, collected under participation.

- **Return feedback within 3 days** of each milestone.
- **Revision window: 7 days** from feedback, for up to half the lost points, on
  every milestone **except the terminal one** (M13). The live Expo
  presentation is separately terminal inside Final Project's Poster
  Presentation at the Purdue Undergraduate Research Conference item. For those
  terminal scores, the deadline governs.
- Every submission must append an **AI Research Ledger** entry (8 fields) and
  update the cumulative **Research Project Dossier**. A missing ledger entry
  scores the affected student's individual Craft/ledger row specified in the
  milestone brief 0 and that submission is **returned**. Do not change a
  separate shared terminal-rubric score unless its rubric says to do so.
- Rubrics share a fixed criteria menu (compass alignment, evidence integrity,
  verification, uncertainty + limitations, craft). Confirmed weights live in
  `course_config.yaml assessment:`.

The course has five weighted categories totaling 100 (D74):

| Category | Weight |
|---|---:|
| Attendance | 1 |
| Participation | 9 |
| IYT Practice | 15 |
| Lecture Notebooks | 20 |
| Final Project | 55 |
| **Total** | **100** |

D74 retired the 25% Student Research Lead category and replaced it with **Lecture
Notebooks 20%**; the 5 points that could not fit went to Milestone Deliverables
inside the Final Project, which rose from 50% to 55%. D58 retired the quiz
category for this edition, so nothing in the gradebook is scored on a quiz.

Three of the five categories are **undivided completion contracts** with the same
credit rule (`1.0` on time, `0.5` within seven days, `0` otherwise) and the same
automatic drop of the lowest `⌈0.10 × N⌉` credits. They are separate instruments
with separate credit pools; never merge them, and never publish an internal split
of any of them.

**Participation is one undivided 9% block (D57, amended D58)**: every required
item is one equal credit, graded for completion — the 12 per-studio feedback
surveys (each Sunday that ends a studio week), the student profile survey
(Aug 30) and the course reflection (Dec 11). Baseline **N = 14**, drop **d = 2**,
so the block is `9.0 × (sum of the highest 12 credits) / 12`. Its ±0.9-point
contribution adjustment belongs to this block alone. The contract is
`surveys/participation_grading.md`; the dated assignment list is
`planning/STUDIO_FEEDBACK_SCHEDULE.md`.

**IYT Practice is its own 15% block (D58, amended D61)**: the book's "It is your turn" section
for each required chapter, due 11:59 PM on that chapter's reading day, graded for
completion on the same credit rule. Baseline **N = 35** (36 when the declared
design has stages), drop **d = 4**, so the block is
`15.0 × (sum of the highest 31 credits) / 31`. The dated assignment list
is `planning/IYT_SUBMISSION_SCHEDULE.md`; the contract is the same
`surveys/participation_grading.md`.

**Lecture Notebooks is its own 20% block (D74)** — the course's third undivided
completion contract, and what replaced the live SRL score. Each student submits
**the week's notebook `nbNN`, worked in class**, one per week, due **11:59 PM on
the Sunday that ends the studio week** (Week 16 closes **Fri Dec 11**, the last
class day). Baseline **N = 16**, drop **d = 2**, so the block is
`20.0 × (sum of the highest 14 credits) / 14`.

- Grade it on **completion only**: worked through and handed in. Never on whether
  the answers came out right, and never on how that student's live report went.
  Open the file, confirm the week's writing cells carry the student's own work
  (the 📣 report-plan lines, the seven in-class moves, the 📒 ledger row per
  lecture), enter the credit, and move on. It is not a second milestone.
- Nothing below a lecture's `### ⏸` line, and nothing behind a 🏠 label, counts
  toward the credit; that material is optional depth.
- It is **not participation** and never carries participation's ±0.9 contribution
  adjustment. D57's ban stands in its amended form: lecture-notebook completion
  may never come back **as a participation item**.
- Machine spine: `course_config.yaml lecture_notebooks:`. Dated list:
  `planning/LECTURE_NOTEBOOK_SCHEDULE.md` (generated).
- The milestone studio notebooks (`msNN`) are not part of this block; they arrive
  with their milestone.

**Final Project (55%)** contains **Milestone Deliverables · Peer Evaluation ·
Peer Review · Poster Presentation at the Purdue Undergraduate Research
Conference · Instructor/TA Evaluation**, worth **20 / 10 / 5 / 10 / 10** course
points. D74 gave Milestone Deliverables the five points freed by retiring the SRL
category, so student-facing surfaces now print those **course percentages** of
the final grade rather than shares of the project (20/55 does not terminate);
`course_config.yaml` keeps the exact project shares
36.37 / 18.18 / 9.09 / 18.18 / 18.18 as the machine record. No component was
renamed and no scoring rule inside a component changed. The syllabus states only
those five names and their weights. The "comprehensive set of project
guidelines" it promises is the student-facing
`_research_project/2026Fall/final_project_grading_and_project_modes.md` — paste
it into Brightspace and grade from it. Its gradebook implementation is
`brightspace/gradebook_spec.md` (generated by
`scripts/build_brightspace_kit.py`), and the design reconciliation is
`planning/ASSESSMENT_ARCHITECTURE.md`.

**Project-mode setup.** Record the approved group before shared work begins.
With six students, approve at most one group of two or three, and do so only
when at least three active projects remain and the roster
supports two observers per individual researcher plus a nonempty evaluation
submission set for every student.
For every student, record a received-rating set and a nonempty submission set.
An individual researcher's received-rating set is two assigned project peers
who observe studios, milestone checks, reproduction work, and defenses; their
submission set is the peer or peers they are assigned to observe, normally two.
A group member is rated by every teammate and rates every teammate, and may also
be assigned to observe an individual researcher. The two sets need not be
reciprocal. Do not mix Peer Evaluation with M12 Peer Review. Use
`project/final_dossier/peer_evaluation_instrument.md` for the confidential form,
rating conversion, missing-rating rule, and moderation record.

**Gradebook operation.** Milestone Deliverables is the equal-weight mean of the
sixteen M1–M16 scores. An approved group submits one shared artifact naming
every member. Enter shared rubric-row scores in common and score requirements
marked individual per student; a milestone score may differ only on those
individual rows. Every student still completes Peer Review and presents live. A
group shares the poster-quality score and the instructor's evaluation of the
locked poster; live delivery and Peer Evaluation remain individual.

---

## 4. The milestone brief → Brightspace loop

Milestone briefs and rubrics are authored **one file per milestone** in
`_research_project/2026Fall/milestone_NN_<slug>.md` and are written to be
**copy-paste-ready into Brightspace** (one Brightspace page per milestone). Each
Friday, present the week's brief from Brightspace at the studio kickoff.

The active **M1–M16** briefs are in place. Machine anchors and due dates are
validated by `scripts/validate_milestones.py`.

---

## 5. GenAI Studio setup — DO THIS BEFORE THE SEMESTER

Purdue GenAI Studio (<https://genai.rcac.purdue.edu>) is the course's reviewer
bench. Students **must** consult an assigned reviewer role at five milestones:

| Milestone | Required reviewer role |
|---|---|
| M5  | Causal Identification Skeptic (route declaration) |
| M8  | Prediction & Leakage Auditor |
| M9  | Robustness & Sensitivity Reviewer |
| M13 | Poster Critic (before the lock) |
| M16 | Reproducibility Auditor |

Before the first class:

1. **Create the course group** in GenAI Studio and enroll the six students.
2. **Build the reviewer-role custom models** — the 13 role definitions
   (base model + system prompt) ship in `genai_studio/roles/`.
3. **Upload the course knowledge base** to the RAG-backed roles.
4. **Verify student access** to the group and the models (student API access is
   unverified; the manual-UI path is first-class and must work).

> **Build note:** the `genai_studio/` directory (roles, KB strategy, Colab PoC,
> and the step-by-step `genai_studio/instructor_setup_guide.md`) is being
> produced by a separate workstream and is **not yet in the repo**. Do the setup
> from that guide once it lands; until then this section is the checklist.
> GenAI Studio is used only at capability levels 1–4 (prompted role → custom
> model → RAG assistant → sequential workflow); it has no native agents and
> materials never claim otherwise.

---

## 6. The Expo logistics chain

Three hard anchors drive November. Miss the first and the print deadline slips;
miss the print deadline and there is no poster to present.

1. **Abstract gate — Fri Oct 9 (M7).** Internal completion gate for the URC
   abstract (the external URC deadline is TBD; confirm and post it as soon as it
   publishes). Run the abstract workshop in the M7 studio.
2. **Poster lock + print submission — Sun Nov 8, 11:59 PM (M13, terminal).** The
   poster is locked and submitted for printing. No changes after this time.
   Confirm the print vendor turnaround well before this date.
3. **URC Expo — Tue Nov 17.** Required. Live presentation quality supplies 30%
   of Final Project's Poster Presentation at the Purdue Undergraduate Research
   Conference item; M13 poster quality
   supplies the other 70%. M15 grades the written reflection, not live quality. Each student
   presents their poster and **evaluates at least three other conference
   posters** on the course criticism instrument. **No class Wed Nov 18.** Only a documented
   emergency qualifies for a make-up, handled individually per Honors College
   norms.

Weeks 11–13 (`nb11`–`nb13`) rehearse the presentation: poster criticism, pitch
delivery under uncertainty, and fielding hard questions
(`project/conference/` holds the presentation, hard-questions,
uncertainty-limitations, dress-rehearsal, and reflection protocols).

---

## 7. The M16 peer cold run

The peer cold run takes place in class during Week 15 and feeds M16. Run the
exchange as follows:

1. Each student brings a **reproducibility package** (clean-run Colab notebook +
   data or access recipe + environment record + README, SEED = 464).
2. On the Week-15 Wednesday, colleagues exchange packages and run each other's
   capsule from the written instructions alone while the author remains silent.
3. Each runner records whether the headline result and its uncertainty reproduce,
   every question the instructions forced them to ask, and every mismatch.
4. Friday is the repair and submission block for M16. M16 is one of the sixteen
   scores in Final Project's Milestone Deliverables item and supplies evidence
   for the final artifact, portfolio, and defense evaluated in Instructor/TA
   Evaluation; there is no separate replication category.

---

## 8. The defense schedule and end of term

- **Evidence Defenses — the Week 15–16 Wednesday defense blocks.** Each student
  delivers an oral **Evidence Defense** of the whole project and their AI
  collaboration. Under D54 this is **in-class practice with no grade weight**:
  Instructor/TA Evaluation is now the instructor's evaluation of the M13 final
  poster submission. Davi has not yet ruled whether the defense should stay
  ungraded, be folded into a component, or be retired. D74 sharpened the
  question: with the SRL score gone, the only graded live performance left in
  the course is the M15 Expo presentation, worth 30% of a 10-point component,
  which is **3 course points**.
- **Fri Dec 11 — the course-closing reflection session.** No milestone is
  collected. The reflection is written in the room and submitted by 11:59 PM,
  scored under **Participation** as one credit; Studio 12's feedback survey
  closes the same night.
- **End-of-term wrap:**
  1. Grade M16, the reflection and the Week-16 lecture notebook (the last
     Lecture Notebooks credit, due Fri Dec 11), and enter the Instructor/TA
     Evaluation score from the locked M13 poster.
  2. **Archive the course:** confirm the site is rendered and pushed
     (`quarto render` → commit `docs/` → push), the instructor material is synced
     to the private repo (`scripts/sync_instructor_repo.sh`), and the v2 build
     state is recorded.
  3. **Analyze the course evaluations** once the Purdue/DSB PDFs arrive:
     `.venv/bin/python scripts/analyze_course_eval.py <folder-of-eval-PDFs>`
     produces a single quantitative + qualitative report.

---

## Quick reference — where things live

| Need | Path |
|---|---|
| Dates (authoritative) | `planning/CALENDAR_BACKBONE.csv` |
| Weights, milestone IDs, AI policy | `course_config.yaml` |
| Milestone chain + cadence | `planning/PROJECT_MILESTONES.md` |
| Milestone briefs (Brightspace source) | `_research_project/2026Fall/milestone_NN_*.md` |
| Final Project grading + project modes | `_research_project/2026Fall/final_project_grading_and_project_modes.md` |
| Brightspace gradebook (generated) | `brightspace/gradebook_spec.md` |
| Lecture Notebooks contract + schedule | `course_config.yaml lecture_notebooks:`, `planning/LECTURE_NOTEBOOK_SCHEDULE.md` |
| SRL suite (retired this edition, kept on disk) | `project/srl/`, `scripts/assign_srl_slots.py`, `scripts/build_srl_packet.py` |
| Session guides (generated) | `scripts/build_session_guides.py` → `session_guides/` |
| Schedule data (reporter slots, in the `srl_*` fields) | `scripts/schedule_data/part1–4.py` |
| GenAI Studio roles + setup | `genai_studio/` *(forthcoming)* |
| Conference/presentation protocols | `project/conference/` |
| Course-eval analysis | `scripts/analyze_course_eval.py` |
| Design rationale | `planning/COURSE_MASTER_PLAN.md`, `_project_docs/DECISIONS.md` |
