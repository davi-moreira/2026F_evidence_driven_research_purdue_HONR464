# INSTRUCTOR IMPLEMENTATION GUIDE — HONR 46400 (Fall 2026, v2)

*How to RUN the course week by week.* This is the operating manual, not the
design rationale. For **why** the course is shaped this way, read
`planning/COURSE_MASTER_PLAN.md` and `_project_docs/DECISIONS.md` (D17–D21).
For the machine-readable spine (dates, weights, milestone IDs), read
`course_config.yaml`. On any conflict, dates defer to
`planning/CALENDAR_BACKBONE.csv` and intent defers to the master plan.

The course is a 5-student honors seminar meeting **Mon/Wed/Fri, 50 minutes**,
across **43 meetings** (42 in person + 1 async). Individual projects are the
default; students may form a project group with instructor approval before
shared work begins. The instructor's job is not to lecture; it is to **monitor
and formalize** student-led lectures, **run** the Friday studios, and **grade the
chain** on a fast, predictable cadence.

---

## 1. The weekly rhythm

Each day of the week has one fixed job. The 50-minute section frames are
enforced by the session-guide generator and printed in each meeting's guide.

### Monday — student-led guided investigation

The **Student Research Lead (SRL)** owns the room; the instructor is the accuracy
monitor and the formalizer.

- **0–9 — student-led research puzzle.** Watch, do not intervene. Let prior
  beliefs surface and the room commit in writing before any AI opens.
- **9–31 — guided AI investigation.** Monitor the AI output in the background
  for factual errors. If a conceptual error starts to spread, flag it *without
  taking the room* from the lead. If an AI failure passes unnoticed, ask the
  lead to put it to the room rather than answering directly.
- **31–43 — human verification + formalization.** This block is **yours**. Lock
  down the correct version of the concept and connect it to the room's committed
  answers.
- **43–50 — decision and defense.** Hand back to the lead to force a defended
  decision; confirm the class records an AI Research Ledger line and a Claim
  Ticket.

### Wednesday — applied AI laboratory

The SRL runs a retrieval challenge and a hands-on lab; the instructor referees
the peer defense.

- **0–7 — retrieval and challenge** (lead) · **7–30 — applied AI laboratory**
  (lead) · **30–38 — peer defense and adversarial questioning** (you keep the
  questions coming and the answers honest) · **38–42 — SRL synthesis + your
  accuracy lock (D34):** the lead states the room's conclusion and its
  uncertainty, and you correct any claim that survived challenge but is wrong
  BEFORE it can enter a ledger — Wednesday's consolidation moment ·
  **42–50 — transfer to projects** (lead), closing with a ledger line and
  Claim Ticket.

### Friday — project studio (you run it)

**No new topic content, ever.** The studio is quiz-first (D22/D30):

- **0–10 — weekly topic quiz.** Five printed multiple-choice questions on the
  week's topic (`_quizzes/2026Fall/weekly/`), answered solo, closed notes,
  handed in.
- **10–15 — research stand-up.** Each student states last week's decision and
  this week's blocker.
- **15–45 — milestone kickoff + AI-supported work.** Present the week's
  milestone from its Brightspace brief (about 3 minutes), then students WORK ON
  the milestone with their AI assistant while you run rotating consults. The
  old peer red-team block is retired (D30); at designated milestones an
  assigned GenAI Studio reviewer role is still required (see §5).
- **45–50 — revise, update ledger + dossier, submit.** The milestone is
  submitted at close.

**Week 1 is instructor-led** (both lectures) to model the SRL format before
students take over in Week 2.

### The async module

One meeting is asynchronous online, a self-contained graded unit:

- **Mon Nov 23 (meeting 37)** — the Thanksgiving replication + red-team module
  (M16).

Fri Oct 2 (meeting 17) is a **regular in-person studio** on the standard
10/5/30/5 frame; M6 is submitted there like any other milestone.

**No class Wed Nov 18**, the day after the Expo.

---

## 2. The Student Research Lead (SRL) pipeline

**Assign the slots first — randomly (D22).** There are **25 leadable
lectures** (all Mon/Wed except Week 1's two launch meetings) and 5 students,
so **each student leads 5 times**. Slots are **randomly assigned at the start
of the semester** — no rotation, no seats. Slot 1 is **meeting 4 (Mon Aug
31**, nb02 Lecture 1). The slot-to-meeting mapping and Monday/Wednesday format
live in the schedule data (`scripts/schedule_data/part1–4.py`, fields
`srl_slot` + `srl_focus`) and surface on the public **Schedule** page;
students read their dates there.

**The handoff timeline** (per lead):

1. **1 week ahead** — the lead preps from the student-visible `### 🎤 SRL
   Lead Brief` cell that opens their lecture in that week's notebook (right
   after `# Lecture N`): the concept in play, the run of show, and explicit
   room for the lead's own staging.
2. **2 days ahead** — the lead submits the preparation script
   (`project/srl/srl_prep_template.md`). **Review it and send notes.** This
   review is the difference between a session that lands and one that stalls.
3. **Day of** — the lead runs the room; you monitor, formalize (§1), and on
   Wednesdays run the 38–42 accuracy lock.

**Grade it live.** Score each lead on `project/srl/srl_rubric.md` during or
immediately after the session (conceptual correctness, Socratic quality,
assumption exposure, productive + interrogated AI use, inclusion, time
management, connection to research decisions, handling uncertainty). Collect
classmate feedback on `project/srl/srl_peer_feedback_form.md` and pass it to the
lead quickly; it is the fastest way they improve before the next slot. The
Student Research Lead component is **20%** of the course grade (syllabus).

**Intervention protocol.** How to step in without seizing the room is summarized
in `project/srl/srl_handbook.md` ("How the instructor will step in"); the
student-facing philosophy, the ten SRL moves, and the AI-integration guidance
are in the rest of the SRL suite (`project/srl/`).

---

## 3. Milestone grading cadence

Sixteen milestones (**M1–M16**), one graded artifact each, on a **studio
kickoff → develop → work it at the Friday studio → submit Sunday → revise where
eligible** cadence. D55 put every deadline on a Sunday at 11:59 PM except the
three the conference block pins to weekdays. Due dates are fixed in
`course_config.yaml milestones:`:

| M1 Sun Aug 30 · M2 Sun Sep 6 · M3 Sun Sep 13 · M4 Sun Sep 20 · M5 Sun Sep 27 ·
M6 Sun Oct 4 · M7 Sun Oct 11 · M8 Sun Oct 18 · M9 Sun Oct 25 · M10 Sun Nov 1 ·
**M11 Wed Nov 4 (at class)** · **M12 Fri Nov 6, 5:00 PM** ·
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

The course has five weighted categories totaling 100: Attendance 1 ·
Participation 9 · Quizzes 20 · SRL 20 · Final Project 50.
**Participation is one undivided block (D57)**: every required item is one equal
credit, graded for completion — the book's "It is your turn" section for each
required chapter (due 11:59 PM on that chapter's reading day), the 12 per-studio
feedback surveys (each Sunday that ends a studio week), the student profile
survey (Aug 30) and the course reflection (Dec 11). Lecture notebooks are never
collected. The contract is `surveys/participation_grading.md`; the dated
assignment lists are `planning/IYT_SUBMISSION_SCHEDULE.md` and
`planning/STUDIO_FEEDBACK_SCHEDULE.md`. Final
Project contains **Milestone Deliverables 30% · Peer Evaluation 20% · Peer
Review 10% · Poster Presentation at the Purdue Undergraduate Research
Conference 20% · Instructor/TA Evaluation 20%**, worth 15/10/5/10/10 course
points. The syllabus states only those weights and the five component
descriptions. The "comprehensive set of project guidelines" it promises is the
student-facing
`_research_project/2026Fall/final_project_grading_and_project_modes.md` — paste
it into Brightspace and grade from it. Its gradebook implementation is
`brightspace/gradebook_spec.md` (generated by
`scripts/build_brightspace_kit.py`), and the design reconciliation is
`planning/ASSESSMENT_ARCHITECTURE.md`.

**Project-mode setup.** Record the approved group before shared work begins.
With five students, approve at most one group of two or three, and do so only
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
bench. Students **must** consult an assigned reviewer role at four milestones:

| Milestone | Required reviewer role |
|---|---|
| M5  | Causal Identification Skeptic (route declaration) |
| M8  | Prediction & Leakage Auditor |
| M9  | Robustness & Sensitivity Reviewer |
| M13 | Poster Critic (before the lock) |
| M16 | Reproducibility Auditor |

Before the first class:

1. **Create the course group** in GenAI Studio and enroll the five students.
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
4. Friday is the repair and submission block for M16. M16 is one of the seventeen
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
  ungraded, be folded into a component, or be retired.
- **Fri Dec 11 — the course-closing reflection session.** No milestone is
  collected. The reflection is written in the room and submitted by 11:59 PM,
  scored under **Participation** as one credit; Studio 12's feedback survey
  closes the same night.
- **End-of-term wrap:**
  1. Grade M16 and the reflection, and enter the Instructor/TA Evaluation score
     from the locked M13 poster.
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
| SRL handbook, template, rubric | `project/srl/` |
| Session guides (generated) | `scripts/build_session_guides.py` → `session_guides/` |
| Schedule data (SRL slots) | `scripts/schedule_data/part1–4.py` |
| GenAI Studio roles + setup | `genai_studio/` *(forthcoming)* |
| Conference/presentation protocols | `project/conference/` |
| Course-eval analysis | `scripts/analyze_course_eval.py` |
| Design rationale | `planning/COURSE_MASTER_PLAN.md`, `_project_docs/DECISIONS.md` |
