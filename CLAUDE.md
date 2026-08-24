# HONR 46400 Evidence-Driven Research — AI Assistant Guide

This file documents the rules and workflows that change Claude's behavior in this
repository. Reference material lives in linked files — read those when relevant,
not by default.

## Reciprocal agent partnership

Claude Code and Codex are peer agents with equal repository authority, subject
only to the tools and permissions available in each agent's current runtime.
Either may serve as the implementer, independent reviewer, or development
partner. The task's caller or delegating agent determines the role for that
task; neither agent is permanently primary or subordinate.

- When Codex calls Claude Code, serve as the reviewer or development partner
  requested by Codex.
- When Claude Code calls Codex, Codex should serve as the reviewer or
  development partner requested by Claude Code.
- When the user calls Claude Code directly, follow the role in the user's
  request. If no role is stated, infer it from the requested outcome:
  review/report requests are read-only; build/fix/change requests authorize
  implementation.
- An agent that implemented a change must not be its sole reviewer. When an
  independent review is requested or required, the peer agent inspects the
  actual work and reports its own judgment.
- While assigned as reviewer, do not modify files unless explicitly asked to
  switch roles and implement an approved finding.
- Equal authority does not bypass user instructions, repository rules, security
  boundaries, approval requirements, or runtime tool limitations.

## Project Mission

**HONR 46400 — SP: Evidence-Driven Research** ("How to Design, Analyze, Verify,
and Defend Empirical Research"), a semester-long Honors College seminar (Fall
2026, **Mon/Wed/Fri, 50 minutes, in person**, ~5 students, individual projects
by default with one instructor-approved group permitted when the peer-work
topology remains viable)
teaching honors students — **without assuming a quantitative or computing
background** — to run an original evidence-driven research project from
curiosity to a publicly defended claim. The course's defining message:

> **AI is your arm and your research assistant, not your brain.**

Students direct AI (their AI tools in Colab; Purdue GenAI Studio reviewer roles) through
the **Specify → Delegate → Interrogate → Inspect → Verify → Document → Defend**
workflow (everyday shorthand: **Ask → Verify → Document**), while keeping every
research decision — problem, question, design, measurement, ethics, claims,
uncertainty, defense — human. Deliverables: a poster presented at the **Purdue
Fall Undergraduate Research Expo (Tue Nov 17, 2026; poster locked Sun Nov 8,
11:59 PM — a print run shared with QM 47400)**, a replication + red-team report, a research note grown into a final
research chapter, an AI-management portfolio, and an oral evidence defense.

- **Instructor:** Professor Davi Moreira
- **Repository:** https://github.com/davi-moreira/2026F_evidence_driven_research_purdue_HONR464
- **Website:** https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464/
- **Deployment:** Quarto → `docs/` → GitHub Pages
- **v1 build** (compass-sequenced 20-notebook course) preserved at git tag
  `v1-compass-build`; v1 sources archived in `_production_kit/nb_sources_v1/`
  and `_production_kit/schedule_data_v1/` (gitignored).

## See Also (Reference Files)

| File | When to read |
|---|---|
| `_project_docs/ACTIVITY_TEMPLATE.md` | Creating/restructuring a topic notebook — the machine-validated template |
| `_project_docs/DECISIONS.md` | Before proposing convention changes — D17–D22 govern the v2 build |
| `planning/COURSE_MASTER_PLAN.md` | Sequencing source of truth (16 weeks, nb01–nb16, M1–M16) |
| `planning/PROJECT_MILESTONES.md` | The milestone chain (dev meetings, presentations, due dates) |
| `planning/SOURCE_AUDIT_V2.md` | The rebuild audit: rulings, reuse map, GenAI Studio verification |
| `planning/MEETING_SCHEDULE.md` | Per-meeting detail (43 × 34; generated from `scripts/schedule_data/`) |
| `planning/INQUIRY_MAP.md` | The compass (questions) + design-pathway (designs) layers |
| `surveys/participation_grading.md` | Anything about the Participation 9% or the IYT Practice 15% — the two undivided completion contracts (D57, amended D58/D61; it no longer owns "It is your turn" as participation) |
| `planning/IYT_SUBMISSION_SCHEDULE.md` | The **IYT Practice (15%)** submissions (35 per student, over 40 chapters, in 20 assignments), their due dates, and the one Brightspace instruction (generated) |
| `planning/STUDIO_FEEDBACK_SCHEDULE.md` | The 12 per-studio feedback deadlines (generated) |
| `project/srl/` | Student Research Lead handbook, templates, rubric |
| `genai_studio/` | GenAI Studio role specs, KB strategy, Colab PoC |
| `CONVERSATION_LOG.md` | Project history and prior decisions |
| `scripts/ci_gates_local.py` | Before changing a validator or `.github/workflows/validate.yml` — runs the CI gates on a tracked-files-only checkout, where `_production_kit/` and `notebooks/instructor/` do not exist |

**Canonical notebook reference:** `notebooks/student/nb05_observational_descriptive_student.ipynb`
(the v2 gold standard, built as the Phase-2 prototype) — match its formatting
exactly. Cell sources live in gitignored `_production_kit/nb_sources/nbNN_<slug>.py`;
edit the source, then rebuild with `.venv/bin/python scripts/nbbuild.py nbNN`.

---

## 🚨 CRITICAL RULE — Voice and Audience in Student-Facing Content  *(KEEP verbatim)*

The student activity is read **BY students**, not by instructors who then teach it.
Every sentence in a student-facing cell — including AI prompts and "After running,
verify" checklists — must be written **TO the student**, never ABOUT the student and
never TO the instructor.

1. Never write "students" as a third-party noun inside a student-facing cell.
   Rewrite in second person (`you`), neutral imperative, or first person.
2. AI prompts are scripts the student copies into the AI tool — they must sound like
   something a student would actually type.
3. No instructor-voice / facilitation language in student cells. That belongs only
   in `session_guides/NN_session_guide.md` (gitignored).
4. Session guides may reference students in third person in wrapper prose, but NOT
   inside blockquote read-aloud scripts (`> *"..."*`).

```bash
.venv/bin/python scripts/voice_lint_notebooks.py                      # all student notebooks; expect ✓ clean
python3 scripts/voice_check_guides.py session_guides/NN_session_guide.md
```

---

## 🚨 CRITICAL RULE — Undergraduate-Friendly Voice  *(D14; unchanged)*

Notebooks are read by honors undergraduates with **no quantitative background**.
The narrative machinery stays; the prose must read like a person, not a model.

**Keep (the pedagogy):** named research-world stakeholders opening "Why This
Matters" cells; narrative prose over bullet lists; inline Q&A blocks
(`> **A question that often comes up here:** …`); section bridges and warm
wrap-ups bridging to the next week.

**Enforce (machine-checked by `scripts/voice_lint_notebooks.py`):**
1. **Em-dash budget: ≤ 20 per notebook, ≤ 1 per markdown cell.**
2. **Every technical term:** bold term → one-sentence plain-language definition
   → concrete example, before reuse.
3. **Short-to-medium sentences** (~12–25 words), one idea each, second person.
4. **No fourth-wall meta-references** about how the material was constructed.
5. **No fabricated citations anywhere** (D16).

---

## 🚨 CRITICAL RULE — Evidence-Integrity & Results-Verification  *(unchanged)*

1. **Every empirical claim traces to a real, retrievable source.** If a claim
   came from an AI tool, the underlying source is independently located and
   confirmed to exist.
2. **Every result is verified before it is reported** — recomputed,
   triangulated, or spot-checked, and the check is recorded.
3. **Decisions are documented, not just outcomes.**
4. **No planted-fake citations, even as a teaching device** (D16); hallucination
   demos catch LIVE AI output, never planted text.

```bash
.venv/bin/python scripts/audit_sources.py
```

---

## 🚨 CRITICAL RULE — The AI Research Ledger & SDIIVDD  *(D21 — replaces "Responsible-AI-Use Documentation")*

Every deliverable and every notebook session appends to the student's **AI
Research Ledger** (fields: task delegated · tool used · prompt · output summary
· decision · verification method · remaining concern · responsible researcher).
Embedded AI prompts carry an **"After running, verify:"** checklist ending with
a ledger line. Every notebook also contains: an AI Research Partner briefing,
an initial human commitment BEFORE consulting AI, at least one required prompt
modification, an AI-output interrogation, a **Human-Only Checkpoint** (no AI),
and a **Defend Your Decision** closing move. A missing ledger entry scores the rubric's Craft
criterion 0 and returns the submission. The claim ledger (what the research
asserts) is a separate instrument from the AI Research Ledger (what AI did and
how it was checked).

---

## 🚨 CRITICAL RULE — Inquiry-Declaration Justification  *(updated for the two layers)*

Questions are classified on the **inquiry compass** (RDSS ch. 7): **kind**
(descriptive vs causal) × **reach** (data at hand / population / unseen).
Designs are classified on the **library pathways** (RDSS ch. 15–18):
observational/experimental × descriptive/causal, plus **prediction as its own
answer objective** (never forced into either grid; experimental assignment does
NOT automatically imply a causal inquiry). Whenever a student declares, the
deliverable must state at a conceptual level: (1) why kind + reach fit the
question's words, (2) which crossing licenses the design holds (sampling →
population; prediction-time honesty + held-out check → unseen; assignment /
identification → causal) and hence what the answer can and cannot establish,
and (3) key limitations and uncertainty. Canonical: `planning/INQUIRY_MAP.md`;
machine core: `course_config.yaml inquiry_framework:`. Never reintroduce the
retired four-approach grid vocabulary (D12).

---

## 🚨 CRITICAL RULE — Uncertainty & Limitations in Communication  *(unchanged)*

Findings are never communicated as certainties. Every written report and oral
defense states the uncertainty around its claims and the limitations of its
evidence and method. A results statement with no uncertainty/limitations framing
is a defect.

---

## 🚨 CRITICAL RULE — Lecture Labels, Never Dates  *(D13 rule; unchanged mechanics)*

Notebooks and session guides carry **no calendar dates and no "Meeting M#"
references** — position is expressed as `**Topic NN · N lecture(s)**` headers
and explicit `# Lecture 1` / `# Lecture 2` heading cells, derived mechanically
from `lecture_labels()` in `scripts/notebooks_map.py` (computed from
`planning/MEETING_SCHEDULE.csv`). Dates live ONLY on `schedule.qmd` and in
milestone briefs (`_research_project/2026Fall/`).

---

## 🚨 CRITICAL RULE — The Flipped Classroom & 50-Minute Architectures  *(D17/D18, amended D22/D33)*

**Every Mon/Wed lecture from Week 2 is led by a Student Research Lead (SRL)**
running a Socratic investigation. Slots are **randomly assigned at the start of
the semester** (no rotation, no seats). Each lecture's **SRL Lead Brief** is a
STUDENT-VISIBLE `### 🎤 SRL Lead Brief` cell that opens that lecture in its
notebook (right after `# Lecture N`, before the 🧩 Research Puzzle); leads prep
from one week ahead and submit a preparation script/notebook the day before
the lecture, 11:59 PM (D66).
Briefs must stay simple to follow and explicitly leave room for the lead's own
staging. Fixed section frames, enforced by the session-guide generator
(sums = 50):

- **Monday:** 0–9 SRL research puzzle · 9–31 guided AI research-partner
  investigation · 31–43 human verification + instructor formalization ·
  43–50 decision & defense (ledger + Claim Ticket).
- **Wednesday:** 0–7 SRL retrieval & challenge · 7–30 intensive applied AI
  laboratory · 30–42 peer defense + adversarial questioning (internal split,
  D34: defense to 38, then 38–42 SRL synthesis + instructor accuracy lock) ·
  42–50 project transfer (ledger + Claim Ticket).
- **Friday studio (no new topic content):** 0–5 research stand-up · 5–45
  milestone kickoff (presented from the course Brightspace page) +
  AI-supported work with the student's AI assistant · 45–50 revise, update
  ledger + dossier, submit (Claim Ticket). The Friday red-team block was
  RETIRED (D30); students WORK ON milestones at the studio (no weekly
  presentations). **D58 retired the opening weekly quiz block for this
  edition** — no quiz is administered and nothing is scored on one, and the
  sprint absorbs the ten minutes (5 + 40 + 5 = 50). The banks and builders
  (`_quizzes/`, `scripts/audit_answer_length.py`, and any quiz-building
  script) are KEPT for a future edition and must never be deleted.

**D50 — the conference block.** Weeks 1–10 are Studios 1–10, so **course
milestone M(n) presents Book Milestone (n) one-to-one for n = 1..10**. Weeks
11–14 are the CONFERENCE BLOCK and anchor no new lesson: poster production and
the in-class peer review (M11 draft due AT CLASS Wednesday, M12 one independent
review of every other active project), the **terminal poster lock Sun Nov 8,
11:59 PM (M13)**, presentation
preparation (M14, three timed pitches + the invitation post), the Expo, and two
ASYNCHRONOUS reflection sessions (Fri Nov 20 + Mon Nov 23) closing at M15.
**Studios 11 and 12 run POST-conference on Weeks 15–16 in the standard frame**
(MW teach the lessons, Friday IS the milestone): M16 presents Book Milestone 11
and M17 presented Book Milestone 12 until **D54 retired M17**: the chain is
**M1–M16**, Week 16 still TEACHES Studio 12 but collects nothing, and the last
Friday (Dec 11) is the course-closing reflection, graded under participation.
The peer cold run is IN CLASS on the Week-15 Wednesday. Course milestones are
**M1–M16**; never write M0 and never write M17.

**D55 — every milestone is due the Sunday after its Friday studio, 11:59 PM.**
The studio is still where the work happens; the deadline is the end of that
weekend. Three exceptions keep their weekday slots: M11 (Wed Nov 4, at class),
M12 (Fri Nov 6, 2:30 PM, so peer criticism reaches authors before the lock) and
M13 (Sun Nov 8, terminal). **D66 adds two holiday exceptions: M2 is Mon Sep 7
(Labor Day) and M7 is Tue Oct 13 (October Break).**
`course_config.yaml milestones:` is the source of truth for every due date.

**🚨 D66 — the course platform wins on dates.** Where a due date on Brightspace
disagrees with this repository, **the platform is correct**: fix the repository,
never the platform, and record the correction. The repository still owns the
*rules*; the platform owns the *dates students see*. The studio-feedback survey
takes the same treatment through
`course_config.yaml participation.items.studio_feedback.overrides` (Studio 2 →
Tue Sep 8). SRL preparation is due **11:59 PM the calendar day before the
lecture**, with no class-day snapping.

**All seven active-learning moves + the lecture's 📒 ledger row run INSIDE the
50 minutes (D33)**, above each lecture's `### ⏸ Optional depth from here`
line; below the ⏸ (and every 🏠-labeled prompt) is enrichment, never required
homework. In-class weights: 📝 aloud · ⚖️ one committed line defended aloud ·
🎯 one sentence · 🛡️ the short ritual close. `validate_notebooks.py` enforces
placement (exempt: nb01, nb14, nb13 — conference week's below-⏸ is the Expo +
reflection-studio path).

Week 1's two lectures are instructor-led to model the format. SRL materials:
`project/srl/` (canonical; the book's SRL appendix was retired by D35 — the
book's For Instructors appendix links `project/srl/`); the milestone chain
and weekly-architecture orientation live in nb01 Lecture 1 (not on the
syllabus).

---

## 🚨 CRITICAL RULE — Participation Is One Undivided Completion Contract  *(D57, amended D58)*

Participation is **9%, undivided**. Never publish or apply an internal split of it.
Every required item is worth the same single credit; the block is their sum. **D58
moved the "It is your turn" family OUT of Participation** into its own top-level
**IYT Practice (15%)** category, so the two are separate instruments with separate
credit pools. Three item families remain here and nothing else:

1. **Studio feedback survey** — **one response per Studio, never per chapter**, due
   **11:59 PM on the Sunday that ends the studio week** (12; Studio 12 closes Dec 11).
2. **Student profile survey** — Sun Aug 30, 2026.
3. **Course reflection** — Fri Dec 11, 2026 (D54 put it here; it is not a milestone,
   and it is not M15's conference reflection).

Baseline **N = 14** (12 + 1 + 1), so **d = ⌈0.10 × 14⌉ = 2**. Credit `1.0` on time /
`0.5` within seven days / `0` otherwise; the lowest `⌈0.10 × N⌉` credits drop
automatically, and

```
participation points = 9.0 × (sum of the highest 12 credits) / 12
```

"Other constructive contributions" is a documented **±0.9-point adjustment**, not a
bucket with a weight — the block is still 9%.

**Never reintroduce, in any surface:** lecture-notebook completion as a graded thing
(lecture notebooks are **never collected**), per-chapter reading feedback, the retired
5/2/2 split, or any other published internal split of the 9%. **The syllabus stays
generic** — one paragraph, no sub-weights, no dates, on the web page and in the
`.docx` alike; the operative detail lives in `surveys/participation_grading.md`.
Milestone briefs keep their Book Anchor but must say the "It is your turn" sections
were **already submitted and are not collected a second time**.

```bash
.venv/bin/python scripts/build_participation_schedules.py   # IYT + studio + SRL tables
.venv/bin/python scripts/build_studio_feedback_survey.py    # Qualtrics import + instrument
```

---

## 🚨 CRITICAL RULE — IYT Practice Is Its Own 15% Completion Contract  *(D58, amended D61)*

**IYT Practice is 15%**, a top-level assessment category, and it holds exactly one
item family: the EDR|AI **"It is your turn"** sections of the required chapters. One
submission per required chapter, due **11:59 PM on the date that chapter's reading
was due**, graded by **completion** and never by content.

- `count_typical` is **35** — 34 chapters everyone reads, **one** pathway chapter
  (the student's own declared route; the assigned contrast is required reading but
  is NOT collected, D60), and one more if the declared design has stages
  (N = 36; ⌈0.10 × 36⌉ is still 4).
- Credit `1.0` on time / `0.5` within seven days / `0` otherwise.
- Drop `d = ⌈0.10 × 35⌉ = 4` lowest credits, automatically.
- `iyt points = 15.0 × (sum of the highest 31 credits) / 31`.
- Dated list: `planning/IYT_SUBMISSION_SCHEDULE.md` (generated by
  `scripts/build_participation_schedules.py`; never hand-edited).

This work is **not participation** and must never be called participation on any
surface. The ±0.9-point contribution adjustment belongs to the 9% block alone and
never touches this one. Milestone briefs still name their Book Anchor chapters and
still record that the sections were already handed in, not collected a second time.

---

## 🚨 CRITICAL RULE — Dataset Distribution  *(D15; unchanged)*

`notebooks/data/` is the single canonical dataset folder; everything ships in
`notebooks/data/data.zip`, linked from Material and Schedule. The archive
stores its members under `notebooks/data/`, which is the first path
`load_course_data()` falls back to, so unzipping it makes offline runs work.
After any dataset change:

```bash
.venv/bin/python scripts/make_dataset_zip.py
```

Notebooks load data via `load_course_data()` (GitHub raw first, local fallback).

---

## 🚨 CRITICAL RULE — The EDR|AI Book-First Loop  *(D20, amended D23/D24/D25/D26/D35)*

The course book is **EDR|AI** (*Evidence-Driven Research in the Age of AI*;
`book/`, 37 chapters + Part I overview — 40 lessons and 12 practice stations
under D35's Architecture v0, provisional; front matter: Preface then About the
Author; appendices: Verification Guide, For Instructors (SRL retired to
`project/srl/`, D35); rendered to `docs/book/`; book author is "Davi Moreira",
no title). **Chapter review is FROZEN until Architecture v1 (D35;
`planning/BOOK_DESIGN_ACCEPTANCE.md` holds the acceptance tests).** The loop:

1. **Book and course are DIFFERENT artifacts (D25).** The book owns its
   notebooks: every chapter's badge opens its OWN companion Colab notebook
   (`notebooks/book/chNN_<slug>.ipynb` + `pt/`/`es/`), generated by
   `scripts/build_book_notebooks.py` — rerun it after ANY chapter edit. The
   chapter's "Colab laboratory" section introduces the companion notebook,
   then names its primary course lab (nbNN) as companion-course material. The
   **For Instructors** appendix presents and links all course material; it
   ships **openly** (D35 retired the D26 page encryption — the private
   instructor repo + GitHub auth is the protection; genuinely private material
   lives ONLY there, never on a public page). The
   generator also derives each chapter's **"It is your turn" RUBRIC** (D26):
   a rubric cell in the companion notebook + `<edition>/_iyt-rubrics.qmd`
   included in the appendix — never hand-edit those files. (Rubric
   auto-derivation is slated for retirement under D35 Phase 4 — authored
   rubrics in `planning/BOOK_ASSESSMENTS.yml`.)
2. **Development banners + seeded simulations (D26).** Every chapter carries
   a `.review-pending` warning banner until Davi reviews it (the Part I
   overview page too — `part1_overview` in the registry): the registry is
   `planning/BOOK_REVIEW_STATUS.yml`; when he reports a chapter reviewed,
   flip its flag, run `scripts/update_chapter_review_banners.py`, re-render.
   Companion-notebook header spec (D27): logo → title → "Authored by Davi
   Moreira" (links to the book) → companion line → links → the one rule.
   NEVER add artifact-boundary meta-commentary to reader-facing content
   (no "this belongs to X, not Y" sentences). Chapter badges use
   `[![](badge){fig-alt="Open In Colab"}](url)` — the empty alt suppresses
   Pandoc's implicit-figure caption; keep that form. Part I figure:
   `scripts/build_book_part1_figure.py` (mermaid retired).
   Whenever possible, chapters embed **seeded (SEED=464) simulation code that
   visually presents the concept**: the chapter shows the code AND the
   pre-generated figure (`scripts/build_book_sim_figures.py`, localized
   labels, offline — no render-time execution); keep the chapter block and
   the script in sync, and the code flows into the companion notebook
   automatically. Shipped so far: ch11, ch14, ch15 — extend as chapters are
   reviewed. ALL book prose follows `_project_docs/BOOK_VOICE_POLICY.md`
   (D28: must never read as AI-generated; teaching devices stay, the tells
   go; never say a reader "does not need to be enrolled" — frame
   self-learning positively). Lint: `scripts/voice_lint_book.py`
   (`--strict` on newly written prose).
3. **Notebook content must reflect the book** — course notebooks derive from
   the chapters; every notebook's wrap-up names its chapters; never edit a
   chapter's design content without checking its notebook (and vice versa).
   Every milestone brief M1–M16 **names** its **Book Anchor** chapters but no
   longer collects them (D57): each "It is your turn" section is handed in on
   its own chapter's reading date, under **IYT Practice** (15%, D61). The
   anchors do not partition the book's 40 active lessons — ch. 38–40 anchor to
   nb16, whose crosswalk row carries no milestone (D54), so they are
   IYT-Practice-only, and M11–M15 anchor no chapters at all.
4. **The instructor manually reviews and updates the book**; the assistant then
   articulates and incorporates those reviews across the course material
   (notebooks, guides, site).
5. **The book is institution-agnostic** (used outside Purdue): chapter bodies
   say "your course platform", "AI reviewer bench", "your research conference";
   Purdue specifics appear only as parentheticals (the For Instructors appendix
   is where the companion course is presented). Reading model: EDR|AI chapters
   REQUIRED, matching RDSS chapters RECOMMENDED (stated on the Material page
   and preface — the in-chapter Reading boxes were retired, D24).
   The book is a SELF-CONTAINED MANUAL: every chapter ends with an
   **"It is your turn"** section, and the 40 sections chain into a complete
   research project/paper by the end (no course-milestone language in chapter
   bodies). Domains for examples: econ, political science, business, biology.
   The "AI can review AI — but the last decision is human" rule lives in the
   Verification Guide appendix and wherever chapters verify.
6. **Translations:** `book-pt/` (PT-BR) and `book-es/` (ES) are generated from
   the English edition (the source of truth). **D36 (2026-07-31): translation
   is FROZEN until the end of the D35 build** — edit and render ENGLISH ONLY;
   the PT/ES books stay online behind per-page development notices (injected
   by their `_lang-switcher.html`), and every deferred item is logged in
   `planning/TRANSLATION_BACKLOG.md`. The resynchronize-on-every-edit rule
   resumes at project end, after Davi's manual EN review; translations may
   not ship *as current* before that sync. During the freeze:

```bash
.venv/bin/python scripts/build_book_notebooks.py          # EN companions + rubrics (D36: defaults --editions en)
.venv/bin/python scripts/update_chapter_review_banners.py # banners from BOOK_REVIEW_STATUS.yml
.venv/bin/python scripts/build_book_sim_figures.py        # EN seeded figures (D36: defaults --editions en)
.venv/bin/python scripts/voice_lint_book.py               # BOOK_VOICE_POLICY tells (D28)
.venv/bin/python scripts/validate_book_sync.py            # chapter↔notebook links, both directions
quarto render book/    # AFTER the site render
quarto render book-pt/ && quarto render book-es/  # SOURCES frozen (D36) and the
                       # generators skip them, so this re-emits byte-identical
                       # pages; needed ONLY because the site render PRUNES docs/book-*
```

---

## 🚨 CRITICAL WORKFLOW — Instructor-First Notebook Editing  *(hard rule — no exceptions)*

**ANY request to "work on a notebook" means: edit the instructor side first; the
student notebook is only ever a mechanical, answer-stripped copy.** Never edit a
`notebooks/student/*.ipynb` directly.

ALWAYS edit the cell source `_production_kit/nb_sources/nbNN_<slug>.py` (gitignored)
FIRST, then rebuild: `.venv/bin/python scripts/nbbuild.py nbNN` — regenerates the
instructor notebook, executes it with nbclient, strips `INSTRUCTOR SOLUTION`
cells into the student file, runs the template/voice validators, and refreshes
the schedule badge.

- Markers: `### INSTRUCTOR SOLUTION — Exercise N`, `# INSTRUCTOR SOLUTION`,
  `<!-- INSTRUCTOR SOLUTION -->`. Student placeholders: `### YOUR ANSWER HERE:`,
  `# YOUR SOLUTION HERE`.
- Only `notebooks/student/*_student.ipynb` is committed; instructor notebooks and
  `_production_kit/` are gitignored.
- Badges key off git-tracked student files (`scripts/update_schedule_badges.py`).
- **After building, sync the private instructor repo:**
  `scripts/sync_instructor_repo.sh` (backs the Instructor tab; the page ships
  openly since D35 — the private repo + GitHub auth is the protection).

---

## 🚨 CRITICAL WORKFLOW — Sync Session Guides and Planning Docs

Session guides are GENERATED: edit `scripts/schedule_data/part1–4.py` →
`.venv/bin/python scripts/build_meeting_schedule.py` →
`.venv/bin/python scripts/build_session_guides.py`. Never hand-edit
`planning/MEETING_SCHEDULE.{csv,md}` or `session_guides/*.md`. Significant
sequencing changes also update `planning/COURSE_MASTER_PLAN.md`.

---

## 🚨 CRITICAL WORKFLOW — The Syllabus .docx Is Generated, and Davi Edits It  *(D62)*

The two Word documents in `_syllabus/2026F/` are GENERATED (`_syllabus/` is
gitignored, so git will not warn you):

```bash
.venv/bin/python scripts/build_syllabus_docx.py    # syllabus + embedded schedule
.venv/bin/python scripts/build_schedule_docx.py    # standalone schedule
```

Davi also edits the BUILT file directly in Word. **Before running either builder,
check the .docx mtime against the script's.** If the document is newer, it holds
hand edits that the build would destroy:

1. Copy the .docx aside FIRST.
2. Generate to a temp path instead of `OUT` (import the module and reassign
   `m.OUT`; do not run the script, which writes to `OUT`).
3. Diff the two, treating **every** difference as an instruction from Davi.
4. Fold the edits into the generator, regenerate, and confirm the output is
   text-identical to his file.
5. Record it in `DECISIONS.md` and propagate to `syllabus.qmd` and any other
   surface carrying the same text.

Never rebuild over his file to "restore consistency" — the generator is what
gets corrected. A `~$…docx` sibling means Word still has it open.

---

## 🚨 CRITICAL WORKFLOW — Commit AND Render Webpage  *(KEEP verbatim)*

Every content change → `quarto render` → commit `docs/` → push. GitHub Pages serves
`docs/`; skipping the render leaves the site stale (the project's most common
mistake).

```bash
git add <changed .qmd or activity>
git commit -m "feat: ..."
/Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto render
git add docs/ && git commit -m "build: Render Quarto site"
git push origin main
```

Site pages: `index` / `syllabus` (hand-edited), `material.qmd` + `instructor.qmd`
(generated by `scripts/build_material_page.py`), `schedule.qmd` (generated by
`scripts/update_schedule_badges.py`), the book (rendered from `book/`).
Instructor-facing pages ship openly (D35); genuinely private material lives
only in the private instructor repo. Do not hand-edit generated pages.

---

## 🚨 OPTIONAL RULE — MC Option-Length Parity  *(dormant; only if MC quizzes are used)*

If auto-graded MC quizzes are introduced: every option ≥ 60% of the longest
option's length; correct option strictly longest in ≤ 40% of a bank;
`python3 scripts/audit_answer_length.py --file <csv>` must PASS before import.

**D58 — the quiz material is KEPT, the category is not.** No quiz is administered
this edition and nothing is scored on one, but the banks under `_quizzes/` (already
gitignored), `scripts/audit_answer_length.py`, and every quiz-building script stay in
the repository for a future edition. **Never delete a quiz file or a quiz script.**
What was retired is the grade category and the Friday class-time block, never the
material.

---

## Style Guidelines

| Setting | Value |
|---|---|
| Money in markdown cells | Always escape: `\$50,000` |
| Tildes in markdown cells | Always escape: `\~30 sources` |
| Emoji vocabulary | `✓` success, `⚠️` warning, `📝` exercise, `💡` insight |

> `SEED = 464` via `np.random.default_rng(SEED)` in every setup cell; all
> simulations deterministic. No seaborn. Python 3.11-compatible; libraries:
> numpy, pandas, matplotlib, scipy, statsmodels, scikit-learn, networkx.

## Naming and Commit Conventions

- Student notebooks (committed): `notebooks/student/nbNN_topic_student.ipynb`
  (nb01–nb16, one per week); milestone studio notebooks `msNN_topic_student.ipynb`.
- Instructor notebooks (gitignored): `notebooks/instructor/…_instructor.ipynb`
- Cell sources (gitignored, canonical for editing): `_production_kit/nb_sources/`
- Milestone briefs: `_research_project/2026Fall/milestone_NN_<slug>.md` (M1–M16;
  the two D49 briefs the renumber retired are archived under `_retired_d50/`)
- Commit messages: `<type>: <subject>` (feat|fix|docs|chore|build|refactor) with a
  trailing `Co-Authored-By:` line. Stage specific files — never `git add .`.

---

**Version:** 7.0 — D62, Davi's Word pass folded back into the generator
(2026-08-23, DECISIONS.md D62): the syllabus `.docx` is a GENERATED artifact that Davi
also edits by hand, so hand edits are now captured and pushed back into
`scripts/build_syllabus_docx.py` before it is ever run again (see the new CRITICAL
WORKFLOW above). Five adopted changes: the course-materials label becomes
**`Recommended:`**; the `Grading:` lead-in drops its duplicated "There is no curve.";
the **Grading scale moves directly beneath the weights table**; the **AI Policy body
becomes one bullet per principle** (`NUM["ai_policy"]` repointed 2 → 14 to match the
720-twip Symbol bullet Word used); and "Some activities **are** done without AI"
becomes "**may be** done". Propagated to `syllabus.qmd`, which also gained the
"AI is your arm…" line the `.docx` had and the web page lacked. **No weight, deadline,
or contract changed** — D61's table still governs. ⚠ Exposed and UNRESOLVED:
`syllabus.qmd` still names Gemini the "primary" assistant, contradicting the `.docx`
and D30.
(6.9 — the D61 weight rebalance (2026-08-23, DECISIONS.md D61):
**IYT Practice rises from 10% to 15%** and **Student Research Lead settles from 30%
to 25%**. D61 amends D58's two weights and nothing else: the completion-contract
mechanics, the credit rule, the drop rule, participation's undivided 9% (N = 14,
d = 2), IYT's counts (N = 35 typical, 36 with stages, d = 4), the quiz retirement and
the Friday 5/40/5 frame all stand. The IYT formula becomes `15.0 × (sum of the highest
31 credits) / 31`; participation's stays `9.0 × …` and its ±0.9 contribution adjustment
is untouched. Weights: attendance 1 · participation 9 · IYT Practice 15 · SRL 25 ·
Final Project 50.)
(6.8 — the D58 quiz retirement and IYT Practice split (2026-08-23,
DECISIONS.md D58): the **quiz grade category and its Friday class-time block are
RETIRED for this edition** — no quiz is administered and nothing is scored on one,
while the banks (`_quizzes/`), their builders and `scripts/audit_answer_length.py` are
KEPT for a future edition and must never be deleted. The EDR|AI **"It is your turn"**
sections leave Participation and become a top-level **IYT Practice, 10%** (N = 36,
d = 4, completion, due 11:59 PM on each chapter's reading date). **Student Research
Lead rises from 20% to 30%.** Participation stays **9%** over **14** credits (12
studio feedback + profile survey + course reflection, d = 2), undivided as before.
The Friday studio becomes three sections summing to 50: **0–5 research stand-up ·
5–45 milestone kickoff + AI-supported work · 45–50 revise, update ledger + dossier,
submit** — the sprint absorbs the ten quiz minutes. Weights: attendance 1 ·
participation 9 · IYT Practice 10 · SRL 30 · Final Project 50.
(6.7 — the D57 participation contract (2026-08-23, DECISIONS.md D57):
Participation stays **one undivided 9%** and becomes a completion contract over four
item families — the book's **"It is your turn" sections, collected on the date each
chapter's reading was due** (40 chapters, 21 Brightspace assignments,
`planning/IYT_SUBMISSION_SCHEDULE.md`); a **per-studio** feedback survey replacing the
per-chapter one, closing the Sunday that ends each studio week
(`planning/STUDIO_FEEDBACK_SCHEDULE.md`); the **student profile survey** (Aug 30); and
the **course reflection** (Dec 11). Retired: the proposed 5/2/2 internal split,
lecture-notebook completion (notebooks are never collected), and per-chapter reading
feedback. The syllabus Participation section is deliberately generic on the web page
and in the `.docx`; `surveys/participation_grading.md` carries the operative rule. The
"It is your turn" row STAYS in every anchored milestone's submission table and now
records that the sections were already handed in; the five conference-block briefs
(M11-M15), which anchor no chapter, lose theirs. The 10 scored Synthetic Colleague
audits join the participation ledger as equal credits, retiring their
best-8-of-10 rule.
(6.6 — the D53 QM474 syllabus-text adoption (2026-08-23, DECISIONS.md
D53): the public `### Final Project (50%)` syllabus section is now QM 47400's Final
Project section copied **word for word**, with exactly six permitted deviations (the
35%→50% header; "In groups … predictive analytics" → the individual-default
evidence-driven framing; "teamwork" → "research work"; "each group … other teams'
posters" → "each student … the other projects' posters"; "indicated in the syllabus" →
"indicated in the course schedule"; and the TA dropped from item 5, since HONR has
none). **No weight, component name, or scoring rule changed — D52 still governs those.**
The operational machinery (the share-of-course table, the four scoring formulas, the
project-mode rules, the Peer Evaluation conversion) moved OUT of the syllabus into
`_research_project/2026Fall/final_project_grading_and_project_modes.md` — the
"comprehensive set of project guidelines" the new text promises — and
`brightspace/gradebook_spec.md`. The syllabus governs the weights; that document governs
the detail. ⚠ The adopted text promises "a poster template and assessment rubric will be
shared"; the rubric exists, **the template does not** and is now a public promise due by
M11 on Wed 2026-11-04.
(6.5 — the D52 grading and project-mode contract (2026-08-23,
DECISIONS.md D52): one top-level Final Project at 50%, using QM474's same five
items at 30/20/10/20/20; individual work is the default, with at most one
instructor-approved group of two or three when at least three active projects
and a feasible Peer Evaluation assignment remain; solo researchers receive
confidential ratings from two assigned project peers, while group members rate
teammates; all student-facing grading, milestone, poster, Brightspace, and
notebook sources synchronized.))
(6.4 — the D50 conference block (2026-08-22, DECISIONS.md D50):
course milestones renumbered **M0–M15 → M1–M17** so M1–M10 present Book
Milestones 1–10 one-to-one; Weeks 11–14 become the conference block (poster
production, in-class peer review, the terminal **Sun Nov 8** lock shared with
QM 47400's print run, presentation preparation, the Expo, and two asynchronous
reflection sessions); **Studios 11–12 move to Weeks 15–16** in the standard
MW-lessons/Friday-milestone frame, with the peer cold run brought in-class;
Fri Nov 20 becomes asynchronous (43 = 41 in-person + 2 async); imported from
QM 47400 — the conference application with its proof PDF (previously absent
entirely), the draft abstract, the poster template and rubric, the timed-pitch
specification, the invitation post, the structured peer-review instrument, and
the proof-of-presentation photograph. New notebooks nb11/nb12; Studios 11/12
became nb15/nb16.
(6.3 — the D36 translation freeze + autonomous build-out
(2026-07-31, DECISIONS.md D36): PT/ES frozen online behind per-page
development notices until the D35 build completes — EN is the sole edited and
rendered edition; deferred work (round-4 PT/ES ch14 errors, ch21/ch22
crossing, preface fix, human PT/ES methods review) logged in
`planning/TRANSLATION_BACKLOG.md`; Phases 1–4 execute autonomously via the
two-role Codex loop; course readings regenerate from the machine-verified
crosswalk; translation happens once, after Davi's manual EN review.)
(6.2 — the D35 book-design ruling + Phase 1 (2026-07-30, DECISIONS.md
D35, from the task-#20 evaluation: two ultra Codex rounds + the Batch-A/B/C
correction loop): EDR|AI Architecture v0 ruled — independence axiom binding, 39
lessons, 12 provisional practice stations, versioned Research Contract, four
rails, four-dimension route model; **chapter review frozen until Architecture
v1** (`planning/BOOK_DESIGN_ACCEPTANCE.md` = the promise/acceptance-test
contract, A1–A11); F7 page encryption retired (pages ship openly; the private
instructor repo is the protection); SRL appendix out of the three books
(canonical: `project/srl/`); 111 legacy shims skipped. Phase-1 methods
corrections applied in ENGLISH through the two-role Codex loop (partner mirror
runs + adversarial critiques): the kind rule (a causal question with weak data
is "causal, currently unidentified" — NEVER relabeled descriptive; enforced in
INQUIRY_MAP, course_config.yaml `kind_rule`/`claim_upgrades:`, nb02, ch06/ch09/
ch25), signed bias + declared-test power (ch10, nb04), attrition as
complete-case contrast with retention as warning-light-not-diagnosis (ch15,
nb09), sufficient adjustment set not "every confounder" (ch12), three-role
prediction split (ch14), items-not-people reliability + interpretation-and-use
validity (ch18), same-estimand specification curves (ch21), null reference
spread not exact zero (ch22), LOCF/death + demand-the-execution-record (ch32);
new seeded counterexamples ch14/ch15-attrition/ch22. PT/ES deliberately stale
until the English passes review — a release blocker, do not render-and-ship
translations before syncing them. (6.1 — twelfth review round (2026-07-30,
DECISIONS.md D34, from
the task-#18 evaluation + Codex critique): truth-in-labelling sweep — optional
(below-⏸ / 🏠) material may never be assessed or scheduled as required
(week07 quiz Q5 replaced; M18/M26 schedule fields realigned; nb08 gained a
compact in-class cross-validation + shift probe licensing week08's quiz and
M7's boundary language); one-live-prompt rule machine-checked (nb03 allowance
2; `**🏠 Optional depth.**` label required in the prompt's own cell; homework-
depth wording banned); nbbuild normalizes the ⏸ region (standard cell text;
Wrap-Up → Sources hoisted above the final ⏸ — the close is never optional;
nb13 exempt); validator requires exactly one ⏸ heading per governed lecture +
the close above it; Wednesday 30–42 split internally into 30–38 peer defense
+ 38–42 SRL synthesis & instructor accuracy lock (D22 boundaries untouched;
13 Wednesdays; SRL suite + book appendix ×3 + implementation guide updated,
the guide also de-staled: quiz-first Friday, random slots, SRL 20%). Rejected
after verification: Wednesday retime, four-heading collapse, calendar
fading. (6.0 — eleventh instructor review round (2026-07-29, DECISIONS.md
D33): ALL seven moves + a per-lecture 📒 ledger row now run INSIDE the
50-minute MW frame, above each lecture's `### ⏸ Optional depth from here`
line — the required homework tail is retired (below-⏸ and 🏠 prompts are
optional depth); Wednesday opens with a spoken 📝 retrieval drill and folds
🔁/🔬 into the lab; in-class weights codified (template §7); frames, validator
placement checks, all 25 lectures, nb01's week cells, and the SRL appendix ×3
updated; exemptions nb01/nb14/nb13 (conference path). (5.9 — eighth
instructor review round (2026-07-29, DECISIONS.md
D30): AI-generic student-facing voice (Gemini retired from notebooks + 5
chapters; template element renamed "AI Prompt"); agentic-era framing +
brainstorming as a partner role; Friday studio = 10/5/30/5 with the
red-team block RETIRED and milestones WORKED ON (not presented); nb01
restructured (panel explainer, pathways named, partner cell before the
puzzle, book-ch4 never-delegate link, per-code-cell expectation +
"Reading the output" narration — standing rule, exemplar nb01 +
companion generator); syllabus book-first + AI-generated translations.
(5.8 — same-day addendum (2026-07-29, DECISIONS.md D29): one
brand — site sidebar carries the EDR|AI wordmark and the book's neutral
palette (gold retired from styles.css); `nbbuild.py` prepends a generated
logo cell to every built notebook (injected once into existing ones);
AI-image disclosure note under the book image on the main page ×3.
(5.7 — seventh instructor review round (2026-07-29, DECISIONS.md
D28): BOOK_VOICE_POLICY (book must never read as AI-generated; adapted from
mgaldino's rewrite-introduction style guide for the undergrad audience) +
`voice_lint_book.py`; enrollment language banned (self-learning framing
instead); preface restructured ×3 with For students / For instructors /
Languages sections; `description:` blurb removed from the three book
`_quarto.yml`. (5.6 — sixth instructor review round (2026-07-28, DECISIONS.md
D27): pill-button language switcher; designed Part I figure
(`build_book_part1_figure.py`, mermaid retired); part1-overview joins the
banner registry; enriched author page ×3; companion-notebook header spec
(logo + "Authored by Davi Moreira" + no artifact-boundary meta-commentary
rule); badge implicit-figure caption fix ×111; 3D book mockup in the
preface ×3. (5.5 — fifth instructor review round (2026-07-28, DECISIONS.md
D26): For-Instructors appendix password-locked in all three editions
(post-render encryption; password only in gitignored
`_production_kit/page_password.txt`, requested by email, scrubbed from all
committed docs); auto-derived **"It is your turn" rubrics** in every companion
notebook + the locked appendix (`_iyt-rubrics.qmd`); under-development
banners on all 37 chapters driven by `planning/BOOK_REVIEW_STATUS.yml` +
`update_chapter_review_banners.py`; standing seeded-simulation content rule
with first tranche ch11/ch14/ch15 (`build_book_sim_figures.py`); book-funding
search tracked as private course task #17. (5.4 — fourth instructor review
round (2026-07-28, DECISIONS.md
D25): book/course SEPARATION — every chapter gets its OWN companion Colab
notebook (`notebooks/book/`, EN/PT/ES, built by
`scripts/build_book_notebooks.py`; chapter badges repointed; "Colab
laboratory" sections re-anchored); new **For Instructors** appendix (×3
editions) presenting the companion course; milestone briefs M0–M15 carry Book
Anchors collecting the chapters' "It is your turn" sections (submission-table
row added); About the Author moved to right after the Preface; author "Davi
Moreira"; new preface/description blurb ("undergraduates who aspire to produce
high-quality research with scientific impact"); validator extended (companion
links, For-Instructors coverage, localized companions). (5.3 — third
instructor review round (2026-07-27,
D24): the book becomes **EDR|AI — Evidence-Driven Research in the Age of AI**,
a SELF-CONTAINED MANUAL: per-chapter "It is your turn" sections chaining into a
full research artifact (Verification lab / Project transfer / Defend sections
retired; Reading boxes retired; sync-validator elements updated); domains econ
/ political science / business / biology; the AI loop taught from ch. 3;
per-page language switcher; Part I overview page with diagram; appendices:
SRL, Verification Guide, About the Author; site tab "Book: EDR|AI" (new tab);
nb01 = orientation Lecture 1 with ⚙️ Setup section and updated bio. (5.2 —
second instructor review round (2026-07-27,
D23): EDR|AI (then 'EDRAI') acronym + book-first loop (notebooks reflect the book; instructor
reviews the book; assistant propagates; institution-agnostic body), EDR|AI
required / RDSS recommended reading model, PT-BR + ES book translations
(book-pt/, book-es/ — EN is source of truth), AI-reviews-AI-human-decides
callouts, provenance metadata lines + "all positions" tags retired from
notebooks, upgraded claim standard, professor intro opening nb01, syllabus
de-policying. (5.1 — first instructor review round (2026-07-27, D22):
week-aligned numbering nb01–nb16, random SRL slots with notebook-embedded
student-visible SRL Lead Briefs, quiz-first Fridays (10-min printed MC quiz;
`_quizzes/2026Fall/weekly/`), confirmed assessment weights, course book
retitled (now EDR|AI, D24) (work in progress) with the SRL
appendix. (5.0 = v2 prompt-architecture rebuild 2026-07-22/23, D17–D21: 16
weekly topics, milestones M0–M15, SRL flipped classroom, AI Research Ledger +
SDIIVDD, GenAI Studio reviewer bench, 37-chapter course book, 43-meeting
calendar; 4.0 = 2026-07-20 course redesign D13–D16; 3.0 = RDSS inquiry compass
2026-07-19; 2.0 = v1 build complete; 1.0 = seeded from MGMT474 infra.))))))))))))))
**Maintained by:** Professor Davi Moreira + AI Assistants
