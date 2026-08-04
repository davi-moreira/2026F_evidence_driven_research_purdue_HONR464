# INSTRUCTOR IMPLEMENTATION GUIDE — HONR 46400 (Fall 2026, v2)

*How to RUN the course week by week.* This is the operating manual, not the
design rationale. For **why** the course is shaped this way, read
`planning/COURSE_MASTER_PLAN.md` and `_project_docs/DECISIONS.md` (D17–D21).
For the machine-readable spine (dates, weights, milestone IDs), read
`course_config.yaml`. On any conflict, dates defer to
`planning/CALENDAR_BACKBONE.csv` and intent defers to the master plan.

The course is a 5-student honors seminar meeting **Mon/Wed/Fri, 50 minutes**,
across **43 meetings** (42 in person + 1 async). Five students run five
individual projects to five posters. The instructor's job is not to lecture; it
is to **monitor and formalize** student-led lectures, **run** the Friday
studios, and **grade the chain** on a fast, predictable cadence.

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
  (M13).

Fri Oct 2 (meeting 17) is a **regular in-person studio** on the standard
10/5/30/5 frame; M5 is submitted there like any other milestone.

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
lead quickly; it is the fastest way they improve before the next slot. SRL
performance is **20%** of the course grade (syllabus).

**Intervention protocol.** How to step in without seizing the room is summarized
in `project/srl/srl_handbook.md` ("How the instructor will step in"); the
student-facing philosophy, the ten SRL moves, and the AI-integration guidance
are in the rest of the SRL suite (`project/srl/`).

---

## 3. Milestone grading cadence

Sixteen milestones (**M0–M15**), one graded artifact each, on a **develop →
present → submit → revise** cadence. Due dates (all Fridays unless noted) are
fixed in `course_config.yaml milestones:`:

| M0 Aug 28 · M1 Sep 4 · M2 Sep 11 · M3 Sep 18 · M4 Sep 25 · M5 Oct 2 ·
M6 Oct 9 · M7 Oct 16 · M8 Oct 23 · M9 Oct 30 · **M10 Nov 6, 5 PM (terminal)** ·
M11 Nov 13 · M12 Nov 20 · M13 Nov 29 (Sun, async) · M14 Dec 4 ·
**M15 Dec 11 (terminal)** |

- **Return feedback within 3 days** of each milestone.
- **Revision window: 7 days** from feedback, for up to half the lost points, on
  every milestone **except the terminal two** (M10, M15) and the live Expo
  presentation (M12 component). For those, the deadline governs.
- Every submission must append an **AI Research Ledger** entry (8 fields) and
  update the cumulative **Research Project Dossier**. A missing ledger entry
  scores the rubric's Craft criterion 0 and the submission is **returned**.
- Rubrics share a fixed criteria menu (compass alignment, evidence integrity,
  verification, uncertainty + limitations, craft). Weighting proposal in
  `course_config.yaml assessment:`.

> **Build note:** `planning/ASSESSMENT_ARCHITECTURE.md` still describes the v1
> M00–M23 scheme and needs reconciling to the v2 weights before it is cited as
> authoritative. `syllabus.qmd` already carries the v2 weights (pending final
> instructor confirmation).

---

## 4. The milestone brief → Brightspace loop

Milestone briefs and rubrics are authored **one file per milestone** in
`_research_project/2026Fall/milestone_NN_<slug>.md` and are written to be
**copy-paste-ready into Brightspace** (one Brightspace page per milestone). Each
Friday, present the week's brief from Brightspace at the studio kickoff.

> **Build note:** the files currently in `_research_project/2026Fall/` are the
> **v1 M00–M23** briefs. The **v2 M0–M15** briefs are on the build queue (see
> the master build plan); confirm the v2 set is in place before the semester.
> Machine anchors and due dates are validated by `scripts/validate_milestones.py`.

---

## 5. GenAI Studio setup — DO THIS BEFORE THE SEMESTER

Purdue GenAI Studio (<https://genai.rcac.purdue.edu>) is the course's reviewer
bench. Students **must** consult an assigned reviewer role at four milestones:

| Milestone | Required reviewer role |
|---|---|
| M4  | Causal Identification Skeptic (route declaration) |
| M7  | Prediction & Leakage Auditor |
| M8  | Robustness & Sensitivity Reviewer |
| M10 | Poster Critic (before the lock) |
| M13 | Reproducibility Auditor |

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

1. **Abstract gate — Fri Oct 9 (M6).** Internal completion gate for the URC
   abstract (the external URC deadline is TBD; confirm and post it as soon as it
   publishes). Run the abstract workshop in the M6 studio.
2. **Poster lock + print submission — Fri Nov 6, 5:00 PM (M10, terminal).** The
   poster is locked and submitted for printing. No changes after this time.
   Confirm the print vendor turnaround well before this date.
3. **URC Expo — Tue Nov 17.** Required, graded (a component of M12). Each student
   presents their poster and **evaluates at least three colleagues' posters** on
   the course criticism instrument. **No class Wed Nov 18.** Only a documented
   emergency qualifies for a make-up, handled individually per Honors College
   norms.

Weeks 11–13 (`nb11`–`nb13`) rehearse the presentation: poster criticism, pitch
delivery under uncertainty, and fielding hard questions
(`project/conference/` holds the presentation, hard-questions,
uncertainty-limitations, dress-rehearsal, and reflection protocols).

---

## 7. The M13 replication exchange (anonymized)

The Thanksgiving async module (**Mon Nov 23**, due **Sun Nov 29**) is a
peer replication + red-team. Run the exchange as follows:

1. At the **Week-13 studio**, each student submits a **reproducibility package**
   (clean-run Colab notebook + data + documentation, SEED = 464).
2. **You anonymize:** strip identifying headers and reassign packages so no
   student receives their own or can identify the author.
3. Each student **reproduces** the assigned package from scratch and **attests**
   whether the headline result runs, then red-teams where it is fragile, using
   the GenAI Studio **Reproducibility Auditor** role as a second opinion.
4. The **replication + red-team report** is due Sun Nov 29 (async board
   exchange). Replication + red-team is **5%** of the course grade.

---

## 8. The defense schedule and end of term

- **Final defenses — meetings 42–43 (Wed Dec 9 + Fri Dec 11).** Each student
  delivers a public **evidence defense** of the whole project and their AI
  collaboration. Fold the defense grade into **M15**.
- **M15 — Fri Dec 11 (terminal).** Final research chapter + AI-management
  portfolio, submitted at the closing ceremony. No revision window.
- **End-of-term wrap:**
  1. Grade M15 and the defenses against the shared rubric menu.
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
| SRL handbook, template, rubric | `project/srl/` |
| Session guides (generated) | `scripts/build_session_guides.py` → `session_guides/` |
| Schedule data (SRL slots) | `scripts/schedule_data/part1–4.py` |
| GenAI Studio roles + setup | `genai_studio/` *(forthcoming)* |
| Conference/presentation protocols | `project/conference/` |
| Course-eval analysis | `scripts/analyze_course_eval.py` |
| Design rationale | `planning/COURSE_MASTER_PLAN.md`, `_project_docs/DECISIONS.md` |
